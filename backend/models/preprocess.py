import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def preprocess_data(input_path, features_start, features_end, target_start, target_end):
    """
    Preprocess the dataset.

    Args:
        input_path (str): Path to the dataset CSV file.
        features_start (int): Start index of feature columns in the raw data.
        features_end (int): End index of feature columns in the raw data.
        target_start (int): Start index of the target column in the raw data.
        target_end (int): End index of the target column in the raw data.

    Returns:
        X_train, X_test, y_train, y_test: Preprocessed and split data.
        pipeline: Preprocessing pipeline used for scaling.
    """
    # Load dataset
    data = pd.read_csv(input_path)
    df = pd.DataFrame(data)

    # Extract feature and target column names
    features = df.iloc[features_start:features_end, 0].to_list()
    target = df.iloc[target_start:target_end, 0].to_list()
    cleaned_columns = [col.replace(" numeric", "").replace("'", "").strip() for col in features + target]

    # Apply cleaned column names
    df.columns = cleaned_columns
    df = df.iloc[23:, ].reset_index(drop=True)

    # Feature and target separation
    X = df[features]
    y = df[target]

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a preprocessing pipeline
    pipeline = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])

    # Apply preprocessing
    X_train = pipeline.fit_transform(X_train)
    X_test = pipeline.transform(X_test)

    return X_train, X_test, y_train, y_test, pipeline
