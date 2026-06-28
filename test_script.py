from flask import Flask,jsonify
import joblib
import numpy as np



app=Flask(__name__)
@app.route('/check-drift', methods=['GET'])
def check_drift():
    model=joblib.load("baseline_model.pkl")


    new_x =np.load("new_data_X.npy", allow_pickle=True)
    new_y=np.load("new_data_y.npy", allow_pickle=True)

    predictions=model.predict(new_x)

    from sklearn.metrics import accuracy_score
    accuracy=m=accuracy_score(new_y,predictions)

    THRESHOLD =0.80
    drift_detected=accuracy<THRESHOLD

    result = {
        "accuracy": round(accuracy, 3),
        "drift_detected": bool(drift_detected),
        "message": "Drift detected! Retraining needed." if drift_detected else "Model healthy."
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)

