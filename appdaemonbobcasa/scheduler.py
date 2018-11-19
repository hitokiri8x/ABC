import datetime
from appdaemon.plugins.hass.hassapi import Hass
from sensor import Sensor
import holidays


class MyHolidays(holidays.Italy):
    def _populate(self, year):
        holidays.Italy._populate(self, year)
        self[datetime.date(year, 1, 19)] = "custom day "


# noinspection PyUnusedLocal
class Schedule(Hass):
    """
    functions that are triggered by time ( mostly on daily basis )
    """

    # noinspection PyAttributeOutsideInit
    def initialize(self):
        self.my_holidays = MyHolidays()
        early_morning = datetime.time(int(self.args['early_morning_h']), int(self.args['early_morning_min']), 0)
        late_morning = datetime.time(int(self.args['late_morning_h']), int(self.args['late_morning_min']), 0)
        sleep_time = datetime.time(1, 0, 0)  # 1:00 AM
        self.run_daily(self.reset_sensors_workday, early_morning)
        self.run_daily(self.reset_sensors_holiday, late_morning)
        self.run_daily(self.going_sleep, sleep_time)
        self.sensor_living = self.get_app('globals').sensor_living  # type: Sensor
        self.sensor_bedroom = self.get_app('globals').sensor_bedroom  # type: Sensor
        self.sensor_spare = self.get_app('globals').sensor_spare  # type: Sensor

    def reset_sensors_workday(self, entity, attribute, old, new, kwargs):
        """
        reset sensors before wake-up time checking that is not an holiday or a week-end day
        """
        if datetime.date.today() not in self.my_holidays and datetime.date.today().weekday() < 5:
            self.sensor_living.set_state_boolean(True)
            self.sensor_bedroom.set_state_boolean(True)
            self.sensor_spare.set_state_boolean(True)
        else:
            return

    def reset_sensors_holiday(self, entity, attribute, old, new, kwargs):
        """
        reset sensors before wake-up time checking that is an holiday or a week-end day
        """
        if datetime.date.today() in self.my_holidays or datetime.date.today().weekday() >= 5:
            self.sensor_living.set_state_boolean(True)
            self.sensor_bedroom.set_state_boolean(True)
            self.sensor_spare.set_state_boolean(True)
        else:
            return

    def going_sleep(self, entity, attribute, old, new, kwargs):
        """
        prevents lights to turn on when going to bathroom or to drink in the night
        """
        self.sensor_living.set_state_boolean(False)
        self.sensor_bedroom.set_state_boolean(False)
