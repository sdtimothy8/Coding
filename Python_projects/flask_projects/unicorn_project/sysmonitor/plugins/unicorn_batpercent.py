# -*- coding: utf-8 -*-

"""Battery plugin."""

# Import libs
from sysmonitor.core.unicorn_logging import logger
from unicorn_plugin import UnicornPlugin

# Batinfo library (optional; Linux-only)
try:
    import batinfo
except ImportError:
    logger.debug("Batinfo library not found. Unicon cannot grab battery info.")


class Plugin(UnicornPlugin):

    """ battery capacity plugin.

    stats is a list
    """

    def __init__(self, args=None):
        """Init the plugin."""
        UnicornPlugin.__init__(self, args=args)

        # Init the sensor class
        self.unicongrabbat = UniconGrabBat()

        # We do not want to display the stat in a dedicated area
        # The HDD temp is displayed within the sensors plugin
        self.display_curse = False

        # Init stats
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    @UnicornPlugin._log_result_decorator
    def update(self):
        """Update battery capacity stats using the input method."""
        # Reset stats
        self.reset()

        if self.input_method == 'local':
            # Update stats
            self.unicongrabbat.update()
            self.stats = self.unicongrabbat.get()

        elif self.input_method == 'snmp':
            # Update stats using SNMP
            # Not avalaible
            pass

        return self.stats


class UniconGrabBat(object):

    """Get batteries stats using the batinfo library."""

    def __init__(self):
        """Init batteries stats."""
        try:
            self.bat = batinfo.batteries()
            self.initok = True
            self.bat_list = []
            self.update()
        except Exception as e:
            self.initok = False
            logger.debug("Cannot init unicongrabbat class (%s)" % e)

    def update(self):
        """Update the stats."""
        if self.initok:
            self.bat.update()
            self.bat_list = [{
                'label': 'Battery',
                'value': self.battery_percent,
                'unit': '%'}]
        else:
            self.bat_list = []

    def get(self):
        """Get the stats."""
        return self.bat_list

    @property
    def battery_percent(self):
        """Get batteries capacity percent."""
        if not self.initok or not self.bat.stat:
            return []

        # Init the bsum (sum of percent)
        # and Loop over batteries (yes a computer could have more than 1 battery)
        bsum = 0
        for b in self.bat.stat:
            try:
                bsum += int(b.capacity)
            except ValueError:
                return []

        # Return the global percent
        return int(bsum / len(self.bat.stat))
