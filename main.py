import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
st.set_page_config(page_title="Simple Data Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center; color: White;'>Data Analysis Dashboard</h1><p style='text-align: center; color: white'>Upload  Analyze  Visualize</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
if uploaded_file is not None:
    with st.spinner('Loading Dataset...'):
        df=pd.read_csv(uploaded_file)
    st.success('File uploaded successfully!')
    col1,col2,col3,col4=st.columns(4)
    col1.metric("Number of Rows", df.shape[0])  
    col2.metric("Number of Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())
    col4.metric("Duplicate Rows", df.duplicated().sum())
    st.markdown("----")
    st.sidebar.title("Dashboard controls")
    filter_column = st.sidebar.selectbox("Filter column", df.columns.tolist())
    filter_value = st.sidebar.selectbox("Filter value", df[filter_column].unique().tolist())
    filtered_df = df[df[filter_column] == filter_value]
    left, right = st.columns([2,1])
    with left:
        st.subheader("Data Preview")
        st.dataframe(filtered_df.head())
    with right:
        st.subheader("Data Summary")
        st.write(filtered_df.describe())
    st.markdown("----")
    st.subheader("Data Visualization")
    numeric_columns = filtered_df.select_dtypes(include="number").columns.tolist()
    if len(numeric_columns) >= 2:
        x=st.selectbox("Select X-axis column", numeric_columns)
        y=st.selectbox("Select Y-axis column", numeric_columns, index=1)
        chart_type = st.selectbox("Select chart type", ["Line Chart", "Scatter Chart", "Bar Chart"])
        if chart_type == "Line Chart":
            st.line_chart(filtered_df.set_index(x)[y])
        elif chart_type == "Bar Chart":
            st.bar_chart(filtered_df.set_index(x)[y])
        elif chart_type == "Scatter Chart":
            fig , ax = plt.subplots(figsize=(10,5))
            ax.scatter(filtered_df[x], filtered_df[y])
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(f"{y} vs {x}")
            st.pyplot(fig)
    else:
        st.warning("Dataset must have at least two numeric columns for visualization.")
    st.markdown("----")
    csv=filtered_df.to_csv(index=False)
    st.download_button(label="Download Filtered Data as CSV", data=csv, file_name="filtered_data.csv", mime="text/csv")
    st.markdown("----")
    st.markdown("<p style='text-align: center; color:gray'>Developed by A Azhagu Ramkumar </p>", unsafe_allow_html=True)
else:
    st.info("Please upload a CSV file to start the analysis.")