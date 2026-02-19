import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="SkyPrice Analytics | Flight Price Intelligence",
    page_icon="airplane",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS for White Background and FontAwesome CDN
st.markdown("""
<style>
    /* Import Google Fonts and Font Awesome CDN */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Root Variables */
    :root {
        --primary-blue: #1e40af;
        --primary-blue-light: #3b82f6;
        --primary-blue-dark: #1e3a8a;
        --secondary-teal: #0d9488;
        --secondary-teal-light: #14b8a6;
        --accent-orange: #ea580c;
        --accent-amber: #d97706;
        --text-dark: #1e293b;
        --text-medium: #475569;
        --text-light: #64748b;
        --bg-light: #f8fafc;
        --bg-card: #ffffff;
        --border-light: #e2e8f0;
        --border-medium: #cbd5e1;
        --success: #059669;
        --warning: #d97706;
        --error: #dc2626;
    }
    
    /* Main App Styling */
    .main {
        background-color: #ffffff;
    }
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #ffffff;
    }
    
    /* Sidebar Styling - Dark Blue Theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 50%, #2563eb 100%);
        padding: 1.5rem 1rem;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        color: rgba(255,255,255,0.9) !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #e0e7ff !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stRadio label span {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 10px;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.2);
    }
    
    /* Header Styling - Blue Gradient */
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #0ea5e9 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(30, 64, 175, 0.25);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
    }
    
    .main-header h1 {
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.05rem;
        position: relative;
        z-index: 1;
        margin: 0;
    }
    
    /* Metric Cards - Clean White with Colored Accents */
    .metric-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-color: #3b82f6;
    }
    
    .metric-card.blue::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #1e40af 0%, #3b82f6 100%);
    }
    
    .metric-card.teal::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #0d9488 0%, #14b8a6 100%);
    }
    
    .metric-card.orange::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #ea580c 0%, #f97316 100%);
    }
    
    .metric-card.slate::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #334155 0%, #64748b 100%);
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        color: inherit;
    }
    
    .metric-value {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0.5rem 0;
    }
    
    .metric-value.blue { color: #1e40af; }
    .metric-value.teal { color: #0d9488; }
    .metric-value.orange { color: #ea580c; }
    .metric-value.slate { color: #334155; }
    
    .metric-label {
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(90deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 0.9rem 1.25rem;
        border-radius: 10px;
        margin: 1.75rem 0 1.25rem 0;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.05rem;
        box-shadow: 0 3px 12px rgba(30, 41, 59, 0.2);
    }
    
    /* Chart Container */
    .chart-container {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.25rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        margin-bottom: 1.25rem;
        border: 1px solid #e2e8f0;
    }
    
    /* Info Cards */
    .info-card {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 10px;
        padding: 1.25rem;
        margin: 1rem 0;
    }
    
    .info-card h4 {
        color: #1e40af;
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
    }
    
    .info-card p, .info-card li {
        color: #334155;
        margin: 0;
    }
    
    .success-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 4px solid #059669;
        border-radius: 10px;
        padding: 1.25rem;
        margin: 1rem 0;
    }
    
    .success-card h4 { color: #047857; }
    .success-card p { color: #064e3b; }
    
    .warning-card {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 4px solid #d97706;
        border-radius: 10px;
        padding: 1.25rem;
        margin: 1rem 0;
    }
    
    .warning-card h4 { color: #b45309; }
    .warning-card p { color: #78350f; }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 1.75rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(30, 64, 175, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 64, 175, 0.4);
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Form Styling */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        background: #ffffff;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        background: #3b82f6;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f1f5f9;
        padding: 0.4rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.6rem 1.25rem;
        font-weight: 500;
        color: #475569;
        background: transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e2e8f0;
        color: #1e293b;
    }
    
    .stTabs [aria-selected="true"] {
        background: #1e40af !important;
        color: white !important;
    }
    
    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #cbd5e1, transparent);
        border: none;
        margin: 1.75rem 0;
        border-radius: 2px;
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        color: #1e293b;
        font-weight: 500;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f1f5f9;
        border-color: #3b82f6;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.75rem;
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 2.5rem;
        border-top: 1px solid #e2e8f0;
        background: #f8fafc;
        border-radius: 12px;
    }
    
    .footer strong {
        color: #1e40af;
    }
    
    /* Prediction Result Card */
    .prediction-result {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #0ea5e9 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 10px 40px rgba(30, 64, 175, 0.3);
    }
    
    .prediction-result h2 {
        color: white;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 0.5rem;
        font-size: 1.3rem;
        font-weight: 500;
    }
    
    .prediction-price {
        font-size: 2.75rem;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Feature Card */
    .feature-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
    }
    
    .feature-card h4 {
        color: #1e293b;
        margin: 0 0 0.75rem 0;
        font-size: 0.95rem;
        font-weight: 600;
    }
    
    /* Stats Box */
    .stats-box {
        background: #f8fafc;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        border: 1px solid #e2e8f0;
        margin: 0.5rem 0;
    }
    
    .stats-box .label {
        color: #64748b;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.25rem;
    }
    
    .stats-box .value {
        color: #1e293b;
        font-size: 1.4rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
    }
    
   
    
    /* Metric Component Override */
    [data-testid="stMetricValue"] {
        color: #1e293b;
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stMetricLabel"] {
        color: #64748b;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
        border-radius: 10px;
    }
    
    /* Radio buttons in main area */
    .stRadio > label {
        color: #1e293b !important;
    }
    
    /* Checkbox */
    .stCheckbox label span {
        color: #1e293b;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        box-shadow: 0 4px 14px rgba(13, 148, 136, 0.3);
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%);
        box-shadow: 0 6px 20px rgba(13, 148, 136, 0.4);
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 10px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# Color Palette for Charts
CHART_COLORS = {
    'primary': '#1e40af',
    'secondary': '#3b82f6',
    'tertiary': '#0ea5e9',
    'teal': '#0d9488',
    'teal_light': '#14b8a6',
    'orange': '#ea580c',
    'amber': '#d97706',
    'slate': '#475569',
    'success': '#059669',
    'sequential': ['#1e3a8a', '#1e40af', '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd'],
    'categorical': ['#1e40af', '#0d9488', '#ea580c', '#7c3aed', '#059669', '#dc2626', '#d97706', '#0284c7']
}

# Helper Functions
def duration_to_minutes(duration):
    if pd.isna(duration):
        return 0
    hours = 0
    minutes = 0
    parts = str(duration).split()
    for part in parts:
        if 'h' in part:
            hours = int(part.replace('h', ''))
        elif 'm' in part:
            minutes = int(part.replace('m', ''))
    return (hours * 60) + minutes

def create_metric_card(icon, value, label, color_class="blue"):
    return f"""
    <div class="metric-card {color_class}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value {color_class}">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

def create_section_header(icon, title):
    return f"""
    <div class="section-header">
        <span>{icon}</span>
        <span>{title}</span>
    </div>
    """

def create_stats_box(label, value):
    return f"""
    <div class="stats-box">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
    </div>
    """

@st.cache_data
def load_and_preprocess():
    try:
        df = pd.read_excel('flight_price.xlsx')
        
        if 'Date_of_Journey' in df.columns:
            df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True)
            df['Day'] = df['Date_of_Journey'].dt.day
            df['Month'] = df['Date_of_Journey'].dt.month_name()
            df['Weekday'] = df['Date_of_Journey'].dt.day_name()
        
        if 'Duration' in df.columns:
            df['Duration'] = df['Duration'].apply(duration_to_minutes)
        
        if 'Total_Stops' in df.columns:
            df['Stops_Num'] = df['Total_Stops'].replace({
                'non-stop': 0, '1 stop': 1, '2 stops': 2, '3 stops': 3, '4 stops': 4
            }).astype(float)
            
        return df
    except Exception as e:
        st.error(f"Data loading error: {e}")
        return None

