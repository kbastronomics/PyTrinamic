# Created on: 06.07.2021
# Author: LK

from PyTrinamic.features.Current import Current

class CurrentModule(Current):

    class __GROUPING:

        def __init__(self, parent):
            self.parent = parent

        def get_current_run(self, axis):
            return self.parent.get_axis_parameter(self.parent.APs.RunCurrent)

        def set_current_run(self, axis, value):
            self.parent.set_axis_parameter(self.parent.APs.RunCurrent, value)

        def get_current_standby(self, axis):
            return self.parent.get_axis_parameter(self.parent.APs.StandbyCurrent)

        def set_current_standby(self, axis, value):
            self.parent.set_axis_parameter(self.parent.APs.StandbyCurrent, value)

        # Properties
        current_run = property(get_current_run, set_current_run)
        current_standby = property(get_current_standby, set_current_standby)


    def __init__(self):
        self.Current = self.__GROUPING(self)
