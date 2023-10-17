import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style="dark")

def create_holiday_df(df):
    holiday_bike = df.groupby(by="holiday").instant.nunique().reset_index()
    holiday_bike.rename(columns={"instant": "sum"}, inplace=True)
    holiday_bike

    return holiday_bike

def create_weekday_df(df):
    weekday_bike = df.groupby(by="weekday").instant.nunique().reset_index()
    weekday_bike.rename(columns={"instant": "sum"}, inplace=True)
    weekday_bike

    return weekday_bike

def sidebar(df):
    df["dteday"] = pd.to_datetime(df["dteday"])
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()
    with st.sidebar:
        # Logo
        st.image("https://github.com/amandaaanh/Belajar-Analisis-Data-dengan-Python/blob/main/Capital%20Bikeshare%20Logo.png")

        def on_change():
            st.session_state.date = date

        date = st.date_input(
            label="Time Range",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date],
            on_change=on_change
        )

    return date

# Load dataset
df_day = pd.read_csv("dashboard.csv")

date = sidebar(df_day)
if len(date) == 2:
    dataFrame = df_day[(df_day["dteday"] >= str(date[0])) & (df_day["dteday"] <= str(date[1]))]
else:
    main_df = df_day[
        (df_day["dteday"] >= str(st.session_state.date[0])) & (df_day["dteday"] <= str(st.session_state.date[1]))]

holiday_bike = create_holiday_df(dataFrame)
weekday_bike = create_weekday_df(dataFrame)

st.header("Bike Sharing Dashboard")
# Pertanyaan 1: Bagaimana pengaruh hari libur pada rental sepeda?
st.subheader("Holiday")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(
    y="sum",
    x="holiday",
    data=holiday_bike.sort_values(by="holiday", ascending=False),
    palette="muted"
)
ax.set_title("How do holidays affect bike rentals?", loc="center", fontsize=12)
ax.set_label("Number of Renters")
ax.set_xlabel(None)
ax.tick_params(axis="x", labelsize=12)
ax.tick_params(axis="y", labelsize=12)
st.pyplot(fig)

# Pertanyaan 2: Bagaimana jumlah pengguna rental sepeda tiap harinya?
st.subheader("Weekday")
fig, ax = plt.subplots(figsize=(8, 6))
colors = sns.color_palette("viridis")

sns.barplot(
    y="sum",
    x="weekday",
    data=weekday_bike.sort_values(by="weekday", ascending=False),
    palette="muted"
)
ax.set_title("How many bicycle rental users are there each day?", loc="center", fontsize=12)
ax.set_ylabel("Number of Renters")
ax.set_xlabel(None)
ax.tick_params(axis="x", labelsize=12)
ax.tick_params(axis="y", labelsize=12)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(6, 6))

ax.pie(weekday_bike['sum'], labels=weekday_bike['weekday'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
ax.axis('equal')
ax.set_title("Distribution of Bike Rentals per Day", fontsize=12)
st.pyplot(fig)