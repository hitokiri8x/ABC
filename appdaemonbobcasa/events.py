from appdaemon.plugins.hass.hassapi import Hass


# noinspection PyUnusedLocal
class Event(Hass):
    """
    functions that are triggered by external events( mail, router, sensors)
    """

    def initialize(self):
        pass

    def going_work(self, entity, attribute, old, new, kwargs):
        pass

    def coming_home(self, entity, attribute, old, new, kwargs):
        pass
