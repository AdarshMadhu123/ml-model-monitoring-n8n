# ML Model Monitoring & Auto-Alert Pipeline (n8n + Flask)

An automated MLOps-style pipeline that monitors a deployed machine learning model for **performance drift**, logs results to Google Sheets, and sends an **email alert** automatically when the model's accuracy drops below a defined threshold — built using **n8n** (workflow automation) and **Flask** (REST API).

## 🎯 Problem this solves

In real production systems, ML models silently degrade over time as real-world data changes (this is called **data/model drift**). Most teams only discover this when something goes wrong downstream. This project simulates a **daily automated health-check system** for a deployed model — exactly the kind of monitoring real MLOps teams build.

## 🏗️ Architecture

```
[Schedule Trigger - runs daily]
        ↓
[HTTP Request → Flask API]
        ↓
[Flask: loads model, predicts on new data, calculates accuracy]
        ↓
[IF: accuracy < threshold?]
   ↓ YES (Drift)                  ↓ NO (Healthy)
[Log to Google Sheets]        [Log to Google Sheets]
        ↓
[Send Email Alert] 
```

## ⚙️ Tech Stack

- **n8n** – visual workflow orchestration (Schedule Trigger, HTTP Request, IF logic, Google Sheets, Gmail nodes)
- **Flask** – lightweight Python REST API serving the model and drift-check logic
- **scikit-learn** – RandomForestClassifier trained on the Iris dataset
- **Google Sheets API** – persistent logging of every health check (timestamp, accuracy, drift status, action taken)
- **Gmail API** – automated email alerts on drift detection

## 🔍 How it works

1. **Training (`train_model.py`)** – Trains a RandomForest model on the Iris dataset and saves it (`baseline_model.pkl`), along with a holdout "new data" set that simulates incoming production data.
2. **Monitoring API (`test_script.py`)** – A Flask endpoint (`/check-drift`) that loads the saved model, runs predictions on the "new" data, and calculates current accuracy. If accuracy falls below 80%, it flags `drift_detected: true`.
3. **Orchestration (n8n)** – A scheduled workflow calls this API daily, branches based on the result:
   - **Healthy** → logs the result to Google Sheets
   - **Drift detected** → logs to Google Sheets **and** sends an automated email alert

## 📊 Example Output (Google Sheets log)

| Timestamp | Accuracy | Drift Detected | Action |
|---|---|---|---|
| 2026-06-28T04:18:10 | 1.0 | false | No action needed |
| 2026-06-28T04:24:51 | 0.74 | true | Retraining triggered |

## 🚀 Running it yourself

1. Install dependencies: `pip install flask scikit-learn pandas numpy joblib`
2. Train the model: `python train_model.py`
3. Start the API: `python test_script.py`
4. Import `workflow.json` into a running n8n instance (`npx n8n`)
5. Connect your own Google Sheets + Gmail credentials in n8n
6. Activate the workflow

## 💡 What this project demonstrates

- End-to-end ML lifecycle thinking (not just training a model once, but monitoring it in "production")
- REST API development for serving ML models
- Workflow automation / orchestration design
- Conditional logic and branching in automated pipelines
- Third-party API integration (Google Sheets, Gmail) via OAuth2
- Practical debugging (port conflicts, OAuth scopes, data flow issues)

## 📌 Future improvements

- Replace simulated "new data" with a real streaming data source
- Add automatic model retraining when drift is detected
- Add a Slack/Telegram notification option
- Build a simple dashboard on top of the Google Sheets log
