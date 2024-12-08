from flask import Flask, request, jsonify
import tensorflow as tf
import joblib
import numpy as np
import pandas as pd
import os
import sklearn.pipeline
from sklearn.preprocessing import FunctionTransformer
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json  # NEW: To persist selected model/pipeline

# Define combine_features function
def combine_features(X):
    mean_cols = ['High School Average Mark', 'Math Score']
    mode_cols = ['Prev Education', 'Age Group', 'English Grade']
    fill_with_0_cols = ['1st Term GPA', '2nd Term GPA']
    fill_with_3_cols = ['First Language']
    passthrough_cols = ['Funding', 'Fast Track', 'Coop', 'Residency', 'Gender']
    
    column_names = mean_cols + fill_with_0_cols + fill_with_3_cols + mode_cols + passthrough_cols
    df_handle_missing = pd.DataFrame(X, columns=column_names)
    
    # Convert the columns to the appropriate types
    num_cols = ['High School Average Mark', 'Math Score', '1st Term GPA', '2nd Term GPA']
    cat_cols = ['First Language', 'Funding', 'Fast Track', 'Coop', 'Residency', 'Gender', 'Prev Education', 'Age Group', 'English Grade']
    
    df_handle_missing[num_cols] = df_handle_missing[num_cols].apply(pd.to_numeric, errors='coerce')
    df_handle_missing[cat_cols] = df_handle_missing[cat_cols].astype('int')
    df_handle_missing[cat_cols] = df_handle_missing[cat_cols].astype('object')
    
    return df_handle_missing

# Define passthrough function
def passthrough(X):
    return X

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# Directories
MODEL_DIR = "./model/"
PIPELINE_DIR = "./pipeline/"
CONFIG_FILE = "./model/selected_model.json"
USER_FILE = "./users.json" 

# API Key for Admin
API_KEY = "zu9gLCNscr8vlAKXqZ6zMH4bXIAfI43H"

# Default model and pipeline
current_model_path = os.path.join(MODEL_DIR, "model1.keras")
current_pipeline_path = os.path.join(PIPELINE_DIR, "pipeline1.pkl")

# NEW: Load selected model/pipeline from saved config
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as config_file:
        config = json.load(config_file)
        model_name = config.get("model", "model2.keras")
        pipeline_name = config.get("pipeline", "pipeline2.pkl")
        current_model_path = os.path.join(MODEL_DIR, model_name)
        current_pipeline_path = os.path.join(PIPELINE_DIR, pipeline_name)
        current_model_name = model_name

# Load the model and pipeline
current_model = tf.keras.models.load_model(current_model_path)
current_pipeline = joblib.load(current_pipeline_path)

def load_users():
    with open(USER_FILE, "r") as file:
        return json.load(file)

# Protect admin endpoints with API key
@app.before_request
def handle_options_requests():
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight"})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,x-api-key")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 200

def require_api_key():
    if request.endpoint in ["list_models", "list_pipelines", "change_model"]:
        api_key = request.headers.get("x-api-key")
        if api_key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401

# List available models
@app.route('/admin/models', methods=['GET'])
def list_models():    
    available_models = [f for f in os.listdir(MODEL_DIR) if f.endswith(".keras")]
    return jsonify({"available_models": available_models})

# List available pipelines
@app.route('/admin/pipelines', methods=['GET'])
def list_pipelines():
    available_pipelines = [f for f in os.listdir(PIPELINE_DIR) if f.endswith(".pkl")]
    return jsonify({"available_pipelines": available_pipelines})

# Change the active model and pipeline
@app.route('/admin/change_model', methods=['POST'])
def change_model():
    data = request.get_json()
    model_name = data.get("model_name")
    pipeline_name = data.get("pipeline_name")

    model_path = os.path.join(MODEL_DIR, model_name)
    pipeline_path = os.path.join(PIPELINE_DIR, pipeline_name)

    if not os.path.exists(model_path):
        return jsonify({"error": f"Model {model_name} does not exist"}), 400
    if not os.path.exists(pipeline_path):
        return jsonify({"error": f"Pipeline {pipeline_name} does not exist"}), 400

    try:
        global current_model, current_pipeline
        current_model = tf.keras.models.load_model(model_path)
        current_pipeline = joblib.load(pipeline_path)

        # NEW: Persist selection
        with open(CONFIG_FILE, "w") as config_file:
            json.dump({"model": model_name, "pipeline": pipeline_name}, config_file)
            
            # PRINT STATEMENTS: Confirm the model and pipeline change
        print(f"Switched to model: {model_name}")
        print(f"Switched to pipeline: {pipeline_name}")

        return jsonify({"message": f"Model switched to {model_name} and pipeline to {pipeline_name}."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Upload a new model
@app.route('/admin/upload_model', methods=['POST'])
def upload_model():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if not file.filename.endswith('.keras'):
            return jsonify({"error": "Invalid file type. Only .keras files are allowed"}), 400

        filename = secure_filename(file.filename)
        file.save(os.path.join(MODEL_DIR, filename))

        return jsonify({"message": f"Model {filename} uploaded successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Predict endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.json
        df = pd.DataFrame([input_data])
        preprocessed_data = current_pipeline.transform(df)
        prediction = current_model.predict(preprocessed_data)
        confidence = float(prediction[0][0])
        persist = confidence >= 0.5

        return jsonify({
            'persist': persist,
            'confidence': confidence
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    users_data = load_users()

    for user in users_data.get("users", []):
        if user["username"] == username and user["password"] == password:
            return jsonify({"message": "Login successful", "token": "valid_admin_token"}), 200

    return jsonify({"message": "Invalid username or password"}), 401

if __name__ == '__main__':
    app.run(debug=False)
