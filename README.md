# CRM360 – Customer Analytics & Prediction Platform

## Overview

CRM360 is a customer analytics platform designed to help businesses understand customer behaviour, identify potential churn, segment customers, and analyze revenue trends using machine learning.

The application integrates customer data processing, predictive modelling, and interactive dashboards to support data-driven business decisions.

## Key Features

- **Customer Churn Prediction:** Predicts customer churn using Logistic Regression and Random Forest.
- **Customer Segmentation:** Groups customers based on purchasing behaviour using RFM analysis and K-Means clustering.
- **Revenue Forecasting:** Uses Ridge Regression and historical revenue features for forecasting.
- **Deal Win/Loss Prediction:** Uses Decision Tree classification to analyze deal outcomes.
- **Customer Analytics:** Displays important business KPIs, revenue summaries, and customer insights.
- **Interactive Dashboard:** Provides visualizations and analytical results through Streamlit.

## Tech Stack

| Category | Technologies |
| Programming | Python, SQL |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | MySQL |
| ORM | SQLAlchemy |
| Model Optimization | GridSearchCV, Cross-Validation |
| Model Persistence | Joblib |
| Visualization | Streamlit Charts, Matplotlib, Seaborn |

## Machine Learning Implementation

### 1. Customer Churn Prediction
- Logistic Regression
- Random Forest Classifier
- SMOTE / Class Weighting for class imbalance
- GridSearchCV for hyperparameter tuning
- Evaluation using Accuracy, Precision, Recall and F1-score

### 2. Customer Segmentation
- RFM (Recency, Frequency, Monetary) analysis
- K-Means clustering
- Elbow Method
- Silhouette Score
- PCA for dimensionality reduction and visualization

### 3. Revenue Forecasting
- Ridge Regression
- RidgeCV for regularization parameter selection
- Lag features
- Rolling statistical features

### 4. Deal Win/Loss Prediction
- Decision Tree Classifier

## System Architecture

The application follows a modular architecture:

1. **Data Layer:** MySQL stores structured application data.
2. **Backend Layer:** FastAPI handles API requests and business logic.
3. **ML Layer:** Processes customer data and generates predictions and analytical insights.
4. **Frontend Layer:** Streamlit provides interactive dashboards and visualizations.

## Project Structure

```text
CRM360/
│
├── app/
│   ├── routers/
│   ├── services/
│   ├── schemas/
│   ├── models/
│   └── config/
│
├── data/
│
├── notebooks/
│
├── frontend/
│
├── ml/
│
├── requirements.txt
├── .env.example
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd CRM360
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

Windows:
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file using `.env.example` and configure the required database and application settings.

### 5. Run the Backend

```bash
uvicorn app.main:app --reload
```

### 6. Run the Frontend

```bash
streamlit run frontend/frontend.py
```

## Results
<img width="1917" height="928" alt="image" src="https://github.com/user-attachments/assets/78c49897-f9e5-4a14-96b4-ecc2d3693390" />
<img width="1916" height="912" alt="image" src="https://github.com/user-attachments/assets/162431f3-56eb-4ccb-83e5-7f5eb9ba686d" />
<img width="1917" height="920" alt="image" src="https://github.com/user-attachments/assets/8f1ea3dc-629b-4bb5-a6e6-f8873064a683" />
<img width="1917" height="872" alt="image" src="https://github.com/user-attachments/assets/27849972-a07e-4ad3-b403-7ccae4fbe76a" />
<img width="1917" height="833" alt="image" src="https://github.com/user-attachments/assets/46f78ea1-2121-4aff-8064-14f5294a453c" />
<img width="1917" height="847" alt="image" src="https://github.com/user-attachments/assets/0b3519a2-e958-42f8-a4a5-df1404745423" />



## Future Improvements

- Enhance prediction performance with additional customer behavioural features.
- Improve model monitoring and evaluation.
- Extend customer analytics with additional business insights.
- Improve deployment and scalability.
