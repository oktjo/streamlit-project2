import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Page Configuration
st.set_page_config(
    page_title="UNEB Performance Dashboard 2026", 
    page_icon="🎓", 
    layout="wide"
)

# 2. Data Loading
@st.cache_data
def load_data():
    # Ensure data/uneb.csv exists in your directory
    df = pd.read_csv("data/uneb.csv")
    # Adding mock 'Exam' column if not present in CSV
    if "Exam" not in df.columns:
        df["Exam"] = np.random.choice(["PLE", "UCE", "UACE"], size=len(df))
    return df

try:
    df = load_data()

    # 3. Sidebar Filters
    st.sidebar.title("🎛 Filters")
    
    exam = st.sidebar.selectbox("Select Exam Level", options=df["Exam"].unique())
    
    # Filter subject based on exam selection
    available_subjects = df[df["Exam"] == exam]["Subject"].unique()
    subject = st.sidebar.multiselect(
        "Select Subject", 
        options=available_subjects, 
        default=available_subjects
    )
    
    district = st.sidebar.multiselect(
        "Select School/District", 
        options=df["School"].unique(), 
        default=df["School"].unique()[:5] # Default to first 5 to avoid clutter
    )
    
    gender = st.sidebar.radio("Gender", options=["All", "M", "F"])

    # 4. Data Filtering Logic
    filtered_data = df[
        (df["Exam"] == exam) & 
        (df["Subject"].isin(subject)) & 
        (df["School"].isin(district))
    ]

    if gender != "All":
        filtered_data = filtered_data[filtered_data["Gender"] == gender]

    # 5. Header Section
    st.title("🎓 UNEB Student Performance Dashboard – 2026")
    st.markdown(f"Overview of performance for **{exam}** results.")

    # 6. KPI Metrics
    if not filtered_data.empty:
        total_students = filtered_data["StudentID"].nunique()
        average_score = round(filtered_data["Score"].mean(), 2)
        pass_rate = round((filtered_data["Score"] >= 50).mean() * 100, 2)
        top_school = (
            filtered_data.groupby("School")["Score"]
            .mean()
            .idxmax()
        )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👨‍🎓 Total Students", f"{total_students:,}")
        col2.metric("📊 Average Score", f"{average_score}%")
        col3.metric("✅ Pass Rate", f"{pass_rate}%")
        col4.metric("🏫 Top School", top_school)
        
        st.divider()

        # 7. Data Visualization & Table
        tab1, tab2 = st.tabs(["📊 Visualizations", "📋 Raw Data"])
        
        with tab1:
            st.subheader("Performance by Subject")
            chart_data = filtered_data.groupby("Subject")["Score"].mean().sort_values()
            st.bar_chart(chart_data)

        with tab2:
            st.dataframe(filtered_data, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

except FileNotFoundError:
    st.error("Error: The file 'data/uneb.csv' was not found. Please ensure the file exists.")
