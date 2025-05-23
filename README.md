# 🌍 AQI Forecast - Air Quality Prediction in "Chi cục BVMT"

AQI Forecast is a web application that predicts air quality using Deep Learning. This project uses LSTM models to forecast AQI (Air Quality Index) based on environmental factors such as PM2.5, PM10, CO, NO2, temperature, humidity, and wind speed.

## ✨ Key Features

- 🔮 **AQI Prediction**: Forecast air quality for the next 72 hours
- 📊 **Data Visualization**: Display charts and colors according to AQI standards
- 🌡️ **Multi-parameter Monitoring**: Track PM2.5, PM10, CO, NO2, temperature, humidity, wind speed
- 🐳 **Docker Support**: Easy deployment with Docker

## 🚀 Installation & Usage

### Method 1: Run directly with Python

#### System Requirements
- Python 3.10+
- pip

### Run application:
```bash
python app.py
```

5. **Access application:**
Open browser and go to: `http://localhost:5000`

### Method 2: Using Docker

#### Requirements
- Docker
- Docker Compose

#### Running Steps

1. **Clone repository:**
```bash
git clone https://github.com/damcuong8/AQI_Forcast.git
cd AQI_Forcast
```

2. **Run with Docker Compose:**
```bash
docker-compose up --build
```

3. **Access application:**
Open browser and go to: `http://localhost:5000`

## 🧠 Machine Learning Model

For detailed model architecture, training process, and performance analysis, please visit:
**📊 [Complete Model Development & Training Process on Kaggle](https://www.kaggle.com/code/damcuong/aqi-forcast)**

### Model Architecture
- **Model Type**: LSTM with Keras/TensorFlow
- **Input Features**: 8 features (PM2.5, CO, PM10, NO2, Temperature, Humidity, Wind Speed, AQI)
- **Time Window**: 480 time steps
- **Output**: AQI prediction for next 72 hours

### Data Preprocessing
- **Normalization**: MinMaxScaler for numerical features
- **Sliding Window**: Using 480 time steps for prediction
- **Features**: CO, NO2, PM10, PM2.5, Temperature, Humidity, Wind Speed

## 🛠️ Technologies Used

### Backend
- **Flask**: Web framework
- **TensorFlow/Keras**: Deep Learning
- **scikit-learn**: Machine Learning utilities
- **pandas**: Data manipulation
- **numpy**: Numerical computing

### Frontend
- **HTML/CSS**: Web interface
- **Jinja2**: Template engine

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## 📈 Model Performance

Mean Absolute Percentage Error (MAPE): 0.78048

**Made with ❤️ for cleaner air quality monitoring** 