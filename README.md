# Employee Well-Being Analytics & Interactive Dashboard

[Español](README_ES.md) | **English**

Interactive data analytics project focused on workplace well-being, burnout, job satisfaction, leadership, psychosocial risk, and turnover intention.

Built with **Python, Pandas, Plotly, Streamlit, Statsmodels, and Scikit-learn**.

> This project was developed as an academic Data Science case study at Universidad de La Sabana. It is presented here as a portfolio project to demonstrate data analysis, statistical modeling, visualization, clustering, and dashboard development skills.

## Business Problem

Employee well-being is influenced by multiple organizational and psychosocial factors. Looking at these variables independently can make it difficult to identify the employees or groups that may require attention.

The objective of this project is to transform employee survey data into an interactive analytical tool that helps explore:

- Workplace well-being
- Burnout and exhaustion
- Job satisfaction
- Leadership
- Psychosocial risk dimensions
- Turnover intention
- Employee risk profiles

## Dataset

The analysis uses a dataset of **400 employees** containing demographic information and **15 psychosocial dimensions**.

The dimensions analyzed include well-being, burnout, exhaustion, somatization, job satisfaction, turnover intention, leadership commitment, time pressure, coworker support, role conflict, change management, organizational mental health, role clarity, and work-family conflict variables.

## Analytical Workflow

The project follows an end-to-end analytics workflow:

1. Data loading and quality checks
2. Data cleaning and preparation
3. Exploratory Data Analysis (EDA)
4. Demographic and psychosocial segmentation
5. Correlation analysis
6. Linear regression analysis
7. K-Means clustering
8. Risk-profile interpretation
9. Interactive dashboard development with Streamlit

## Key Results

### Burnout and related risk factors

Burnout shows strong positive relationships with other psychosocial risk dimensions:

- **Burnout ↔ Exhaustion:** r = 0.658
- **Burnout ↔ Somatization:** r = 0.610
- **Exhaustion ↔ Somatization:** r = 0.554

These relationships suggest that burnout should be analyzed together with physical and emotional exhaustion indicators rather than as an isolated dimension.

### Leadership and employee experience

Leadership is associated with both positive and negative employee outcomes:

- **Leadership ↔ Job Satisfaction:** r = 0.487
- **Leadership ↔ Burnout:** r = -0.533

Higher leadership scores are therefore associated with greater job satisfaction and lower burnout levels in this dataset.

### Turnover intention

A linear regression was used to analyze the relationship between job satisfaction and turnover intention.

- **R²:** 0.704
- **Slope:** -1.150
- **Intercept:** 9.430
- **p-value:** 2.28e-107

The model identifies a strong negative association: higher job satisfaction is associated with lower turnover intention. This is an observational analysis and should not be interpreted as proof of causality.

### Employee segmentation

K-Means clustering was used to identify **three employee profiles**:

| Profile | Employees |
|---|---:|
| Stable profile | 112 |
| High-risk profile | 79 |
| Moderate-risk profile | 209 |

The segmentation provides a practical way to compare groups and prioritize exploratory intervention analysis.

## Interactive Dashboard

The Streamlit application organizes the analysis into multiple interactive sections:

| Section | Analysis |
|---|---|
| Demographic Profile | Gender, work modality, sector and age |
| Risk Ranking | Comparison of psychosocial dimensions |
| Well-Being by Group | Analysis by role, sector and modality |
| Burnout & Exhaustion | Relationships between burnout-related variables |
| Leadership | Leadership, satisfaction and burnout analysis |
| Turnover Analysis | Statistical relationship between satisfaction and turnover intention |
| Employee Profiles | K-Means clustering and profile comparison |
| Intervention Matrix | Global risk visualization and prioritization |

The dashboard includes interactive filters and visualizations designed to make the statistical results easier to explore and interpret.

## Technologies

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Statsmodels
- Scikit-learn
- Jupyter Notebook
- OpenPyXL

## Repository Structure

```text
.
├── README.md
├── README_ES.md
├── app.py
├── crear_app.py
├── requirements.txt
├── data/
│   └── bienestar_laboral_limpio.xlsx
└── notebook/
    └── analisis.ipynb
```

The structure above reflects the repository in its current state. File and repository names may be standardized as part of future portfolio improvements.

## Run Locally

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd <repository-folder>
```

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv venv
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

## Skills Demonstrated

`Data Analysis` · `Python` · `Pandas` · `Exploratory Data Analysis` · `Statistical Analysis` · `Linear Regression` · `K-Means Clustering` · `Data Visualization` · `Streamlit` · `Dashboard Development`

## Author

**David Santiago Cifuentes Grimaldo**  
Data Science Student  
Universidad de La Sabana
