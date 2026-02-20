# ✈️ SkyPrice Analytics | Flight Price Intelligence Platform

[![Live Demo](https://img.shields.io/badge/Live_App-View_Dashboard-239120?style=for-the-badge&logo=streamlit)](https://flightpriceanalysis-001.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)

> **An enterprise-grade analytics platform** that transforms flight pricing data into actionable insights using advanced ML algorithms and interactive visualizations.

**SkyPrice Analytics** empowers airlines, travel agencies, and data enthusiasts to explore historical flight data, identify pricing patterns, and predict future ticket prices with machine learning—all through an intuitive web interface.

## 👉 **[Access the Live Application Here](https://flightpriceanalysis-001.streamlit.app/)**

---
 

##  Key Features

| Feature | Description |
|---------|-------------|
|  **Executive Summary** | High-level KPIs, market insights, average price by airline, and price distribution charts |
|  **Feature Analysis** | Deep dive into Airlines, Source, Destination, Stops with market volume and price variance box plots |
|  **Trends & Correlations** | Time-series analysis for monthly/weekly trends, flight duration impact, and correlation heatmaps |
|  **ML Price Predictor** | Random Forest Regressor predicting flight prices based on Airline, Source, Destination, Stops, Duration |
|  **Data Explorer** | Interactive dataframe viewer with real-time search, filtering, statistics, and CSV export |

---

##  Technology Stack

<table>
<tr>
<td>

**Category** | **Technology**
--- | ---
Frontend | Streamlit
Data Processing | Pandas, NumPy
Visualization | Plotly Express & Graph Objects
Machine Learning | Scikit-Learn
UI/UX | Custom CSS, Google Fonts

</td>
</tr>
</table>

---

##  Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/pranay-surya/Flight_Price_Analysis.git
cd Flight_Price_Analysis

# 2. Create virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
