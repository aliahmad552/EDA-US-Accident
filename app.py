# app.py
import streamlit as st
import helper

st.set_page_config(page_title="US Accident Dashboard", layout="wide")

# Sidebar filters
st.sidebar.title("Filters")
df = helper.load_data(nrows=1_000_000)

year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique()))
states = st.sidebar.multiselect("Select States", df['State'].unique())

filtered_df = helper.filter_data(df, year, states)

# Dashboard
st.title("🚦 US Traffic Accident Analysis")

st.header("📊 Overview")
helper.show_overview(filtered_df, st)

st.header("⏳ Time Analysis")
st.plotly_chart(helper.plot_yearly(filtered_df))
st.plotly_chart(helper.plot_monthly(filtered_df))
st.pyplot(helper.plot_heatmap(filtered_df))

st.header("🗺️ Geographic Analysis")
st.plotly_chart(helper.plot_state_map(filtered_df))
st.plotly_chart(helper.plot_city_map(filtered_df))

st.header("⚠️ Severity & Weather")
st.plotly_chart(helper.plot_severity(filtered_df))
st.plotly_chart(helper.plot_weather(filtered_df))

st.header("🚗 Road & Traffic Features")
st.plotly_chart(helper.plot_junction(filtered_df))
sig_fig = helper.plot_signal(filtered_df)
if sig_fig:
    st.plotly_chart(sig_fig)

st.header("📈 Numerical Analysis")
st.pyplot(helper.plot_correlation(filtered_df))

st.header("🔍 Key Insights")
helper.show_insights(st)
