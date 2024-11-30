from flask import Flask, request, jsonify
import tensorflow as tf
import joblib
import numpy as np
import pandas as pd
import os
import sklearn.pipeline
from sklearn.preprocessing import FunctionTransformer

# Define passthrough function
def passthrough(X):
    return X


app = Flask(__name__)

# Load the model and pipeline
path = "./model/"

model_fullpath = os.path.join(path, 'best_model.keras')
pipeline_fullpath = os.path.join(path, 'final_pipeline.pkl')

model = tf.keras.models.load_model(model_fullpath)
pipeline = joblib.load(pipeline_fullpath)

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from request
    input_data = request.json
    df = pd.DataFrame([input_data])  # Convert input to DataFrame
    
    # Preprocess data using pipeline
    preprocessed_data = pipeline.transform(df)
    
    # Make prediction
    prediction = model.predict(preprocessed_data)
    
    # Return the result
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=False)
