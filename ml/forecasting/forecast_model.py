from sklearn.ensemble import HistGradientBoostingRegressor

def build_forecast_model():
    return HistGradientBoostingRegressor(
        learning_rate=0.08,
        max_iter=150,
        max_leaf_nodes=31,
        l2_regularization=1.0,
        early_stopping=False,
        random_state=42,
    )