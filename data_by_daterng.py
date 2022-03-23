import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta

SS_DENSITY = 0.12
MCO_DENSITY = 0.09

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/dblidar")
conn = engine.connect()

def getData(sdate, edate):
    try:
        data_query = '''select "LocalTime","Volume","ConveyorId" from "VolumeLogReports" where  "LocalTime"::date >= \'''' + str(sdate) +  '''\'
                         and "LocalTime"::date <= \''''+ str(edate)+'''\' and "Volume" > 0 ;'''
        data_df = pd.read_sql(data_query, conn)

        return data_df              

    except Exception as e:
        return (e)

def VolByDateRange(sdate, edate):

    h_range = np.empty((0,0))
    df_lidar = getData(str(sdate), str(edate))
    # print(df_lidar.head())
    df_lidar['LocalTime'] = pd.to_datetime(df_lidar['LocalTime'])

    sdate = datetime.fromisoformat(sdate)
    edate = datetime.fromisoformat(edate)

    for i in range(0, 24, 2):
        rng = str(i) + '-' + str(i+2)
        h_range = np.append(h_range, rng)

    data = pd.DataFrame(columns=['Date', 'Hours', 'Total Volume SS', 'Total Volume MCO'])
    rwn = 0
    for j in range((edate-sdate).days+1):
        vdate = sdate + timedelta(days=j)
        for i in h_range:
            cnt = int(i.split('-')[0])
            vol_total = df_lidar.loc[((df_lidar['LocalTime'].dt.hour == cnt) | (df_lidar['LocalTime'].dt.hour == cnt+1)) & (df_lidar['ConveyorId'] == 'f03ce602-c521-4a43-af5c-367e4d8fed76') & (df_lidar['LocalTime'].dt.normalize() == vdate), 'Volume'].sum()
            vol_total2 = df_lidar.loc[((df_lidar['LocalTime'].dt.hour == cnt) | (df_lidar['LocalTime'].dt.hour == cnt+1)) & (df_lidar['ConveyorId'] == '31634244-066c-4403-82ff-75911babf124') & (df_lidar['LocalTime'].dt.normalize() == vdate), 'Volume'].sum()
            data.loc[rwn, 'Date'] = datetime.date(vdate)
            data.loc[rwn, 'Hours'] = i
            data.loc[rwn, 'Total Volume SS'] = vol_total / 1000000000
            data.loc[rwn, 'Total Volume MCO'] = vol_total2 / 1000000000
            rwn += 1


    return data