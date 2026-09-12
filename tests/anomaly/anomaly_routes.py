from flask import Blueprint, jsonify
from services.anomaly_service import detect_anomalies

anomaly_routes = Blueprint("anomaly_routes", __name__)

@anomaly_routes.route("/api/anomalies", methods=["GET"])
def get_anomalies():
    df = detect_anomalies()

    anomalies = df[df["anomaly"] == 1]

    result = anomalies[
        ["Datetime", "Consumption", "anomaly_score", "anomaly"]
    ].head(100)

    result["Datetime"] = result["Datetime"].astype(str)

    return jsonify({
        "total_records": len(df),
        "total_anomalies": len(anomalies),
        "anomalies": result.to_dict(orient="records")
    })