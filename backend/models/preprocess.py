import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_data(input_path, features_start, features_end, target_start, target_end):
    try:
        logging.info(f"Loading dataset from {input_path}")
        data = pd.read_csv(input_path)
        df = pd.DataFrame(data)

        # Extract feature and target column names
        features = df.iloc[features_start:features_end, 0].to_list()
        target = df.iloc[target_start:target_end, 0].to_list()
        cleaned_columns = [col.replace(" numeric", "").replace("'", "").strip() for col in features + target]

        # Validate column names
        if len(features) == 0 or len(target) == 0:
            logging.error("Feature or target columns are missing. Check column indices.")
            raise ValueError("Invalid column indices provided for feature/target extraction.")

        # Apply cleaned column names
        logging.info("Cleaning column names and resetting the dataframe.")
        df.columns = cleaned_columns
        df = df.iloc[23:, ].reset_index(drop=True)

        # Feature and target separation
        X = df[features]
        y = df[target]

        # Split the data
        logging.info("Splitting the dataset into training and testing sets.")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create a preprocessing pipeline
        logging.info("Initializing preprocessing pipeline for scaling.")
        pipeline = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])

        # Apply preprocessing
        X_train = pipeline.fit_transform(X_train)
        X_test = pipeline.transform(X_test)

        logging.info("Preprocessing completed successfully.")
        return X_train, X_test, y_train, y_test, pipeline
    except Exception as e:
        logging.error(f"An error occurred during preprocessing: {e}")
        raise
