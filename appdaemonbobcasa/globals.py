from appdaemon.plugins.hass.hassapi import Hass
from appdaemonbobcasa.sensor import Sensor


class Global(Hass):

    # noinspection PyAttributeOutsideInit
    def initialize(self):
        entity_livingroom = self.args['entity_livingroom']
        entity_bedroom = self.args['entity_bedroom']
        entity_spare = self.args['entity_spare']
        hue_id_livingroom = self.args['hue_id_livingroom']
        hue_id_bedroom = self.args['hue_id_bedroom']
        hue_id_spare = self.args['hue_id_spare']

        self.sensor_living = Sensor(self.AD, self.name, self._logger, self._error, self.args, self.config,
                                    self.app_config, self.global_vars, entity_livingroom, hue_id_livingroom)
        self.sensor_bedroom = Sensor(self.AD, self.name, self._logger, self._error, self.args, self.config,
                                     self.app_config, self.global_vars, entity_bedroom, hue_id_bedroom)
        self.sensor_spare = Sensor(self.AD, self.name, self._logger, self._error, self.args, self.config,
                                   self.app_config, self.global_vars, entity_spare, hue_id_spare)
        self.listen_state(self.toggle_sensor, entity_livingroom, item='sensor_living')
        self.listen_state(self.toggle_sensor, entity_bedroom, item='sensor_bedroom')
        self.listen_state(self.toggle_sensor, entity_spare, item='sensor_spare')

    # noinspection PyUnusedLocal
    def toggle_sensor(self, entity, attribute, old, new, kwargs):
        """
        make the toggle also effective on hue bridge
        :param entity: is the input boolean
        :param attribute:  not used
        :param old:  old value
        :param new:  new value
        :param kwargs: contains the name of the item to update that generated the call
        """
        item = getattr(self, kwargs['item'])
        if new == 'on':
            new = True
        else:
            new = False
        item.set_hue(on=new)
