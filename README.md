# 📣 Marketing Campaign Analytics — Capstone Project

> **Improving Marketing Campaign Strategy using Business Analytics and Machine Learning**

**Author:** Dixit Mukeshkumar Patel &nbsp;|&nbsp; 📍 Perth, WA, Australia &nbsp;|&nbsp; 📧 dixitmpatel14@gmail.com

![Python](https://img.shields.io/badge/Tool-Orange%20ML-orange?logo=data:image/png;base64,&logoColor=white)
![Power BI](https://img.shields.io/badge/Tool-Power%20BI-F2C811?logo=powerbi&logoColor=black)
![Dataset](https://img.shields.io/badge/Dataset-8%2C000%20Records-blue)
![Models](https://img.shields.io/badge/Models-5%20Algorithms-green)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 🎯 Project Overview

This capstone project analyses a **digital marketing campaign dataset** of 8,000 customer records to predict whether a customer will convert, and to identify which campaign factors drive the best outcomes. The project combines **machine learning classification models** (built in Orange ML), **interactive dashboards** (Power BI), and formal written analysis (Word / PowerPoint).

**Core questions answered:**
- Which customer and campaign attributes most strongly predict conversion?
- Which machine learning model performs best at predicting conversion?
- How can marketing spend and channel targeting be improved based on the data?

---

## 📂 Repository Structure

```
marketing-analytics-capstone/
│
├── Dataset/
│   └── digital_marketing_campaign_dataset.csv   ← 8,000 rows, 20 columns
│
├── Models_Orange/
│   ├── KNN_Model.ows                             ← 5 KNN variants (k = 3, 5, 7, 10, 15)
│   ├── Logistic_Regression_Model.ows             ← L1, L2 and no-penalty variants
│   ├── Neural_Networks_Model.ows                 ← 5 MLP architectures
│   ├── Random_Forest_Model.ows                   ← 5 RF configurations (200–2000 trees)
│   ├── SVM_Model.ows                             ← Linear, Polynomial, RBF, Sigmoid kernels
│   └── Final_Model_Workflow.ows                  ← Best models combined for final comparison
│
├── PowerBI/
│   ├── Marketing_Dashboard_V1.pbix
│   └── Marketing_Dashboard_V2.pbix               ← Interactive campaign performance dashboard
│
├── Reports/
│   ├── Project_Report.docx
│   ├── Final_Project_Report.docx                 ← Final submitted report
│   └── Feedback_Report.docx
│
├── Presentation/
│   ├── Final_Presentation_V1.pptx
│   └── Final_Presentation_V2.pptx               ← Final submitted slides
│
└── README.md
```

---

## 📊 Dataset

**File:** `Dataset/digital_marketing_campaign_dataset.csv`

| Property | Value |
|---|---|
| Total records | 8,000 customers |
| Total columns | 20 (17 features + CustomerID + 2 confidential + 1 target) |
| Target variable | `Conversion` (binary: 1 = converted, 0 = not converted) |
| Converted customers | 7,012 (87.6%) |
| Not converted | 988 (12.3%) |

### Column Reference

| Column | Type | Range / Values | Description |
|---|---|---|---|
| `CustomerID` | ID | 8000 – 15999 | Unique customer identifier (excluded from modelling) |
| `Age` | Numeric | 18 – 69 (avg 43.6) | Customer age in years |
| `Gender` | Categorical | Female (60.5%), Male (39.5%) | Customer gender |
| `Income` | Numeric | $20,014 – $149,986 (avg $84,664) | Annual income in USD |
| `CampaignChannel` | Categorical | Email, PPC, Referral, SEO, Social Media | Marketing channel used |
| `CampaignType` | Categorical | Awareness, Consideration, Conversion, Retention | Campaign goal type |
| `AdSpend` | Numeric | $100 – $9,998 (avg $5,001) | Advertising spend per customer in USD |
| `ClickThroughRate` | Numeric | 0.01 – 0.30 (avg 0.15) | Ad click-through rate |
| `ConversionRate` | Numeric | 0.01 – 0.20 (avg 0.10) | Historical conversion rate |
| `WebsiteVisits` | Numeric | 0 – 49 (avg 24.8) | Number of website visits |
| `PagesPerVisit` | Numeric | 1.0 – 10.0 (avg 5.6) | Average pages viewed per visit |
| `TimeOnSite` | Numeric | 0.5 – 15.0 min (avg 7.7) | Average time on site in minutes |
| `SocialShares` | Numeric | 0 – 99 (avg 49.8) | Number of social media shares |
| `EmailOpens` | Numeric | 0 – 19 (avg 9.5) | Email opens count |
| `EmailClicks` | Numeric | 0 – 9 (avg 4.5) | Email click count |
| `PreviousPurchases` | Numeric | 0 – 9 (avg 4.5) | Number of previous purchases |
| `LoyaltyPoints` | Numeric | 0 – 4,999 (avg 2,490) | Accumulated loyalty points |
| `AdvertisingPlatform` | Categorical | Confidential | Platform used (redacted in this dataset) |
| `AdvertisingTool` | Categorical | Confidential | Tool used (redacted in this dataset) |
| `Conversion` | **Target** | 0 or 1 | **Whether the customer converted** |

### Campaign Channel Distribution

| Channel | Count | Share |
|---|---|---|
| Referral | 1,719 | 21.5% |
| PPC | 1,655 | 20.7% |
| Email | 1,557 | 19.5% |
| Social Media | 1,519 | 19.0% |
| SEO | 1,550 | 19.4% |

### Campaign Type Distribution

| Type | Count | Share |
|---|---|---|
| Conversion | 2,077 | 26.0% |
| Awareness | 1,988 | 24.9% |
| Consideration | 1,988 | 24.9% |
| Retention | 1,947 | 24.4% |

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| **Orange ML** | Visual machine learning — model building, hyperparameter tuning, evaluation |
| **Power BI** | Interactive dashboard — campaign KPIs, customer segmentation, channel analysis |
| **CSV / Excel** | Data storage and preprocessing |
| **MS Word** | Project report and documentation |
| **MS PowerPoint** | Final presentation slides |

---

## 🤖 Machine Learning Models

All models were built in Orange ML with an **80/20 train/test split** (stratified) and evaluated using **Accuracy, AUC, and Confusion Matrix**. Preprocessing applied to all workflows: **standardisation (z-score)** and **one-hot encoding** of categorical variables.

### 1 · K-Nearest Neighbours (`KNN_Model.ows`)

Five configurations tested to compare the effect of k, distance metric, and weighting:

| Variant | k | Distance Metric | Weighting |
|---|---|---|---|
| kNN 1 | 5 | Euclidean | Uniform |
| kNN 2 | 3 | Euclidean | Distance |
| kNN 3 | 7 | Manhattan | Uniform |
| kNN 4 | 10 | Euclidean | Distance |
| kNN 5 | 15 | Manhattan | Uniform |

---

### 2 · Logistic Regression (`Logistic_Regression_Model.ows`)

Three regularisation strategies compared:

| Variant | Penalty | Regularisation Strength (C) |
|---|---|---|
| Lasso 1 | L1 (Lasso) | 100.0 (low regularisation) |
| Ridge L2 | L2 (Ridge) | 100.0 (low regularisation) |
| None | No penalty | — |

Coefficient tables exported for each variant to inspect feature importance.

---

### 3 · Neural Networks (`Neural_Networks_Model.ows`)

Five multi-layer perceptron architectures tested:

| Variant | Hidden Layers | Activation | Solver | Max Iterations |
|---|---|---|---|---|
| NN1 | (10,) | ReLU | Adam | 200 |
| NN2 | (25, 10) | ReLU | Adam | 500 |
| NN3 | (25, 10, 5) | ReLU | SGD | 500 |
| NN4 | (50, 25, 10) | tanh | Adam | 1,000 |
| NN5 | (25, 10) | Logistic | SGD | 500 |

---

### 4 · Random Forest (`Random_Forest_Model.ows`)

Five configurations covering a range of tree depths and ensemble sizes:

| Variant | Trees | Max Depth | Min Samples Split | Max Features |
|---|---|---|---|---|
| RF1 | 200 | Unlimited | 5 | Auto |
| RF2 | 500 | 10 | 5 | Auto |
| RF3 | 300 | 15 | 5 | 12 |
| RF4 | 500 | Unlimited | 10 | Auto |
| RF5 | 2,000 | 20 | 10 | 24 |

---

### 5 · Support Vector Machine (`SVM_Model.ows`)

Four kernel types compared, all with C = 20.0:

| Variant | Kernel | C |
|---|---|---|
| SVM | Sigmoid | 20.0 |
| SVM (1) | RBF | 20.0 |
| SVM (2) | Polynomial (degree 3) | 20.0 |
| SVM (3) | Linear | 20.0 |

---

### 6 · Final Comparison Workflow (`Final_Model_Workflow.ows`)

The best-performing variant from each algorithm was brought together in a single workflow for side-by-side comparison, with added explainability components:

| Component | Purpose |
|---|---|
| kNN 4 (k=10, Euclidean, Distance) | Best KNN variant |
| Logistic Regression (no penalty) | Best LR variant |
| NN3 (25-10-5, ReLU, SGD) | Best NN variant |
| RF5 (2000 trees, depth 20) | Best RF variant |
| SVM (RBF kernel) | Best SVM variant |
| Feature Statistics | Dataset summary and distributions |
| Feature Importance | RF-based feature ranking |
| Explain Model (SHAP) | Global model explanation |
| Explain Prediction (SHAP) | Per-prediction explanation |
| ICE Plots | Individual conditional expectation curves |

---

## 📊 Power BI Dashboard

**Files:** `PowerBI/Marketing_Dashboard_V1.pbix` · `PowerBI/Marketing_Dashboard_V2.pbix`

The interactive dashboard covers:
- **Campaign performance overview** — conversion rates by channel, type, and spend
- **Customer demographics** — age groups, gender split, income bands
- **Engagement metrics** — click-through rates, website visits, time on site, email engagement
- **Loyalty analysis** — loyalty points distribution vs. conversion outcome
- **Comparative KPIs** — side-by-side channel and campaign type effectiveness

---

## 📁 File Summary

| Folder | File(s) | Description |
|---|---|---|
| `Dataset/` | `digital_marketing_campaign_dataset.csv` | Full dataset — 8,000 records, 20 columns |
| `Models_Orange/` | `KNN_Model.ows` | KNN workflow with 5 variants |
| `Models_Orange/` | `Logistic_Regression_Model.ows` | Logistic Regression workflow with L1, L2, no-penalty |
| `Models_Orange/` | `Neural_Networks_Model.ows` | Neural Network workflow with 5 architectures |
| `Models_Orange/` | `Random_Forest_Model.ows` | Random Forest workflow with 5 configurations |
| `Models_Orange/` | `SVM_Model.ows` | SVM workflow with 4 kernel types |
| `Models_Orange/` | `Final_Model_Workflow.ows` | Combined best-model comparison + explainability |
| `PowerBI/` | `Marketing_Dashboard_V1.pbix` | Power BI dashboard version 1 |
| `PowerBI/` | `Marketing_Dashboard_V2.pbix` | Power BI dashboard version 2 (final) |
| `Reports/` | `Project_Report.docx` | Initial project report |
| `Reports/` | `Final_Project_Report.docx` | Final submitted project report |
| `Reports/` | `Feedback_Report.docx` | Supervisor / reviewer feedback |
| `Presentation/` | `Final_Presentation_V1.pptx` | Presentation version 1 |
| `Presentation/` | `Final_Presentation_V2.pptx` | Final submitted presentation |

---

## 🙏 Acknowledgements

Special thanks to my mentors and reviewers who guided me throughout this project.

---

## 🔗 Contact

**Dixit Mukeshkumar Patel**  
📧 dixitmpatel14@gmail.com  
📍 Perth, WA, Australia

---

> *This project is part of my personal portfolio and demonstrates skills in data analytics, machine learning, business intelligence, and data-driven decision making.*
