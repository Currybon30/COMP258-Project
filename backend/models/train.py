from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from models.preprocess import preprocess_data

def build_model(input_dim):
    """
    Build the neural network model.

    Args:
        input_dim (int): Number of input features.

    Returns:
        model: Compiled Keras model.
    """
    model = Sequential([
        Dense(128, activation='relu', input_dim=input_dim),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(1, activation='sigmoid')  # For binary classification
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_and_save_model(input_path, model_path, features_start, features_end, target_start, target_end):
    """
    Train the model and save it.

    Args:
        input_path (str): Path to the dataset.
        model_path (str): Path to save the trained model.
    """
    # Preprocess the data
    X_train, X_test, y_train, y_test, _ = preprocess_data(input_path, features_start, features_end, target_start, target_end)

    # Build the model
    model = build_model(input_dim=X_train.shape[1])

    # Train the model
    model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

    # Save the model
    model.save(model_path)
