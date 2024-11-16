from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from models.preprocess import preprocess_data
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def build_model(input_dim):
    try:
        logging.info("Building the neural network model.")
        model = Sequential([
            Dense(128, activation='relu', input_dim=input_dim),
            Dropout(0.3),
            Dense(64, activation='relu'),
            Dropout(0.3),
            Dense(1, activation='sigmoid')  # Binary classification
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        logging.info("Model built successfully.")
        return model
    except Exception as e:
        logging.error(f"An error occurred while building the model: {e}")
        raise

def train_and_save_model(input_path, model_path, features_start, features_end, target_start, target_end):
    try:
        logging.info("Starting model training process.")
        
        # Preprocess the data
        X_train, X_test, y_train, y_test, _ = preprocess_data(input_path, features_start, features_end, target_start, target_end)

        # Validate input dimensions
        if X_train.shape[1] == 0:
            logging.error("No features available for training. Check preprocessing.")
            raise ValueError("Feature data is empty or invalid.")

        # Build and train the model
        model = build_model(input_dim=X_train.shape[1])
        logging.info("Training the model...")
        model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))
        
        # Save the model
        model.save(model_path)
        logging.info(f"Model trained and saved successfully to {model_path}.")
    except Exception as e:
        logging.error(f"An error occurred during model training: {e}")
        raise
