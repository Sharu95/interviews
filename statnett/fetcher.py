from datetime import datetime, timedelta, timezone
import logging
import requests

from schema import MeasurementRecord
from power_logger import PowerDataLogger
import traceback


class PowerDataFetcher:
    def __init__(self, endpoint_url: str = None, log_level=logging.INFO):
        self.ENDPOINT_URL = endpoint_url
        self.log = PowerDataLogger(__class__.__name__, level=log_level)

    def fetch_data(self, window_size_in_minutes: int, limit: int) -> list[MeasurementRecord]:
        now = datetime.now(tz=timezone.utc)
        start = now - timedelta(minutes=window_size_in_minutes)
        tz = "UTC"
        params = {"timezone": tz, "start": start.strftime("%Y-%m-%dT%H:%M"), "limit": limit}
        try:
            res = requests.get(self.ENDPOINT_URL, params=params)
            self.log.debug("Requesting data from %s (timezone: %s): %s measurement(s)", start, tz, limit)
            res.raise_for_status()
            if res.status_code == 200:
                records = res.json().get("records", [])
                records = [MeasurementRecord(**item) for item in records]
                self.log.debug(records)
                return records
        except Exception as e:
            # NOTE: Push metrics for alerts, log error and return appropriate HTTP response code 500
            self.log.error("Error fetching data %s", e)
            traceback.print_exc()
        return []
