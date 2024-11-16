import tensorflow as tf
import numpy as np

def load_model(model_path):
    """
    Load the trained model from disk.

    Args:
        model_path (str): Path to the saved model.

    Returns:
        model: Loaded Keras model.
    """
    return tf.keras.models.load_model(model_path)

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
    # Load the trained model
    model = load_model(model_path)

    # Preprocess the input data
    input_data = np.array(input_data).reshape(1, -1)
    input_data = pipeline.transform(input_data)

    # Make predictions
    prediction = model.predict(input_data)
    return prediction[0][0]
