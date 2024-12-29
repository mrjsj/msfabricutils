from dataclasses import dataclass
from typing import Annotated, List, Literal

from cyclopts import Parameter

from .complex_type import ComplexType


@dataclass
class ScheduleConfig(ComplexType):
    type: Annotated[Literal["Cron", "Daily", "Weekly"], Parameter(help="The type of the schedule config.")]

    # Cron
    start_date_time: Annotated[str, Parameter(help="The start date time of the schedule config.")] = None
    end_date_time: Annotated[str, Parameter(help="The end date time of the schedule config.")] = None
    local_time_zone_id: Annotated[str, Parameter(help="The local time zone ID of the schedule config.")] = None
    interval: Annotated[int, Parameter(help="The time interval in minutes")] = None

    # Daily
    times: Annotated[List[str], Parameter(help="A list of time slots in hh:mm format", consume_multiple=True)] = None

    # Weekly
    weekdays: Annotated[
        List[Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]],
        Parameter(help="A list of weekdays", consume_multiple=True),
    ] = None

    def to_dict(self):
        payload = {}
        if self.type:
            payload["type"] = self.type
        if self.start_date_time:
            payload["startDateTime"] = self.start_date_time
        if self.end_date_time:
            payload["endDateTime"] = self.end_date_time
        if self.local_time_zone_id:
            payload["localTimeZoneId"] = self.local_time_zone_id
        if self.interval:
            payload["interval"] = self.interval
        if self.times:
            payload["times"] = self.times
        if self.weekdays:
            payload["weekdays"] = self.weekdays
        return payload
