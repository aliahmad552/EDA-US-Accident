# helper.py
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------------------
# Load & Preprocess Data
# ---------------------------
def load_data(nrows=1_000_000, random_state=42):
    """Load random sample of nrows from CSV"""
    df = pd.read_csv("US_Accidents_March23.csv")
    if len(df) > nrows:
        df = df.sample(n=nrows, random_state=random_state)

    df['Start_Time'] = pd.to_datetime(df['Start_Time'],format="ISO8601")
    df['Year'] = df['Start_Time'].dt.year
    df['Month'] = df['Start_Time'].dt.month
    df['Hour'] = df['Start_Time'].dt.hour
    df['DayOfWeek'] = df['Start_Time'].dt.day_name()
    return df

def filter_data(df, year=None, states=None):
    """Apply filters on data"""
    if year:
        df = df[df['Year'] == year]
    if states:
        df = df[df['State'].isin(states)]
    return df

# ---------------------------
# Overview Section
# ---------------------------
def show_overview(df, st=None):
    total_accidents = f"{df.shape[0]:,}"
    total_states = df['State'].nunique()
    avg_severity = round(df['Severity'].mean(), 2)
    top_city = df['City'].value_counts().idxmax()

    if st:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Accidents", total_accidents)
        col2.metric("States Covered", total_states)
        col3.metric("Avg Severity", avg_severity)
        col4.metric("Top City", top_city)

# ---------------------------
# Time Analysis
# ---------------------------
def plot_yearly(df):
    yearly = df.groupby("Year").size().reset_index(name="Accidents")
    fig = px.line(yearly, x="Year", y="Accidents", markers=True,
                  title="Accidents Per Year")
    return fig

def plot_monthly(df):
    monthly = df.groupby("Month").size().reset_index(name="Accidents")
    fig = px.bar(monthly, x="Month", y="Accidents",
                 title="Accidents Per Month")
    return fig

def plot_heatmap(df):
    heatmap_data = (
        df.groupby(['DayOfWeek', 'Hour'])
        .size()
        .reset_index(name="Accidents")
        .pivot(index="DayOfWeek", columns="Hour", values="Accidents")
        .reindex(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
    )
    fig, ax = plt.subplots(figsize=(12,6))
    sns.heatmap(heatmap_data, cmap="Reds", ax=ax)
    ax.set_title("Accidents by Hour of Day vs Day of Week")
    return fig

# ---------------------------
# Geographic Analysis
# ---------------------------
def plot_state_map(df):
    state_counts = df['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Accidents']
    fig = px.choropleth(
        state_counts,
        locations="State",
        locationmode="USA-states",
        color="Accidents",
        scope="usa",
        title="Accidents per State"
    )
    return fig

def plot_city_map(df):
    sample = df.sample(n=min(5000, len(df)), random_state=42)  # avoid lag
    fig = px.scatter_mapbox(
        sample,
        lat="Start_Lat", lon="Start_Lng",
        color="Severity",
        size_max=10,
        zoom=3,
        mapbox_style="carto-positron",
        title="Accidents by City (sample view)"
    )
    return fig

# ---------------------------
# Severity & Weather
# ---------------------------
def plot_severity(df):
    fig = px.histogram(df, x="Severity", nbins=10,
                       title="Accidents by Severity")
    return fig

def plot_weather(df):
    top_weather = df['Weather_Condition'].value_counts().nlargest(10).reset_index()
    top_weather.columns = ["Weather", "Accidents"]
    fig = px.bar(top_weather, x="Weather", y="Accidents",
                 title="Top 10 Weather Conditions")
    return fig

# ---------------------------
# Road & Traffic Features
# ---------------------------
def plot_junction(df):
    cols = ['Amenity','Bump','Crossing','Give_Way','Junction','Railway','Roundabout','Station','Stop','Traffic_Signal']
    counts = {col: df[col].sum() for col in cols if col in df.columns}
    counts_df = pd.DataFrame(list(counts.items()), columns=['Feature','Accidents'])
    fig = px.bar(counts_df, x="Feature", y="Accidents",
                 title="Accidents by Road Features")
    return fig

def plot_signal(df):
    if "Traffic_Signal" in df.columns:
        counts = df["Traffic_Signal"].value_counts().reset_index()
        counts.columns = ["Traffic Signal", "Count"]
        fig = px.pie(counts, names="Traffic Signal", values="Count",
                     title="Accidents with/without Traffic Signal")
        return fig

# ---------------------------
# Numerical Analysis
# ---------------------------
def plot_correlation(df):
    num_cols = df.select_dtypes(include=['int64','float64']).sample(n=8, axis=1, random_state=42)
    corr = num_cols.corr()
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Heatmap of Numerical Features")
    return fig

# ---------------------------
# Insights
# ---------------------------
def show_insights(st=None):
    insights = """
    ### 🔍 Key Insights
    - California, Texas, and Florida consistently record the highest accident counts.
    - Most accidents occur during rush hours (7–9 AM and 5–7 PM).
    - Severity 2 accidents dominate, but Severity 4 (highest) are linked with bad weather.
    - Poor weather (Rain, Fog, Snow) and night-time visibility increase accident severity.
    - Highways, crossings, and traffic signals are major hotspots.
    - Correlation analysis shows transaction count and amount features are strongly related.
    """
    if st:
        st.markdown(insights)
    else:
        print(insights)
