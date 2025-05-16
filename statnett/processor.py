from collections import deque
import logging
from statistics import mean

from schema import MeasurementRecord
from power_logger import PowerDataLogger


class PowerDataProcessor:
    def __init__(
        self, window_size_in_minutes: int, averaging_column: str, log_level=logging.INFO
    ):
        self.window = deque(maxlen=window_size_in_minutes)
        self.current_average = None
        # By doing this we ensure some sort of type safety and can fail fast on initialization of app
        # Instead of failing when calculating the average
        self.averaging_column = MeasurementRecord.__dataclass_fields__[
            averaging_column
        ].name
        self.log = PowerDataLogger(__class__.__name__, level=log_level)

    def update_moving_average(self, data: list[MeasurementRecord]):
        if data:
            self.log.debug(
                "Updating moving average window for '%s'", self.averaging_column
            )
            self.window.extend(sorted(data, key=lambda x: x.Minutes1UTC))
            self.current_average = mean(
                [getattr(record, self.averaging_column) for record in self.window]
            )
            self.log.debug(
                "New average for '%s': %s", self.averaging_column, self.current_average
            )

    def get_current_average(self):
        return self.current_average or None

    def get_current_window(self):
        if self.window:
            return [
                {
                    self.averaging_column: getattr(record, self.averaging_column),
                    "timestamp": record.Minutes1UTC,
                }
                for record in self.window
            ]
        return []
