from contextlib import asynccontextmanager
import logging
from power_logger import PowerDataLogger
from fastapi import FastAPI
from threading import Thread
import time

from processor import PowerDataProcessor
from fetcher import PowerDataFetcher


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background thread for data polling
    # NOTE: thread failures might happen in production environments
    thread = Thread(target=poll_data, daemon=True)
    thread.start()
    yield


# Init of app
app = FastAPI(lifespan=lifespan)
log_level = logging.DEBUG
log = PowerDataLogger(name="PowerDataApplicationMain", level=log_level)
window_size_in_minutes = 5
processor = PowerDataProcessor(
    window_size_in_minutes=window_size_in_minutes, 
    averaging_column="SolarPower",
    log_level=log_level
)
fetcher = PowerDataFetcher(
    endpoint_url="https://api.energidataservice.dk/dataset/PowerSystemRightNow",
    log_level=log_level,
)


# Endpoints
@app.get("/latest")
def get_latest_data():
    return {
        "currentAverage": processor.get_current_average(),
        "currentWindow": processor.get_current_window()
    }

@app.get("/predict")
def get_ml_model_prediction():
    return {
        "predictedAverage": "42"
    }


# Polling function
def poll_data():
    while True:
        data = fetcher.fetch_data(window_size_in_minutes=window_size_in_minutes)
        processor.update_moving_average(data)
        time.sleep(60)
