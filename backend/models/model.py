import tensorflow as tf
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def load_model(model_path):
    """
    Load the trained model from disk.

    Args:
        model_path (str): Path to the saved model.

    Returns:
        model: Loaded Keras model.
    """
    try:
        logging.info(f"Loading model from {model_path}")
        model = tf.keras.models.load_model(model_path)
        logging.info("Model loaded successfully.")
        return model
    except Exception as e:
        logging.error(f"An error occurred while loading the model: {e}")
        raise

def predict(input_data, model_path, pipeline):
    """
    Make predictions using the trained model.

    Args:
        input_data (list): Input features for prediction.
        model_path (str): Path to the saved model.
        pipeline: Preprocessing pipeline for scaling.

    Returns:
        prediction: Predicted value.
    """
    try:
        logging.info("Starting prediction process.")

        # Load the trained model
        model = load_model(model_path)

        # Preprocess input data
        if not isinstance(input_data, list):
            logging.error("Input data must be a list of numeric values.")
            raise ValueError("Invalid input data format.")
        input_data = np.array(input_data).reshape(1, -1)
        input_data = pipeline.transform(input_data)

        # Make predictions
        prediction = model.predict(input_data)
        logging.info(f"Prediction successful: {prediction[0][0]}")
        return prediction[0][0]
    except Exception as e:
        logging.error(f"An error occurred during prediction: {e}")
        raise
