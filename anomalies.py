import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

def read_data(file_path):
    """
    Reads the parquet file into a DataFrame, drops rows with missing 'max',
    and ensures 'time' is a datetime column.
    """
    df = pd.read_parquet(file_path)
    df = df.dropna(subset=['max'])
    df['time'] = pd.to_datetime(df['time'])
    return df

def detect_rapid_changes_isolation_forest(df, contamination=0.01):
    """
    Detect anomalies (rapid changes) in supply air temperature using Isolation Forest.
    
    Args:
        df (pd.DataFrame): DataFrame containing columns ['time', 'max'] for a single SAT TagName.
        contamination (float): Proportion of outliers in the data (tunable parameter).
    
    Returns:
        pd.DataFrame: Original df with an additional 'anomaly' column (1 = normal, -1 = anomaly).
    """
    # Sort by time
    df = df.sort_values('time').reset_index(drop=True)
    
    # Create a feature: temperature difference from the previous reading
    df['temp_diff'] = df['max'].diff().fillna(0)
    
    # Convert to 2D array for model input
    X = df[['temp_diff']].values
    
    # Initialize and train Isolation Forest
    iso_forest = IsolationForest(n_estimators=100,
                                 contamination=contamination,
                                 random_state=42)
    iso_forest.fit(X)
    
    # Predict anomalies (1 = normal, -1 = anomaly)
    preds = iso_forest.predict(X)
    df['anomaly'] = preds
    
    return df

def plot_anomalies(results_df, title='SAT Anomaly Detection'):
    """
    Plot the time series and color anomalies in red.
    """
    normal_data = results_df[results_df['anomaly'] == 1]
    anomaly_data = results_df[results_df['anomaly'] == -1]
    
    plt.figure(figsize=(12, 6))
    plt.plot(normal_data['time'], normal_data['max'], 'b.-', label='Normal')
    plt.plot(anomaly_data['time'], anomaly_data['max'], 'r.', label='Anomaly')
    plt.xlabel('Time')
    plt.ylabel('Max Value')
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()

def generate_alerts(df, threshold=5):
    """
    Group anomalies by hour and generate alerts if anomalies exceed threshold.
    
    Returns:
        pd.DataFrame: Rows with hour and anomaly count that exceed the threshold.
    """
    df['hour'] = df['time'].dt.floor('H')
    
    # Count anomalies per hour (anomaly = -1)
    anomaly_counts = df[df['anomaly'] == -1].groupby('hour')['anomaly'].count().reset_index(name='count')
    
    # Filter hours where anomalies exceed the threshold
    alerts = anomaly_counts[anomaly_counts['count'] > threshold]
    return alerts

def main():
    file_path = 'lab.parquet'  # Update with your actual file path
    
    # 1. Read the data
    df = read_data(file_path)
    
    # 2. Filter for Supply Air Temperature (SAT) TagNames
    sat_df = df[df['TagName'].str.contains('.SAT')]
    
    # If you want to pick a specific TagName, update the code here:
    tag_to_use = 'QTS_LAB_CRAC_MG1102_07.SAT'
    sat_df = sat_df[sat_df['TagName'] == tag_to_use]
    
    # # Otherwise, just pick the first SAT TagName found
    # unique_sat_tags = sat_df['TagName'].unique()
    # if len(unique_sat_tags) == 0:
    #     print("No SAT measurements found in the data.")
    #     return
    
    # first_sat_tag = unique_sat_tags[0]
    # print(f"Using TagName: {first_sat_tag}")
    
    # sat_df = sat_df[sat_df['TagName'] == first_sat_tag]
    
    # 3. Detect anomalies (rapid changes) using Isolation Forest
    results_df = detect_rapid_changes_isolation_forest(sat_df, contamination=0.01)
    
    # 4. Plot the anomalies
    plot_anomalies(results_df, title=f'{tag_to_use} - Anomaly Detection')
    
    # 5. Generate alerts if more than 5 anomalies occur within an hour
    alerts_df = generate_alerts(results_df, threshold=5)
    if alerts_df.empty:
        print("No alerts generated. Anomalies per hour did not exceed the threshold.")
    else:
        print("Alerts generated! Hours exceeding the threshold:")
        print(alerts_df)

if __name__ == "__main__":
    main()
