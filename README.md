# Updated Interview Task

# 🧊 CRAC Unit Hunting Detection

This repository contains a **Python script** to detect *hunting* behavior in a **CRAC (Computer Room Air Conditioning)** unit — defined as rapid fluctuations in supply air temperature. If more than **5 rapid changes** occur within a single hour, an alert is generated.

---

## 📌 Project Goals

- **📥 Read & Preprocess Data**  
  Load a Parquet file and clean rows with missing values.

- **🔍 Detect Hunting Activities**  
  Use temperature differences between consecutive readings and detect anomalies.

- **🚨 Generate Alerts**  
  If >5 anomalies are found in any one-hour period, flag it.

- **📊 Visualize Results**  
  Plot normal vs anomalous readings for quick analysis.

---

## 🧠 Model Details: Isolation Forest

This project uses **Isolation Forest** from `scikit-learn`, an unsupervised algorithm great for detecting anomalies.

### How it works:

- **🔀 Isolation Principle**:  
  Randomly splits data until each point is isolated. Anomalies are isolated quicker.

- **🌲 Tree Ensemble**:  
  A forest of isolation trees improves accuracy.

- **⚖️ Contamination Parameter**:  
  Default = `0.01` (1% of the data expected to be anomalies).

---

## 🔄 Workflow

### 1. 🛠 Feature Engineering

- Compute `temp_diff`: the difference between consecutive supply air temperature readings.
- This captures rapid shifts in temperature — the essence of hunting behavior.

### 2. 🎯 Model Training

- Train **Isolation Forest** on `temp_diff`.
- Label outputs:  
  `1` = normal, `-1` = anomaly.

---

## 💾 Requirements

```bash
Python 3.7+
pandas
matplotlib
scikit-learn
pyarrow
```

**Install:**

```bash
pip install pandas matplotlib scikit-learn pyarrow
```

---

## 🚀 Usage

### 1. Clone the repository

```bash
git clone <repository_link>
cd <repository_directory>
```

### 2. Update File Path

Inside `main()`, change:

```python
file_path = 'your_file.parquet'
```

### 3. Choose a TagName

```python
tag_to_use = 'QTS_LAB_CRAC_MG1102_07.SAT'
```

Change this if you're analyzing a different sensor.

### 4. Run the script

```bash
python script_name.py
```

This will:

- Load and clean the data
- Filter for `.SAT` TagName
- Compute temperature changes
- Detect anomalies using Isolation Forest
- **Plot** normal vs anomalous points
- **Generate alerts** if anomalies exceed threshold

---

## 🧩 Code Structure

### `read_data(file_path)`

- Reads Parquet
- Drops rows with missing `max` values
- Converts `time` to datetime

---

### `detect_rapid_changes_isolation_forest(df, contamination=0.01)`

- Computes `temp_diff`
- Applies Isolation Forest on `temp_diff`
- Returns DataFrame with `anomaly` column

---

### `plot_anomalies(results_df, title='SAT Anomaly Detection')`

- Visualizes the time series
- Normal points = blue  
  Anomalies = red

---

### `generate_alerts(df, threshold=5)`

- Groups anomalies by hour
- Returns alerts if count > 5 anomalies/hour

---

### `main()`

- Loads data
- Filters for SAT Tag
- Computes anomalies
- Plots results
- Generates alerts

---

## 📁 Assumptions

- Data format: **Parquet**
- Required columns: `time`, `max`, `TagName`
- Filters for rows with `.SAT` in TagName
- Default Tag: `QTS_LAB_CRAC_MG1102_07.SAT`

---

## 🔭 Future Improvements

### 🔧 Parameterization

- Accept CLI args for:
  - File path
  - Contamination rate
  - TagName
  - Threshold

### 🧠 Model Enhancements

- Use additional features like moving averages or gradient over time.

### 📂 File Format Support

- Add support for CSV, Excel, etc.

### ⚙️ Real-Time & Edge Deployment

- **Real-Time Ingestion** via MQTT or similar
- **Parallel Processing** via Dask or multiprocessing
- **Edge Computing** for decentralized processing
- **Alert Monitoring** for robust deployment








# Interview Task

## Objective
Your task is to read in a data file and create logic to detect hunting activities with a CRAC (Computer Room Air Conditioning) unit. If hunting occurs more than 5 times in a hour, it should be considered an alert.

## Data File
The data file contains timestamped entries of the CRAC unit's activities. Each entry includes a timestamp, Return Air Tempurature, Supply Air Temperature.

## Requirements
1. **Read the Data File**: Write a function to read the data file and parse the entries.
2. **Detect Hunting Activities**: Implement logic to detect hunting activities. Hunting is defined as rapid changes in the CRAC unit's supply temperature.
3. **Generate Alerts**: If hunting occurs more than 5 times within a hour, generate an alert.


## Deliverables
1. The code to read and parse the data file.
2. The logic to detect hunting activities.
3. The code to generate alerts when hunting occurs more than 5 times in a hour.
4. A brief explanation of your approach and any assumptions made.

## Submission
Please submit your solution as a GitHub repository link or a zip file containing your code and explanation.

Good luck!