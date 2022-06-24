import pandas as pd


def date_filter(df, start_date, end_date):
    df["start_date"] = pd.to_datetime(df['date'], yearfirst=True).dt.floor("D")
   
    if start_date is not None and end_date is not None:
        df = df.loc[(df['start_date'] >= start_date) & (df['start_date'] <= end_date)]
    elif start_date is not None:
        df = df.loc[(df['start_date'] >= start_date)]
    elif end_date is not None:
        df = df.loc[(df['start_date'] <= end_date)]
    return df


def sensor_filter(df, sensor):
    df["sensor"] = df['sensorID']
    if sensor is not None:
        df = df.loc[(df['sensor'] == sensor)]
    return df

