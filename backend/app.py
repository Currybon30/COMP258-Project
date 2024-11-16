from flask import Flask, request, jsonify
from models.train import train_and_save_model
from models.model import predict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from .env
DATASET_PATH = os.getenv('DATASET_PATH')
MODEL_PATH = os.getenv('MODEL_PATH')
FEATURES_START = int(os.getenv('FEATURES_START'))
FEATURES_END = int(os.getenv('FEATURES_END'))
TARGET_START = int(os.getenv('TARGET_START'))
TARGET_END = int(os.getenv('TARGET_END'))

app = Flask(__name__)

@app.route('/train', methods=['POST'])
def train():
    train_and_save_model(DATASET_PATH, MODEL_PATH, FEATURES_START, FEATURES_END, TARGET_START, TARGET_END)
    return jsonify({"message": "Model trained and saved successfully."})

@app.route('/predict', methods=['POST'])
def make_prediction():
    input_data = request.json['data']
    pipeline = ...  # Load the preprocessing pipeline if saved
    result = predict(input_data, MODEL_PATH, pipeline)
    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(debug=True)
