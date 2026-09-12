from sklearn.ensemble import IsolationForest


def build_anomaly_model():
    """
    Create and return the anomaly detection model.
    """

    return IsolationForest(
        n_estimators=200,
        contamination=0.2,
        random_state=42
    )