from appdaemon.plugins.hass.hassapi import Hass
import requests
import json


class Sensor(Hass):

    def __init__(self, ad, name, logger, error, args, config, app_config, global_vars, entity=None, hue_id=None):
        super().__init__(ad, name, logger, error, args, config, app_config, global_vars)
        if entity is None and hue_id is None:
            return
        self.hue_url = self.args['hue_url']
        self.hue_api = self.args['hue_api']
        self.entity = str(entity)
        self.hue_id = str(hue_id)
        self.hue_value = self.get_state_hue()
        self.set_state_boolean(self.hue_value)
        self.entity_value = self.get_state_boolean()

    def initialize(self):
        pass

    def get_state_boolean(self) -> bool:
        """
        return the state of the input_boolean in hass
        :return: true or false
        """
        if self.get_state(self.entity) == 'on':
            return True
        else:
            return False

    def get_state_hue(self) -> bool:
        """
        get the state of the sensor from hue bridge
        """
        try:
            r = requests.get(self.hue_url + self.hue_api + r'/sensors/' + self.hue_id)
            return r.json()['config']['on']
        except Exception as ex:
            print(ex)

    def set_state_boolean(self, status: bool):
        if status:
            self.turn_on(self.entity)
        else:
            self.turn_off(self.entity)

    def set_hue(self, **kwargs):
        payload = kwargs
        requests.put(self.hue_url + self.hue_api + r'/sensors/' + self.hue_id + '/config', json.dumps(payload))