@st.cache_resource
def train_prediction_model(df):
    model_df = df[['Airline', 'Source', 'Destination', 'Total_Stops', 'Duration', 'Price']].dropna()
    
    encoders = {}
    categorical_cols = ['Airline', 'Source', 'Destination', 'Total_Stops']
    
    for col in categorical_cols:
        le = LabelEncoder()
        model_df[col] = le.fit_transform(model_df[col].astype(str))
        encoders[col] = le
        
    X = model_df.drop('Price', axis=1)
    y = model_df['Price']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X, y)
    
    return model, encoders

# Load Data
df = load_and_preprocess()

if df is not None:
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0 1.5rem 0;">
            <h1 style="color: white; font-family: 'Poppins', sans-serif; font-size: 1.6rem; margin: 0;">
                <i class="fa-solid fa-plane"></i> SkyPrice
            </h1>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-top: 0.4rem;">
                Flight Price Intelligence
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        <p style="color: rgba(255,255,255,0.7); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.75rem;">
            <i class="fa-solid fa-location-dot"></i> Navigation
        </p>
        """, unsafe_allow_html=True)
        
        page = st.radio(
            "",
            ["Executive Summary", "Feature Analysis", "Trends & Correlations", "Price Predictor", "Data Explorer"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        st.markdown("""
        <p style="color: rgba(255,255,255,0.7); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.75rem;">
            <i class="fa-solid fa-sliders"></i> Global Filters
        </p>
        """, unsafe_allow_html=True)
        
        selected_airlines = st.multiselect(
            "Filter by Airline",
            options=sorted(df['Airline'].unique()),
            default=list(df['Airline'].unique()),
            help="Select airlines to include in analysis"
        )
        
        if 'Source' in df.columns:
            selected_sources = st.multiselect(
                "Filter by Source",
                options=sorted(df['Source'].unique()),
                default=list(df['Source'].unique())
            )
        else:
            selected_sources = None
        
        st.markdown("---")
        
        st.markdown("""
        <p style="color: rgba(255,255,255,0.7); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.75rem;">
            <i class="fa-solid fa-chart-line"></i> Quick Stats
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 0.9rem; border-radius: 10px; margin-bottom: 0.5rem;">
            <p style="color: rgba(255,255,255,0.8); font-size: 0.75rem; margin: 0; text-transform: uppercase;">Total Records</p>
            <p style="color: white; font-size: 1.4rem; font-weight: 600; margin: 0.25rem 0 0 0;">{len(df):,}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 0.9rem; border-radius: 10px;">
            <p style="color: rgba(255,255,255,0.8); font-size: 0.75rem; margin: 0; text-transform: uppercase;">Airlines</p>
            <p style="color: white; font-size: 1.4rem; font-weight: 600; margin: 0.25rem 0 0 0;">{df['Airline'].nunique()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Apply Filters
    filtered_df = df.copy()
    if selected_airlines:
        filtered_df = filtered_df[filtered_df['Airline'].isin(selected_airlines)]
    if selected_sources and 'Source' in df.columns:
        filtered_df = filtered_df[filtered_df['Source'].isin(selected_sources)]

    # ==================== PAGES ====================
    
    if "Executive Summary" in page:
        st.markdown("""
        <div class="main-header">
            <h1><i class="fa-solid fa-plane-departure"></i> Flight Price Intelligence Report</h1>
            <p>Comprehensive analytical overview of flight pricing patterns and market trends</p>
        </div>
        """, unsafe_allow_html=True)
        
        # KPI Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card(
                '<i class="fa-solid fa-table-list"></i>', f"{len(filtered_df):,}", "Total Flight Records", "blue"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                '<i class="fa-solid fa-money-bill-wave"></i>', f"₹{int(filtered_df['Price'].mean()):,}", "Average Price", "teal"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(
                '<i class="fa-solid fa-chart-line"></i>', f"₹{int(filtered_df['Price'].std()):,}", "Price Std Dev", "orange"
            ), unsafe_allow_html=True)
        
        with col4:
            unique_routes = filtered_df.groupby(['Source', 'Destination']).ngroups if 'Source' in filtered_df.columns and 'Destination' in filtered_df.columns else 0
            st.markdown(create_metric_card(
                '<i class="fa-solid fa-route"></i>', f"{unique_routes}", "Unique Routes", "slate"
            ), unsafe_allow_html=True)
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown(create_section_header('<i class="fa-solid fa-lightbulb"></i>', "Key Market Insights"), unsafe_allow_html=True)
            st.markdown("""
            <div class="info-card">
                <h4><i class="fa-solid fa-thumbtack"></i> Market Overview</h4>
                <ul style="line-height: 1.9; padding-left: 1.2rem;">
                    <li><strong>Market Volume:</strong> Total flights operated across selected airlines</li>
                    <li><strong>Pricing Variance:</strong> Standard deviation indicates market volatility</li>
                    <li><strong>Route Diversity:</strong> Unique origin-destination pairs in service</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(create_section_header('<i class="fa-solid fa-trophy"></i>', "Top Airlines by Avg Price"), unsafe_allow_html=True)
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            top_airlines = filtered_df.groupby('Airline')['Price'].mean().sort_values(ascending=True).tail(6)
            fig_top = px.bar(
                x=top_airlines.values,
                y=top_airlines.index,
                orientation='h',
                labels={'x': 'Average Price (₹)', 'y': ''},
                color=top_airlines.values,
                color_continuous_scale=[[0, '#93c5fd'], [0.5, '#3b82f6'], [1, '#1e3a8a']]
            )
            fig_top.update_layout(
                template="plotly_white",
                showlegend=False,
                height=280,
                margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_showscale=False,
                font=dict(family="Inter", color="#1e293b")
            )
            st.plotly_chart(fig_top, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_b:
            st.markdown(create_section_header('<i class="fa-solid fa-chart-column"></i>', "Price Distribution"), unsafe_allow_html=True)
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig_hist = px.histogram(
                filtered_df, 
                x='Price',
                nbins=40,
                color_discrete_sequence=[CHART_COLORS['primary']]
            )
            fig_hist.update_layout(
                template="plotly_white",
                height=320,
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis_title="Price (₹)",
                yaxis_title="Frequency",
                font=dict(family="Inter", color="#1e293b")
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Quick stats
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.markdown(create_stats_box("Min Price", f"₹{int(filtered_df['Price'].min()):,}"), unsafe_allow_html=True)
            with col_s2:
                st.markdown(create_stats_box("Median", f"₹{int(filtered_df['Price'].median()):,}"), unsafe_allow_html=True)
            with col_s3:
                st.markdown(create_stats_box("Max Price", f"₹{int(filtered_df['Price'].max()):,}"), unsafe_allow_html=True)
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
        # Additional Stats Row
        st.markdown(create_section_header('<i class="fa-solid fa-clipboard-list"></i>', "Statistical Summary"), unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""<div class="feature-card"><h4><i class="fa-solid fa-money-bill-wave"></i> Price Statistics</h4></div>""", unsafe_allow_html=True)
            st.metric("Average Price", f"₹{int(filtered_df['Price'].mean()):,}")
            st.metric("Price Range", f"₹{int(filtered_df['Price'].max() - filtered_df['Price'].min()):,}")
        
        with col2:
            st.markdown("""<div class="feature-card"><h4><i class="fa-solid fa-stopwatch"></i> Duration Stats</h4></div>""", unsafe_allow_html=True)
            if 'Duration' in filtered_df.columns:
                st.metric("Avg Duration", f"{int(filtered_df['Duration'].mean())} min")
                st.metric("Max Duration", f"{int(filtered_df['Duration'].max())} min")
        
        with col3:
            st.markdown("""<div class="feature-card"><h4><i class="fa-solid fa-route"></i> Route Analysis</h4></div>""", unsafe_allow_html=True)
            st.metric("Total Airlines", filtered_df['Airline'].nunique())
            if 'Source' in filtered_df.columns:
                st.metric("Source Cities", filtered_df['Source'].nunique())

    elif "Feature Analysis" in page:
        st.markdown("""
        <div class="main-header">
            <h1><i class="fa-solid fa-chart-pie"></i> Categorical Feature Analysis</h1>
            <p>Distribution of flights and price variance across all primary features</p>
        </div>
        """, unsafe_allow_html=True)
        
        features = [f for f in ['Airline', 'Source', 'Destination', 'Total_Stops', 'Additional_Info'] if f in filtered_df.columns]
        feature_icons = {
            'Airline': '<i class="fa-solid fa-building"></i>', 
            'Source': '<i class="fa-solid fa-plane-departure"></i>', 
            'Destination': '<i class="fa-solid fa-plane-arrival"></i>', 
            'Total_Stops': '<i class="fa-solid fa-rotate"></i>', 
            'Additional_Info': '<i class="fa-solid fa-circle-info"></i>'
        }
        
        for feature in features:
            icon = feature_icons.get(feature, '<i class="fa-solid fa-chart-column"></i>')
            st.markdown(create_section_header(icon, f"{feature} Analysis"), unsafe_allow_html=True)
            
            col_a, col_b = st.columns([1, 1.2])
            
            with col_a:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                counts = filtered_df[feature].value_counts().reset_index()
                counts.columns = [feature, 'Volume']
                
                fig_bar = px.bar(
                    counts.head(10), 
                    x=feature, 
                    y='Volume',
                    color='Volume',
                    color_continuous_scale=[[0, '#dbeafe'], [0.5, '#3b82f6'], [1, '#1e3a8a']],
                    title="Market Volume Distribution"
                )
                fig_bar.update_layout(
                    template="plotly_white",
                    showlegend=False,
                    coloraxis_showscale=False,
                    height=380,
                    title_font=dict(size=14, color='#1e293b'),
                    margin=dict(l=10, r=10, t=40, b=10),
                    font=dict(family="Inter", color="#1e293b")
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_b:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                fig_box = px.box(
                    filtered_df, 
                    x=feature, 
                    y='Price',
                    color=feature,
                    color_discrete_sequence=CHART_COLORS['categorical'],
                    title="Price Distribution"
                )
                fig_box.update_layout(
                    template="plotly_white",
                    showlegend=False,
                    height=380,
                    title_font=dict(size=14, color='#1e293b'),
                    margin=dict(l=10, r=10, t=40, b=10),
                    font=dict(family="Inter", color="#1e293b")
                )
                st.plotly_chart(fig_box, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with st.expander(f"View {feature} Statistics"):
                stats_df = filtered_df.groupby(feature)['Price'].agg(['mean', 'median', 'std', 'min', 'max', 'count'])
                stats_df.columns = ['Avg Price', 'Median', 'Std Dev', 'Min', 'Max', 'Count']
                stats_df = stats_df.round(2).sort_values('Avg Price', ascending=False)
                st.dataframe(stats_df, use_container_width=True)
            
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    elif "Trends & Correlations" in page:
        st.markdown("""
        <div class="main-header">
            <h1><i class="fa-solid fa-arrow-trend-down"></i> Trends & Correlations</h1>
            <p>Time-series analysis and numerical feature correlations</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Temporal Trends", "Duration Analysis", "Correlation Matrix"])
        
        with tab1:
            st.markdown(create_section_header('<i class="fa-solid fa-calendar-days"></i>', "Pricing Trends Over Time"), unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'Month' in filtered_df.columns:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                                  'July', 'August', 'September', 'October', 'November', 'December']
                    available_months = [m for m in month_order if m in filtered_df['Month'].unique()]
                    
                    if available_months:
                        monthly = filtered_df.groupby('Month')['Price'].agg(['mean', 'median']).reindex(available_months).reset_index()
                        
                        fig_month = go.Figure()
                        fig_month.add_trace(go.Scatter(
                            x=monthly['Month'], y=monthly['mean'],
                            mode='lines+markers',
                            name='Average',
                            line=dict(color=CHART_COLORS['primary'], width=3),
                            marker=dict(size=10)
                        ))
                        fig_month.add_trace(go.Scatter(
                            x=monthly['Month'], y=monthly['median'],
                            mode='lines+markers',
                            name='Median',
                            line=dict(color=CHART_COLORS['teal'], width=3, dash='dash'),
                            marker=dict(size=10)
                        ))
                        fig_month.update_layout(
                            title="Monthly Price Trend",
                            template="plotly_white",
                            height=380,
                            legend=dict(orientation="h", yanchor="bottom", y=1.02),
                            font=dict(family="Inter", color="#1e293b")
                        )
                        st.plotly_chart(fig_month, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                if 'Weekday' in filtered_df.columns:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    available_days = [d for d in day_order if d in filtered_df['Weekday'].unique()]
                    
                    if available_days:
                        weekly = filtered_df.groupby('Weekday')['Price'].mean().reindex(available_days).reset_index()
                        
                        fig_week = px.bar(
                            weekly, x='Weekday', y='Price',
                            color='Price',
                            color_continuous_scale=[[0, '#d1fae5'], [0.5, '#14b8a6'], [1, '#0f766e']],
                            title="Average Price by Day of Week"
                        )
                        fig_week.update_layout(
                            template="plotly_white",
                            height=380,
                            coloraxis_showscale=False,
                            font=dict(family="Inter", color="#1e293b")
                        )
                        st.plotly_chart(fig_week, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Heatmap
            if 'Weekday' in filtered_df.columns and 'Airline' in filtered_df.columns:
                st.markdown(create_section_header('<i class="fa-regular fa-calendar"></i>', "Price Heatmap: Airline × Weekday"), unsafe_allow_html=True)
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                
                pivot = filtered_df.pivot_table(values='Price', index='Airline', columns='Weekday', aggfunc='mean')
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                pivot = pivot.reindex(columns=[d for d in day_order if d in pivot.columns])
                
                fig_heatmap = px.imshow(
                    pivot,
                    color_continuous_scale=[[0, '#eff6ff'], [0.25, '#93c5fd'], [0.5, '#3b82f6'], [0.75, '#1e40af'], [1, '#1e3a8a']],
                    aspect='auto',
                    labels=dict(color="Avg Price")
                )
                fig_heatmap.update_layout(
                    template="plotly_white",
                    height=450,
                    font=dict(family="Inter", color="#1e293b")
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown(create_section_header('<i class="fa-solid fa-stopwatch"></i>', "Duration vs Price Analysis"), unsafe_allow_html=True)
            
            if 'Duration' in filtered_df.columns:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                fig_scatter = px.scatter(
                    filtered_df, 
                    x='Duration', 
                    y='Price',
                    color='Total_Stops' if 'Total_Stops' in filtered_df.columns else None,
                    opacity=0.6,
                    trendline="ols",
                    labels={'Duration': 'Duration (Minutes)', 'Price': 'Price (₹)'},
                    title="Correlation: Travel Duration vs. Ticket Price",
                    color_discrete_sequence=CHART_COLORS['categorical']
                )
                fig_scatter.update_layout(
                    template="plotly_white",
                    height=450,
                    font=dict(family="Inter", color="#1e293b")
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    filtered_df['Duration_Bin'] = pd.cut(
                        filtered_df['Duration'], 
                        bins=[0, 60, 120, 180, 300, 500, 3000],
                        labels=['<1h', '1-2h', '2-3h', '3-5h', '5-8h', '8h+']
                    )
                    duration_price = filtered_df.groupby('Duration_Bin')['Price'].mean().reset_index()
                    
                    fig_duration_bar = px.bar(
                        duration_price,
                        x='Duration_Bin',
                        y='Price',
                        color='Price',
                        color_continuous_scale=[[0, '#fed7aa'], [0.5, '#f97316'], [1, '#c2410c']],
                        title="Average Price by Duration Category"
                    )
                    fig_duration_bar.update_layout(
                        template="plotly_white",
                        height=320,
                        coloraxis_showscale=False,
                        font=dict(family="Inter", color="#1e293b")
                    )
                    st.plotly_chart(fig_duration_bar, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    if 'Total_Stops' in filtered_df.columns:
                        stops_duration = filtered_df.groupby('Total_Stops')[['Duration', 'Price']].mean().reset_index()
                        
                        fig_stops = px.scatter(
                            stops_duration,
                            x='Duration',
                            y='Price',
                            size='Price',
                            color='Total_Stops',
                            title="Stops Impact on Duration & Price",
                            size_max=40,
                            color_discrete_sequence=CHART_COLORS['categorical']
                        )
                        fig_stops.update_layout(
                            template="plotly_white",
                            height=320,
                            font=dict(family="Inter", color="#1e293b")
                        )
                        st.plotly_chart(fig_stops, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown(create_section_header('<i class="fa-solid fa-link"></i>', "Feature Correlation Analysis"), unsafe_allow_html=True)
            
            numeric_df = filtered_df.select_dtypes(include=[np.number])
            
            if not numeric_df.empty and len(numeric_df.columns) > 1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                corr = numeric_df.corr()
                
                fig_corr = go.Figure(data=go.Heatmap(
                    z=corr.values,
                    x=corr.columns,
                    y=corr.columns,
                    colorscale=[[0, '#1e3a8a'], [0.5, '#f8fafc'], [1, '#0f766e']],
                    zmin=-1, 
                    zmax=1,
                    text=corr.round(2).values,
                    texttemplate='%{text}',
                    textfont={"size": 12, "color": "#1e293b"},
                    hoverongaps=False
                ))
                fig_corr.update_layout(
                    title="Correlation Matrix (Numerical Variables)",
                    template="plotly_white",
                    height=450,
                    font=dict(family="Inter", color="#1e293b")
                )
                st.plotly_chart(fig_corr, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("""
                <div class="info-card">
                    <h4><i class="fa-solid fa-thumbtack"></i> Correlation Insights</h4>
                    <p>Values close to <strong>+1</strong> indicate strong positive correlation, 
                    while values close to <strong>-1</strong> indicate strong negative correlation.
                    Values near <strong>0</strong> suggest little to no linear relationship.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Insufficient numerical data for correlation analysis.")

    elif "Price Predictor" in page:
        st.markdown("""
        <div class="main-header">
            <h1><i class="fa-solid fa-bullseye"></i> ML Price Predictor</h1>
            <p>Estimate flight ticket prices using Random Forest regression</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Initializing prediction model..."):
            model, encoders = train_prediction_model(df)
        
        st.markdown(create_section_header('<i class="fa-solid fa-sliders"></i>', "Configure Flight Parameters"), unsafe_allow_html=True)
        
        with st.form("prediction_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="feature-card"><h4><i class="fa-solid fa-building"></i> Airline</h4></div>', unsafe_allow_html=True)
                input_airline = st.selectbox(
                    "Select Airline",
                    options=sorted(df['Airline'].dropna().unique()),
                    label_visibility="collapsed"
                )
                
                st.markdown('<div class="feature-card"><h4><i class="fa-solid fa-plane-departure"></i> Source City</h4></div>', unsafe_allow_html=True)
                input_source = st.selectbox(
                    "Select Source",
                    options=sorted(df['Source'].dropna().unique()),
                    label_visibility="collapsed"
                )
            
            with col2:
                st.markdown('<div class="feature-card"><h4><i class="fa-solid fa-plane-arrival"></i> Destination City</h4></div>', unsafe_allow_html=True)
                input_dest = st.selectbox(
                    "Select Destination",
                    options=sorted(df['Destination'].dropna().unique()),
                    label_visibility="collapsed"
                )
                
                st.markdown('<div class="feature-card"><h4><i class="fa-solid fa-rotate"></i> Total Stops</h4></div>', unsafe_allow_html=True)
                input_stops = st.selectbox(
                    "Select Stops",
                    options=['non-stop', '1 stop', '2 stops', '3 stops', '4 stops'],
                    label_visibility="collapsed"
                )
            
            with col3:
                st.markdown('<div class="feature-card"><h4><i class="fa-solid fa-stopwatch"></i> Flight Duration</h4></div>', unsafe_allow_html=True)
                input_duration = st.slider(
                    "Duration (Minutes)",
                    min_value=30,
                    max_value=2000,
                    value=150,
                    step=10,
                    label_visibility="collapsed"
                )
                hours = input_duration // 60
                mins = input_duration % 60
                st.info(f"{hours}h {mins}m")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                submitted = st.form_submit_button("Generate Price Prediction", use_container_width=True)
        
        if submitted:
            try:
                with st.spinner("Analyzing flight parameters..."):
                    input_data = pd.DataFrame({
                        'Airline': [input_airline],
                        'Source': [input_source],
                        'Destination': [input_dest],
                        'Total_Stops': [input_stops],
                        'Duration': [input_duration]
                    })
                    
                    for col in ['Airline', 'Source', 'Destination', 'Total_Stops']:
                        input_data[col] = encoders[col].transform(input_data[col].astype(str))
                    
                    predicted_price = model.predict(input_data)[0]
                
                st.markdown(f"""
                <div class="prediction-result">
                    <h2><i class="fa-solid fa-wand-magic-sparkles"></i> Predicted Flight Price</h2>
                    <div class="prediction-price">₹{int(predicted_price):,}</div>
                    <p style="opacity: 0.9; margin-top: 1rem;">Based on {len(df):,} historical flight records</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                similar_flights = df[
                    (df['Airline'] == input_airline) & 
                    (df['Source'] == input_source) & 
                    (df['Destination'] == input_dest)
                ]
                
                with col1:
                    if len(similar_flights) > 0:
                        avg_similar = similar_flights['Price'].mean()
                        st.markdown(create_metric_card('<i class="fa-solid fa-chart-column"></i>', f"₹{int(avg_similar):,}", "Historical Average", "blue"), unsafe_allow_html=True)
                
                with col2:
                    if len(similar_flights) > 0:
                        st.markdown(create_metric_card('<i class="fa-solid fa-bullseye"></i>', f"{len(similar_flights)}", "Similar Flights", "teal"), unsafe_allow_html=True)
                
                with col3:
                    confidence = min(95, 80 + (len(similar_flights) / len(df)) * 100)
                    st.markdown(create_metric_card('<i class="fa-solid fa-shield-halved"></i>', f"{confidence:.0f}%", "Confidence Score", "orange"), unsafe_allow_html=True)
                
                st.markdown("""
                <div class="info-card">
                    <h4><i class="fa-solid fa-circle-info"></i> Model Information</h4>
                    <p>This prediction is generated by a <strong>Random Forest Regressor</strong> with 100 estimators,
                    trained on the complete dataset. The model considers airline, route, stops, and duration 
                    to estimate the most likely ticket price.</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error generating prediction: {str(e)}")

    elif "Data Explorer" in page:
        st.markdown("""
        <div class="main-header">
            <h1><i class="fa-solid fa-magnifying-glass"></i> Data Explorer</h1>
            <p>Browse, search, and analyze the complete flight dataset</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(create_section_header('<i class="fa-solid fa-clipboard-list"></i>', "Dataset Overview"), unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Records", f"{len(filtered_df):,}")
        col2.metric("Total Columns", len(filtered_df.columns))
        col3.metric("Memory Usage", f"{filtered_df.memory_usage(deep=True).sum() / 1024:.1f} KB")
        col4.metric("Missing Values", filtered_df.isnull().sum().sum())
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
        st.markdown(create_section_header('<i class="fa-solid fa-magnifying-glass"></i>', "Search & Filter"), unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            search_term = st.text_input("Search in dataset", placeholder="Type to search...")
        
        with col2:
            sort_col = st.selectbox("Sort by", options=filtered_df.columns.tolist())
            sort_order = st.checkbox("Descending order", value=True)
        
        display_df = filtered_df.copy()
        if search_term:
            mask = display_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
            display_df = display_df[mask]
        
        display_df = display_df.sort_values(sort_col, ascending=not sort_order)
        
        st.markdown(f"**Showing {len(display_df):,} records**")
        
        st.dataframe(display_df, use_container_width=True, height=450)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="Download Filtered Data (CSV)",
                data=csv,
                file_name=f"flight_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
        st.markdown(create_section_header('<i class="fa-solid fa-chart-column"></i>', "Column Statistics"), unsafe_allow_html=True)
        
        with st.expander("View Detailed Column Statistics"):
            stats_tabs = st.tabs(["Numerical", "Categorical"])
            
            with stats_tabs[0]:
                numeric_cols = filtered_df.select_dtypes(include=[np.number])
                if not numeric_cols.empty:
                    st.dataframe(numeric_cols.describe().T, use_container_width=True)
                else:
                    st.info("No numerical columns found.")
            
            with stats_tabs[1]:
                categorical_cols = filtered_df.select_dtypes(include=['object'])
                if not categorical_cols.empty:
                    cat_stats = pd.DataFrame({
                        'Column': categorical_cols.columns,
                        'Unique Values': [categorical_cols[col].nunique() for col in categorical_cols.columns],
                        'Most Common': [categorical_cols[col].mode()[0] if len(categorical_cols[col].mode()) > 0 else 'N/A' for col in categorical_cols.columns],
                        'Missing': [categorical_cols[col].isnull().sum() for col in categorical_cols.columns]
                    })
                    st.dataframe(cat_stats, use_container_width=True)
                else:
                    st.info("No categorical columns found.")

    # Footer
    st.markdown("""
    <div class="footer">
        <p>
            <strong>SkyPrice Analytics</strong> | Flight Price Intelligence Platform<br>
            Built with Streamlit & Plotly | © 2024
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem;">
        <h1 style="color: #dc2626;"><i class="fa-solid fa-triangle-exclamation"></i> Data Not Found</h1>
        <p style="font-size: 1.2rem; color: #64748b;">
            Please ensure that <code style="background: #f1f5f9; padding: 0.2rem 0.5rem; border-radius: 4px;">flight_price.xlsx</code> is present in the application directory.
        </p>
    </div>
    """, unsafe_allow_html=True)