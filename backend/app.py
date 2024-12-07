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
import pandas as pd

# Define combine_features function
def combine_features(X):
    # Custom logic for combining or transforming features
    mean_cols = ['High School Average Mark', 'Math Score']
    mode_cols = ['Prev Education', 'Age Group', 'English Grade']
    fill_with_0_cols = ['1st Term GPA', '2nd Term GPA']
    fill_with_3_cols = ['First Language']
    passthrough_cols = ['Funding', 'Fast Track', 'Coop', 'Residency', 'Gender']
    
    column_names = mean_cols + fill_with_0_cols + fill_with_3_cols + mode_cols + passthrough_cols
    df_handle_missing = pd.DataFrame(X, columns=column_names)
    
    # Fill missing values
    df_handle_missing[mean_cols] = df_handle_missing[mean_cols].fillna(df_handle_missing[mean_cols].mean())
    df_handle_missing[fill_with_0_cols] = df_handle_missing[fill_with_0_cols].fillna(0)
    df_handle_missing[fill_with_3_cols] = df_handle_missing[fill_with_3_cols].fillna(3)
    df_handle_missing[mode_cols] = df_handle_missing[mode_cols].fillna(df_handle_missing[mode_cols].mode().iloc[0])
    
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

# API Key for Admin
API_KEY = "zu9gLCNscr8vlAKXqZ6zMH4bXIAfI43H"

# Default model and pipeline
current_model_path = os.path.join(MODEL_DIR, "model1.keras")
current_pipeline_path = os.path.join(PIPELINE_DIR, "pipeline1.pkl")
current_model = tf.keras.models.load_model(current_model_path)
current_pipeline = joblib.load(current_pipeline_path)

# Protect admin endpoints with API key
@app.before_request
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

    global current_model, current_pipeline
    current_model = tf.keras.models.load_model(model_path)
    current_pipeline = joblib.load(pipeline_path)

    return jsonify({"message": f"Model switched to {model_name} and pipeline to {pipeline_name}."})

# Upload a new model
# Upload a new model
@app.route('/admin/upload_model', methods=['POST'])
def upload_model():
    try:
        # Check if the request contains a file
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        # Check if the file has a valid filename
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Ensure the file is a valid Keras model file
        if not file.filename.endswith('.keras'):
            return jsonify({"error": "Invalid file type. Only .keras files are allowed"}), 400

        # Save the uploaded file to the MODEL_DIR
        filename = secure_filename(file.filename)
        file.save(os.path.join(MODEL_DIR, filename))

        return jsonify({"message": f"Model {filename} uploaded successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.json
        df = pd.DataFrame([input_data])  # Convert input to DataFrame
        
        # Preprocess data using the active pipeline
        preprocessed_data = current_pipeline.transform(df)
        
        # Make prediction using the active model
        prediction = current_model.predict(preprocessed_data)
        
        # Return the result
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)