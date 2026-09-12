from sklearn.ensemble import RandomForestRegressor


def build_recommendation_model():
    """
    Create and return the recommendation model.
    """

    return RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )