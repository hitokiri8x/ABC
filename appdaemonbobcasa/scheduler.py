from appdaemon.plugins.hass.hassapi import Hass


# noinspection PyUnusedLocal
class Schedule(Hass):
    """
    functions that are triggered by time
    """

    def initialize(self):
        pass

    def reset_sensors(self, entity, attribute, old, new, kwargs):
        pass

    def going_sleep(self, entity, attribute, old, new, kwargs):
        pass
