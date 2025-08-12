# UBC Housing Analysis & Rent Prediction

## Overview

During my long wait on the UBC year-round housing waitlist, I became genuinely curious about the housing situation both at UBC and across Vancouver. I wanted to understand why the waitlist was so long and whether student housing capacity was keeping pace with enrollment growth. This project is my attempt to explore that question rigorously and to provide practical tools that can help students navigate Vancouver’s challenging rental market.

The project unfolds in two phases:

1. Analyzing whether UBC’s housing infrastructure has kept pace with increasing enrollment.
2. Predicting off-campus rent trends in Vancouver using machine learning, supporting informed housing decisions.

---

## Problem Statement

### Phase 1: UBC Student Housing Capacity vs. Enrollment Growth

- UBC has seen rapid growth in international student enrollment over the past decade.
- Despite efforts to expand housing, waitlists remain long, raising questions about whether housing infrastructure matches enrollment growth.
- Public data is fragmented across multiple reports and formats, complicating analysis.

### Solution: Phase 1

- Gathered and processed historical data from 2012 to 2023 on international student enrollment and on-campus housing capacity, sourced from official UBC enrollment reports and housing statistics.
- Used R and Python to perform exploratory data analysis, visualizing trends in student enrollment and available residence beds over time.
- Calculated year-over-year growth rates to normalize and directly compare changes in enrollment and housing capacity.
- Conducted a one-tailed paired t-test to statistically assess if enrollment growth significantly exceeded housing growth.
- Results showed that international student enrollment has grown significantly faster than on-campus housing capacity, explaining persistent waitlist challenges.

---

### Phase 2: Vancouver Rent Trend Analysis & Prediction

- Off-campus housing in Vancouver is highly competitive and costly, with rents varying by neighborhood and unit type.
- Publicly accessible, detailed rent trend analysis and prediction tools are scarce.

### Solution: Phase 2

- Collected rental market data for Vancouver (2020–2024) from the Canada Mortgage and Housing Corporation (CMHC).
- Conducted exploratory data analysis to understand rent growth patterns by neighborhood and unit type, visualizing key trends over time.
- Developed and compared several predictive models — Linear Regression, Decision Tree, Random Forest, and XGBoost — using features such as year, room type, and zone.
- Selected a hybrid modeling approach that combines Linear Regression to capture overall trends and XGBoost to model residual errors, improving prediction accuracy.
- Exported the trained models using Joblib for later deployment.
- Developed a user-friendly frontend using HTML and CSS for easy input of parameters like year, room type, and zone.
- Implemented a Python Flask backend to handle model predictions and serve the frontend interface.
- The web app is publicly accessible at: [https://ubc-housing-analysis.onrender.com](https://ubc-housing-analysis.onrender.com)

---

## Technologies Used

- **Data Collection & Analysis:** R (`tidyverse`, `ggplot2`, `broom`), Python (`pandas`, `matplotlib`, `scikit-learn`, `xgboost`)
- **Modeling:** Linear Regression, Decision Tree, Random Forest, XGBoost, hybrid modeling approach
- **Web Development:** Python Flask backend, HTML/CSS frontend
- **Deployment:** Render.com

---

## Data Sources

- **UBC Enrolment Reports** and **Student Housing Facts & Figures** from official UBC websites
- Archived charts, PDFs, and screenshots (available in `data/` and `raw/` folders)
- **Canada Mortgage and Housing Corporation (CMHC)** Rental Market Data for Vancouver (2020–2024)

---

## Usage Notice

This repository contains proprietary code and analysis developed by Chaitanya Thakral.  
You are welcome to explore and learn from this work, but please **do not copy, redistribute, or use the code and data for commercial purposes without explicit permission**.  
For inquiries or collaboration, please contact me directly at cthakral6@gmail.com

---
## Project Structure (Summary)

project-root/
├── app.py # Flask backend server
├── data/ # Raw and cleaned datasets for analysis
├── notebooks/ # Jupyter notebooks for Phase 1 & Phase 2 analysis
├── models/ # Serialized trained models
├── static/ # CSS, images for frontend
├── templates/ # HTML templates for Flask
└── README.md # This file

