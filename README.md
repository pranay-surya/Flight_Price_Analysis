# ✈️ SkyPrice Analytics | Flight Price Intelligence

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)

**SkyPrice Analytics** is an interactive, enterprise-grade data visualization and machine learning dashboard built with Streamlit. It enables users to perform in-depth Exploratory Data Analysis (EDA) on historical flight data, uncover market trends, and utilize a built-in Random Forest regression model to predict future flight ticket prices.

---

##  Key Features

* **Executive Summary:** High-level KPIs, market insights, average price by airline, and price distribution charts.
* **Feature Analysis:** Deep dive into categorical features (Airlines, Source, Destination, Stops) with market volume and price variance box plots.
* **Trends & Correlations:** Time-series analysis for monthly/weekly trends, flight duration impact, and numerical correlation heatmaps.
* **ML Price Predictor:** A built-in Random Forest Regressor model that predicts flight prices based on user-selected parameters (Airline, Source, Destination, Stops, Duration).
* **Data Explorer:** Interactive dataframe viewer with real-time search, filtering, detailed column statistics, and one-click CSV export functionality.

---

##  Technology Stack

* **Frontend framework:** Streamlit
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization:** Plotly (Express & Graph Objects)
* **Machine Learning:** Scikit-Learn (RandomForestRegressor, LabelEncoder)
* **UI/UX Design:** Custom CSS, Google Fonts (Inter, Poppins), FontAwesome Icons

---

## Project Structure

```text
skyprice-analytics/
│
├── app.py                  # Main Streamlit application code
├── requirements.txt        # Python dependencies for deployment
├── flight_price.xlsx       # Dataset (Ensure this is in the root folder)
└── README.md               # Project documentation
