import csv
import pytz
import requests
from openaq import OpenAQ
from datetime import datetime, timedelta

# Khởi tạo OpenAQ client
openaq_client = OpenAQ(api_key='your_openaq_api_key')

# API key của OpenWeatherMap
owm_api_key = "your_openweathermap_api_key"
owm_url = "https://history.openweathermap.org/data/2.5/history/city"

# Tọa độ Hà Nội
params = {
    "lat": 21.01519,
    "lon": 105.79991,
    "type": "hour",
    "units": "metric",
    "appid": owm_api_key,
}

# Thời gian bắt đầu và kết thúc
start_datetime = datetime.strptime("2024-12-14 03:00:00", "%Y-%m-%d %H:%M:%S")
now = datetime.now()
end_datetime = now.replace(minute=0, second=0, microsecond=0)

utc_tz = pytz.utc
local_tz = pytz.timezone("Asia/Bangkok")

# File lưu dữ liệu
output_file = "raw_data.csv"

with open(output_file, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    if file.tell() == 0:
        writer.writerow(["utc_time", "local_time",  "PM2.5", "CO", "PM10", "NO2", "Temperature", "Humidity", "Wind Speed"])

    # Lấy dữ liệu OpenAQ
    sensor_ids = {"PM2.5": 7772032, "CO": 7772024, "PM10": 7772048, "NO2": 7888636}
    current_datetime = start_datetime

    while current_datetime <= end_datetime:
        row_data = {"local_time": current_datetime.strftime("%Y-%m-%d %H:%M:%S")}

        # Thêm thời gian UTC
        utc_time = current_datetime.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S")
        row_data["utc_time"] = utc_time

        # Mặc định tất cả giá trị là None (hoặc null)
        for param in sensor_ids.keys():
            row_data[param] = None
        row_data["Temperature"] = None
        row_data["Humidity"] = None
        row_data["Wind Speed"] = None

        # Lấy dữ liệu từ OpenAQ
        for param, sensor_id in sensor_ids.items():
            measurements = openaq_client.measurements.list(
                sensors_id=sensor_id,
                rollup="hourly",
                datetime_from=current_datetime.isoformat() + "Z",
                datetime_to=(current_datetime + timedelta(hours=1)).isoformat() + "Z",
            )
            if measurements.results:
                row_data[param] = measurements.results[0].value

        # Lấy dữ liệu từ OpenWeatherMap
        owm_params = params.copy()
        owm_params["start"] = int(current_datetime.timestamp())
        owm_params["end"] = int((current_datetime + timedelta(hours=1)).timestamp())

        response = requests.get(owm_url, params=owm_params)
        if response.status_code == 200:
            weather_data = response.json()
            if weather_data["list"]:
                weather = weather_data["list"][0]
                row_data["Temperature"] = weather["main"]["temp"]
                row_data["Humidity"] = weather["main"]["humidity"]
                row_data["Wind Speed"] = weather.get("wind", {}).get("speed", None)

        # Ghi dữ liệu vào file
        writer.writerow([
            row_data["utc_time"],
            row_data["local_time"],
            row_data.get("PM2.5"),
            row_data.get("CO"),
            row_data.get("PM10"),
            row_data.get("NO2"),
            row_data.get("Temperature"),
            row_data.get("Humidity"),
            row_data.get("Wind Speed"),
        ])

        # Tăng thời gian
        current_datetime += timedelta(hours=1)

print(f"Dữ liệu đã được lưu vào {output_file}.")
# Close the OpenAQ client
openaq_client.close()
