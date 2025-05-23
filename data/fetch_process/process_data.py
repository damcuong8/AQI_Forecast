import pandas as pd


# Function to calculate AQI for pollutants
def calculate_all_aqi(concentrations):
    breakpoints = {
        "CO": [(0, 5039, 0, 50), (5039, 10765, 51, 100), (10765, 14200, 101, 150),
               (14200, 17636, 151, 200), (17636, 34814, 201, 300), (34814, float('inf'), 301, 500)],
        "NO2": [(0, 99.7, 0, 50), (101.6, 188.12, 51, 100), (190, 677.3, 101, 150),
                (679.2, 1221, 151, 200), (1222.9, 2349.9, 201, 300), (2351.7, float('inf'), 301, 500)],
        "PM10": [(0, 54, 0, 50), (55, 154, 51, 100), (155, 254, 101, 150),
                 (255, 355, 151, 200), (355, 424, 201, 300), (425, float('inf'), 301, 500)],
        "PM2.5": [(0, 9, 0, 50), (9.1, 35.4, 51, 100), (35.5, 55.4, 101, 150),
                  (55.5, 125.4, 151, 200), (125.5, 225.4, 201, 300), (225.5, float('inf'), 301, 500)],
    }

    def calculate_aqi_single(concentration, pollutant):
        for bp in breakpoints[pollutant]:
            if bp[0] <= concentration <= bp[1]:
                return round((bp[3] - bp[2]) / (bp[1] - bp[0]) * (concentration - bp[0]) + bp[2])
        return 0

    aqi_results = {}
    for pollutant, concentration in concentrations.items():
        if pollutant in breakpoints:
            aqi_results[pollutant] = calculate_aqi_single(concentration, pollutant)
        else:
            aqi_results[pollutant] = None
    return aqi_results


raw_df = pd.read_csv('raw_data.csv')
aqi_data = pd.read_csv('../aqi_data.csv')
print(aqi_data.head())

for i in range(len(raw_df)):
    concentrations = {
        "CO": raw_df.loc[i, "CO"],
        "NO2": raw_df.loc[i, "NO2"],
        "PM10": raw_df.loc[i, "PM10"],
        "PM2.5": raw_df.loc[i, "PM2.5"]
    }
    aqi_results = calculate_all_aqi(concentrations)
    for pollutant, aqi in aqi_results.items():
        raw_df.loc[i, f"AQI_{pollutant}"] = aqi

raw_df['AQI'] = raw_df[['AQI_CO', 'AQI_NO2', 'AQI_PM10', 'AQI_PM2.5']].max(axis=1)
print(raw_df.tail())
aqi_data = pd.concat([aqi_data, raw_df], ignore_index=True)
aqi_data.to_csv('../aqi_data.csv', index=False)










