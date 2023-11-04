import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

def create_pertanyaan1_df(df):
    pm25_yearly_avg_df = df.groupby(by="year").agg({
        "PM2.5": "mean"
    }).reset_index()
    return pm25_yearly_avg_df

def create_pertanyaan2_df(df):
    monthly_co_df = df[(df["year"] >= 2015) & (df["year"] < 2017)].groupby(by=["year", "month"]).agg({
        "CO": "mean"
    }).reset_index()

    delta = []
    range_co = len(monthly_co_df["CO"])
    for i in range(range_co):
        if not((i == range_co) or (i == 0)):
            diff = monthly_co_df["CO"][i] - monthly_co_df["CO"][i-1]
            delta.append(diff)

    monthly_co_df = monthly_co_df.iloc[1:]
    monthly_co_df["delta_CO"] = delta
    monthly_co_df = monthly_co_df[monthly_co_df["year"] == 2016]
    return monthly_co_df

def create_pertanyaan3_df(df):
    station_df = df[df["year"] == 2016].groupby(by=["station", "year"]).agg({
        "CO": "mean",
        "PM2.5": "mean",
        "PM10": "mean"
    }).reset_index()
    return station_df

def create_pertanyaan4_df(df):
    daily_pm25_df = df.groupby(by=["year", "day"]).agg({
        "PM2.5": "mean"
    }).reset_index()

    window_size = 5
    daily_pm25_df['MovingAverage'] = daily_pm25_df['PM2.5'].rolling(window=window_size).mean()
    daily_pm25_df = daily_pm25_df.dropna(axis=0)

    time_step = [i+1 for i in range(len(daily_pm25_df))]
    daily_pm25_df["day"] = time_step
    return daily_pm25_df

def forecast_MA_df(df):
    forecast_period = 7

    for i in range(forecast_period):
        data_to_append = []
        last_ma = df["MovingAverage"].iloc[-5].mean()
        next_day = df["day"].iloc[-1] + 1
        last_year = df["year"].iloc[-1]

        data_to_append.append({
            "year": last_year,
            "day": next_day,
            "PM2.5": last_ma,
            "MovingAverage": last_ma,
        })
        # Use pd.concat to append the data in a single step
        df = pd.concat([df, pd.DataFrame(data_to_append)], ignore_index=True)

    return df
    
all_df = pd.read_csv("all_air_data_final.csv")

# # add date column by combining seperate year, month, day columns
# all_df["date"] = pd.to_datetime(all_df[["year", "month", "day"]], format="%Y-%m-%d")

# # membuat komponen filter
# min_date = all_df["date"].min()
# max_date = all_df["date"].max()

# with st.sidebar:
#     # mengambil start date dan end date dari input
#     start_date, end_date = st.date_input(
#         label = "Rentang Waktu Untuk Forecasting",
#         min_value = min_date,
#         max_value = max_date,
#         value = [min_date, max_date] 
#     )

# main_df = all_df[(all_df["date"] >= str(start_date)) and (all_df["date"] <= str(end_date))]
pm25_yearly_avg_df = create_pertanyaan1_df(all_df)
monthly_co_df = create_pertanyaan2_df(all_df)
station_df = create_pertanyaan3_df(all_df)
daily_pm25_df = create_pertanyaan4_df(all_df)
daily_pm25_df = forecast_MA_df(daily_pm25_df)

# melengkapi dashboard
st.header("Dicoding FInal Project Air Quality Data Dashboard :chart_with_upwards_trend:")

# grafik pertanyaan 1
st.subheader("Rata-rata PM2.5 dari tahun 2013-2017")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    pm25_yearly_avg_df["year"],
    pm25_yearly_avg_df["PM2.5"],
    marker='o', 
    linewidth=2,
    color="#b83f35"
)

ax.set_title("PM2.5 per Year", loc="center", fontsize=18)
ax.set_ylabel(None)
ax.set_xlabel(None)
st.pyplot(fig)

# grafik pertanyaan 2
st.subheader("Selisih nilai CO setiap bulannya tahun 2016")
fig, ax = plt.subplots(figsize=(12, 6))
color = ["#b83f35", "#b83f35", "#468ae3", "#b83f35", "#b83f35", "#468ae3", "#468ae3", "#b83f35", "#b83f35", "#468ae3", "#468ae3", "#468ae3",]
sns.barplot(
    x="month",
    y="delta_CO",
    data=monthly_co_df,
    palette=color,
    ax=ax
)

ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)
ax.set_title("Delta CO (mg/m³) by Month in 2016", loc="center", fontsize=18)
st.pyplot(fig)

# grafik pertanyaan 3
st.subheader("Stasiun dengan kualitas udara terburuk dan terbaik tahun 2016")
fig, ax = plt.subplots(figsize=(12, 6))
color = ["lightgrey", "lightgrey", "#468ae3", "#b83f35", "lightgrey", "lightgrey", "lightgrey", "lightgrey", "lightgrey", "lightgrey", "lightgrey", "lightgrey"]
sns.barplot(
    data=station_df,
    x="station",
    y="PM2.5",
    palette=color,
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', rotation=12)
ax.set_title("PM2.5 by Station in 2016", loc="center", fontsize=18)
st.pyplot(fig)

# grafik pertanyaan 4
st.subheader("Forecasting PM2.5 untuk 7 hari kedepan")
forecast_period = 7
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    np.arange(0, len(daily_pm25_df)-forecast_period),
    daily_pm25_df["PM2.5"].iloc[:-forecast_period],
    color="lightgrey",
    label="Original Data"
)
ax.plot(
    np.arange(len(daily_pm25_df)-forecast_period, len(daily_pm25_df)),
    daily_pm25_df["PM2.5"].iloc[-forecast_period:],
    color="#491273",
    label="Moving Average Forecast"
)
ax.set_title("PM2.5 Forecast for {} Days".format(forecast_period), loc="center", fontsize=18)
ax.legend()
st.pyplot(fig)

st.caption("Final Project William Kester Hermawan Dicoding 2023")



