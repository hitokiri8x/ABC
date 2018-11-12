from appdaemon.plugins.hass.hassapi import Hass
from appdaemonbobcasa.sensor import Sensor


# noinspection PyUnusedLocal
class Action(Hass):

    # noinspection PyAttributeOutsideInit
    def initialize(self):
        """
        initialize globals sensors and define listener for actions to perform
        """
        watch_tv = self.args['watch_tv']
        cleaning = self.args['cleaning']
        self.sensor_living = self.get_app('globals').sensor_living  # type: Sensor
        self.sensor_bedroom = self.get_app('globals').sensor_bedroom  # type: Sensor
        self.sensor_spare = self.get_app('globals').sensor_spare  # type: Sensor
        self.listen_state(self.watching_tv, watch_tv, new="on")
        self.listen_state(self.stop_watching, watch_tv, new="off")
        self.listen_state(self.clean_on, cleaning, new='on')
        self.listen_state(self.clean_off, cleaning, new='off')

    def watching_tv(self, entity, attribute, old, new, kwargs):
        """
        turn off living room sensor and light
        """
        self.sensor_living.set_state_boolean(False)
        self.turn_off(self.args['entity_light_livingroom'])

    def stop_watching(self, entity, attribute, old, new, kwargs):
        """
        turn on living room sensor
        """
        self.sensor_living.set_state_boolean(True)

    def clean_on(self, entity, attribute, old, new, kwargs):
        """
        turn on all lights and turn off all sensors
        """
        self.call_service("light/turn_on", entity_id="group.all_lights")
        self.sensor_living.set_state_boolean(False)
        self.sensor_bedroom.set_state_boolean(False)
        self.sensor_spare.set_state_boolean(False)

    def clean_off(self, entity, attribute, old, new, kwargs):
        """
        restore all sensors to on
        """
        self.sensor_living.set_state_boolean(True)
        self.sensor_bedroom.set_state_boolean(True)
        self.sensor_spare.set_state_boolean(True)
