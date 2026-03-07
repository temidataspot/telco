# Customer Churn Prediction & Analysis 
### Telco Customer Retention: End-to-End Machine Learning Project

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-orange?logo=scikit-learn)
![XGBoost](https://img.shields.io/badge/XGBoost-1.7+-red)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-brightgreen?logo=streamlit)
![SHAP](https://img.shields.io/badge/SHAP-Explainability-yellow)

### Dashboard

[![Streamlit Dashboard](https://img.shields.io/badge/Streamlit-Dashboard-247ba0)](https://telcos.streamlit.app/)


[![Vercel Dashboard](https://img.shields.io/badge/React-Dashboard-247ba0)](https://telco-hazel.vercel.app/)

---

## 🔗 Quick Links

| Resource | Link |
|---|---|
| Notebook | [Telco.ipynb](https://github.com/temidataspot/telco/blob/main/Telco.ipynb) |
| Dataset | [IBM Telco Customer Churn ](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) |
| Model Outputs | [churn_model_comparison_v2.csv](https://github.com/temidataspot/telco/blob/main/outputs/rf_full_predictions.csv) |
| Metrics Summary | [model_metrics_summary.csv](https://github.com/temidataspot/telco/blob/main/visuals/model_comparison.png) |

---

## Overview

Customer churn: when a customer stops using a service, is one of the most costly problems in the telecommunications industry. Acquiring a new customer can cost **5–7x more** than retaining an existing one. This project builds a full machine learning pipeline to:

- **Predict** which customers are likely to churn
- **Compare** multiple models to find the best approach
- **Explain** *why* customers churn using SHAP values
- **Deliver** actionable business recommendations
- **Visualise** results via an interactive Streamlit dashboard

---

---

##  Dataset

**Source:** IBM: [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

- **7,043 customers**, 21 features
- **Churn rate: ~26.5%** (imbalanced dataset)
- Features include: contract type, tenure, monthly charges, internet service, payment method, and add-on services

---

## ⚙️ Methodology

### 1. Data Preprocessing
- Converted `TotalCharges` to numeric (contained hidden whitespace)
- Encoded target: `Churn → {Yes: 1, No: 0}`
- Built a `ColumnTransformer` pipeline:
  - **Numeric:** Median imputation + StandardScaler
  - **Categorical:** Constant imputation + OneHotEncoder
- Stratified 80/20 train-test split

### 2. Handling Class Imbalance
The dataset is imbalanced (~73% No Churn / ~27% Churn). Two strategies were applied:
- **SMOTE** (Synthetic Minority Oversampling): generates synthetic churn samples in the training set
- **`class_weight='balanced'`**: used natively in Random Forest

### 3. Models Trained
Four models were trained progressively, from simple to complex:

| Step | Model | Purpose |
|---|---|---|
| 1 | Logistic Regression | Interpretable baseline |
| 2 | Logistic Regression + SMOTE | Improved recall via oversampling |
| 3 | Random Forest | Ensemble method, handles imbalance natively |
| 4 | XGBoost | Gradient boosting, best overall performance |

### 4. Evaluation Strategy
- Primary metric: **Recall** (catching as many churners as possible)
- Secondary metrics: F1 Score, ROC-AUC, Accuracy, Precision
- **5-Fold Stratified Cross-Validation** to confirm robustness
- **SHAP values** for model explainability

---

## Results

### Model Comparison Table

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression (Baseline) | 0.8034 | 0.6520 | 0.5561 | 0.6003 | 0.8417 |
| Logistic + SMOTE | 0.7615 | 0.5380 | 0.7193 | 0.6156 | 0.8399 |
| Random Forest | 0.7296 | 0.4941 | **0.7834** | 0.6060 | 0.8154 |
| **XGBoost** | 0.7800 | 0.5777 | 0.6364 | **0.6056** | **0.8430** |

###  Visual: Model Performance Comparison
![Model Comparison Bar Chart](https://github.com/temidataspot/telco/blob/main/visuals/model_comparison.png)

###  Visual: ROC Curves: All Models
![ROC Curves](https://github.com/temidataspot/telco/blob/main/visuals/roc_curves_all_models.png)

---

## Cross-Validation Results

"Cross-validation confirms XGBoost as the most robust model with the highest mean F1 of ~0.858. While Random Forest achieved the highest recall on the held-out test set, its CV performance was lower and less stable, suggesting it may be slightly overfitting to SMOTE-resampled data."

To ensure the models generalise well beyond the test set, 5-Fold Stratified Cross-Validation was applied on F1 Score.

| Model | CV Mean F1 | Std Dev |
|---|---|---|
| Logistic Regression | ~0.845 | Very low  |
| Random Forest | ~0.800 | Low (1 outlier) |
| **XGBoost** | **~0.858** | **Low ** |

**Key insight:** XGBoost not only outperforms on the test set, it is the most consistent model across all 5 folds, confirming it is not just lucky on one split.

### 📈 Visual: Cross-Validation Boxplot
![Cross-Validation Boxplot](https://github.com/temidataspot/telco/blob/main/visuals/cross_validation_boxplot.png)

---

## SHAP Explainability

SHAP (SHapley Additive exPlanations) was used to explain *why* XGBoost makes each prediction, translating a black-box model into actionable business insight.

### Visual: SHAP Summary Plot
![SHAP Summary](https://github.com/temidataspot/telco/blob/main/visuals/shap_summary.png)

### Key SHAP Findings

"SHAP analysis reveals that contract type and tenure are the dominant churn drivers. Month-to-month customers with short tenure, no security add-ons, and paying via electronic check represent the highest-risk segment. Two-year contract holders show strong negative SHAP values, confirming that locking customers into longer contracts is the most effective retention strategy."

| Feature | Direction | Interpretation |
|---|---|---|
| **Contract_Month-to-month** | ⬆️ Increases churn | Biggest single driver of churn |
| **Tenure (low)** | ⬆️ Increases churn | New customers are highest risk |
| **Tenure (high)** | ⬇️ Reduces churn | Long-term customers rarely leave |
| **OnlineSecurity_No** | ⬆️ Increases churn | Customers without security add-on churn more |
| **InternetService_Fiber optic** | ⬆️ Increases churn | Fiber customers show elevated churn risk |
| **PaymentMethod_Electronic check** | ⬆️ Increases churn | Less committed payment behaviour |
| **TechSupport_No** | ⬆️ Increases churn | Lack of support increases dissatisfaction |
| **MonthlyCharges (high)** | ⬆️ Increases churn | Price sensitivity is real |
| **Contract_Two year** | ⬇️ Reduces churn | Strong protective factor against churn |


![SHAP Feature Importance](https://github.com/temidataspot/telco/blob/main/visuals/shap_feature_importance.png)

---

## Business Interpretation & Recommendations

### Why Recall is the Primary Metric
In churn prediction, **missing a churner costs far more than a false alarm**. Sending a retention offer to someone who wasn't leaving is a small cost. Losing a customer permanently is a much bigger loss. This is why Recall was prioritised over Accuracy throughout this project.

### Model Selection for Business Use

> *"Logistic Regression gave us a clean, interpretable baseline. SMOTE improved recall from 56% to 72%, proving the value of handling class imbalance. Random Forest achieved the highest raw recall at 78%, making it ideal when catching every single churner is paramount. XGBoost delivered the best balance across all metrics with the highest ROC-AUC and cross-validation F1, making it the recommended production model."*

### Actionable Recommendations from SHAP

| Insight | Recommended Action | Expected Impact |
|---|---|---|
| Month-to-month contracts = #1 churn driver | Offer discounts/incentives to upgrade to annual plans | High |
| New customers (low tenure) = highest risk | Launch proactive onboarding programme for first 3–6 months | High |
| No OnlineSecurity / TechSupport = churn risk | Bundle these as free add-ons for new or at-risk customers | Medium–High |
| Electronic check payers churn more | Nudge toward auto-pay or credit card with a small incentive | Medium |
| Fiber optic customers churn more | Review fiber pricing and service quality vs competitors | Medium |
| High monthly charges = churn risk | Identify customers paying > £70/month for targeted offers | Medium |

### Ensemble Risk Scoring
A **High Risk** flag was created in the master output file: customers flagged as churn by **3 or more models** simultaneously are prioritised for immediate intervention, reducing the chance of acting on a single model's error.

---


##  Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.9+ | Core language |
| Pandas / NumPy | Data manipulation |
| Scikit-Learn | Preprocessing, models, metrics |
| XGBoost | Gradient boosting model |
| Imbalanced-Learn | SMOTE oversampling |
| SHAP | Model explainability |
| Matplotlib / Seaborn | Static visualisations |
| Streamlit + Plotly | Interactive dashboard |

---

## 👤 Author

**Temiloluwa Priscilla Jokotola**
📧 [Email](mailto:temi@cognivinelab.com)
🔗 [LinkedIn](https://linkedin.com/in/temiloluwa-priscilla-jokotola)
🐙 [GitHub](https://github.com/temidataspot)

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*If you found this project useful, please consider giving it a ⭐ on GitHub!*
