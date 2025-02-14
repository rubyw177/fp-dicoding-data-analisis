# Air Quality Data Analysis Dashboard

## Overview
This project implements an **air quality analysis dashboard** using **Streamlit** and **Pandas**. The dashboard provides insights into air pollution trends, specifically focusing on **PM2.5, CO, and PM10** levels from 2013 to 2017. The system processes air quality data, generates visualizations, and forecasts pollutant levels using **moving averages**.

## Features
- **Time-Series Analysis**: Tracks PM2.5 levels over time.
- **Monthly CO Analysis**: Identifies month-to-month CO variations in 2016.
- **Station Comparison**: Determines the best and worst air quality stations.
- **Forecasting**: Predicts PM2.5 levels for the next 7 days using a moving average model.

## Dependencies
Ensure the following libraries are installed:
```bash
pip install pandas matplotlib seaborn numpy streamlit
```

## Project Structure
```
📂 project_root/
├── 📜 fp_streamlit.py        # Streamlit dashboard script
├── 📜 fp_notebook.ipynb      # Jupyter notebook for analysis
├── 📄 all_air_data_final.csv # Air quality dataset
├── 📊 dashboard_streamlit.png # Dashboard screenshot
├── 📄 requirements.txt       # Dependency list
└── 📝 README.md             # Project documentation
```

## Usage
### 1. Run the Streamlit Dashboard
To launch the dashboard, execute the following command in the terminal:
```bash
streamlit run fp_streamlit.py
```
The dashboard will be accessible at `http://localhost:8501`.

### 2. Data Processing Functions
The script processes air quality data using various functions:

#### **Yearly PM2.5 Trends**
This function calculates the average PM2.5 concentration per year to analyze pollution trends over time.
```python
def create_pertanyaan1_df(df):
    return df.groupby(by="year")["PM2.5"].mean().reset_index()
```

#### **Monthly CO Differences (2016)**
This function extracts and analyzes CO levels for each month in 2016 to identify seasonal variations in pollution levels.
```python
def create_pertanyaan2_df(df):
    df = df[(df["year"] >= 2015) & (df["year"] < 2017)]
    df = df.groupby(["year", "month"]).agg({"CO": "mean"}).reset_index()
    df = df[df["year"] == 2016]
    return df
```

#### **Worst and Best Air Quality Stations (2016)**
This function identifies the stations with the highest and lowest PM2.5 levels in 2016 to determine areas with the worst and best air quality.
```python
def create_pertanyaan3_df(df):
    return df[df["year"] == 2016].groupby("station")["PM2.5"].mean().reset_index()
```

#### **PM2.5 Forecast Using Moving Averages**
To predict PM2.5 levels for the next seven days, this function applies a **5-day moving average**, smoothing the data and revealing trends.
```python
def forecast_MA_df(df):
    df["MovingAverage"] = df["PM2.5"].rolling(window=5).mean()
    return df.dropna()
```

### 3. Visualizations
The dashboard includes:
- **PM2.5 Trends Over Time**: Displays a line chart showing pollution fluctuations over the years.
- **CO Changes by Month in 2016**: A bar chart highlighting variations in CO concentration month by month.
- **Best and Worst Air Quality Stations**: A comparative analysis of the most and least polluted locations.
- **PM2.5 Forecast for 7 Days**: A predictive model that estimates future pollution levels based on past data.

## Explanation of Analysis
- **Why PM2.5 and CO?**
  - PM2.5 is a significant air pollutant that affects respiratory health.
  - CO is an indicator of incomplete combustion and vehicle emissions, influencing urban air quality.
- **Why Moving Average Forecasting?**
  - Air pollution data contains noise and fluctuations, making traditional forecasting difficult.
  - A moving average smooths out the variations and reveals underlying trends, providing a more reliable prediction.
- **How Does the Dashboard Help?**
  - Users can explore air quality trends interactively.
  - Decision-makers can use insights to implement better pollution control measures.
  - The forecasting feature can be used for proactive health alerts in high-risk areas.

## How to Replicate the Project
Follow these steps to set up and run the project:
1. **Clone the Repository**
   ```bash
   git clone https://github.com/rubyw177/fp-dicoding-data-analisis.git
   cd fp-dicoding-data-analisis
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Jupyter Notebook for Data Exploration**
   ```bash
   jupyter notebook fp_notebook.ipynb
   ```
   - This allows you to explore and preprocess the dataset interactively.
     
4. **Run the Streamlit Dashboard**
   ```bash
   streamlit run fp_streamlit.py
   ```
   - The dashboard will open in your default web browser at `http://localhost:8501`.
