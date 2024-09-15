import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(
    page_title="CSV Data Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add a title with a custom style
st.markdown("<h1 style='text-align: center; color: #42ffffa;'>📊 CSV Data Analyzer and Preprocessing App</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("Use this sidebar to upload your CSV and select options.")

# Upload CSV file
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Step 1: Read CSV into DataFrame
    data = pd.read_csv(uploaded_file)
    st.markdown("<h3 style='color: #2ffffa;'>🔍 Data Preview</h3>", unsafe_allow_html=True)
    st.dataframe(data.head())  # Display first few rows of the dataset

    # Step 2: Data Summary
    st.markdown("<h3 style='color: #2ffffa;'>📋 Dataset Summary</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Rows", data.shape[0])
        st.metric("Total Columns", data.shape[1])
    with col2:
        st.metric("Missing Values", data.isnull().sum().sum())
        st.metric("Columns with Missing Data", data.columns[data.isnull().any()].size)

    # Step 3: Show Column Data Types
    st.markdown("<h3 style='color: #2ffffa;'>🧬 Column Data Types</h3>", unsafe_allow_html=True)
    st.write(data.dtypes)

    # Step 4: Handle Missing Data
    st.markdown("<h3 style='color: #2ffffa;'>🛠 Handle Missing Data</h3>", unsafe_allow_html=True)
    st.write("Choose how to handle missing data in your dataset.")

    fill_missing = st.selectbox(
        "How would you like to handle missing values?",
        ("Do Nothing", "Fill with Mean", "Fill with Median", "Drop Rows with Missing Values")
    )

    if fill_missing == "Fill with Mean":
        data.fillna(data.mean(), inplace=True)
        st.success("Filled missing values with column means.")
    elif fill_missing == "Fill with Median":
        data.fillna(data.median(), inplace=True)
        st.success("Filled missing values with column medians.")
    elif fill_missing == "Drop Rows with Missing Values":
        data.dropna(inplace=True)
        st.success("Dropped rows with missing values.")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Step 5: Basic Statistics
    st.markdown("<h3 style='color: #2ffffa;'>📊 Descriptive Statistics</h3>", unsafe_allow_html=True)
    st.write(data.describe())

    # Step 6: Visualization
    st.markdown("<h3 style='color: #2ffffa;'>📈 Data Visualization</h3>", unsafe_allow_html=True)

    # Select a column to visualize
    column_to_plot = st.selectbox("Select column for visualization", data.columns)

    if np.issubdtype(data[column_to_plot].dtype, np.number):
        # Plot histogram for numeric columns
        st.markdown(f"<h4 style='color: #2ffffa;'>Histogram for {column_to_plot}</h4>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.hist(data[column_to_plot].dropna(), bins=20, color='skyblue', edgecolor='black')
        st.pyplot(fig)
    else:
        # Plot bar chart for categorical columns
        st.markdown(f"<h4 style='color: #2ffffa;'>Bar Chart for {column_to_plot}</h4>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        data[column_to_plot].value_counts().plot(kind='bar', ax=ax, color='lightgreen')
        st.pyplot(fig)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Step 7: Export cleaned data
    st.markdown("<h3 style='color: #2ffffa;'>💾 Export Cleaned Data</h3>", unsafe_allow_html=True)

    if st.button("Download Cleaned CSV"):
        cleaned_csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=cleaned_csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )
        st.success("Cleaned data exported successfully!")
else:
    st.markdown("<h3 style='text-align: center; color: #FF6347;'>⚠️ Please upload a CSV file to get started.</h3>", unsafe_allow_html=True)
