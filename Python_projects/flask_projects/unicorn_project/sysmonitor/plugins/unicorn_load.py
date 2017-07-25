# -*- coding: utf-8 -*-

"""Load plugin."""

# Import system libs
import os

# Import  libs
from unicorn_core import Plugin as CorePlugin
from unicorn_plugin import UnicornPlugin

# SNMP OID
# 1 minute Load: .1.3.6.1.4.1.2021.10.1.3.1
# 5 minute Load: .1.3.6.1.4.1.2021.10.1.3.2
# 15 minute Load: .1.3.6.1.4.1.2021.10.1.3.3
snmp_oid = {'min1': '1.3.6.1.4.1.2021.10.1.3.1',
            'min5': '1.3.6.1.4.1.2021.10.1.3.2',
            'min15': '1.3.6.1.4.1.2021.10.1.3.3'}

# Define the history items list
# All items in this list will be historised if the --enable-history tag is set
# 'color' define the graph color in #RGB format
items_history_list = [{'name': 'min1', 'color': '#0000FF'},
                      {'name': 'min5', 'color': '#0000AA'},
                      {'name': 'min15', 'color': '#000044'}]


class Plugin(UnicornPlugin):

    """ load plugin.

    stats is a dict
    """

    def __init__(self, args=None):
        """Init the plugin."""
        UnicornPlugin.__init__(
            self, args=args, items_history_list=items_history_list)

        # We want to display the stat in the curse interface
        self.display_curse = True

        # Init stats
        self.reset()

        # Call CorePlugin in order to display the core number
        try:
            self.nb_log_core = CorePlugin(args=self.args).update()["log"]
        except Exception:
            self.nb_log_core = 0

    def reset(self):
        """Reset/init the stats."""
        self.stats = {}

    def update(self):
        """Update load stats."""
        # Reset stats
        self.reset()

        if self.input_method == 'local':
            # Update stats using the standard system lib

            # Get the load using the os standard lib
            try:
                load = os.getloadavg()
            except (OSError, AttributeError):
                self.stats = {}
            else:
                self.stats = {'min1': load[0],
                              'min5': load[1],
                              'min15': load[2],
                              'cpucore': self.nb_log_core}
        elif self.input_method == 'snmp':
            # Update stats using SNMP
            self.stats = self.get_stats_snmp(snmp_oid=snmp_oid)

            if self.stats['min1'] == '':
                self.reset()
                return self.stats

            # Python 3 return a dict like:
            # {'min1': "b'0.08'", 'min5': "b'0.12'", 'min15': "b'0.15'"}
            try:
                iteritems = self.stats.iteritems()
            except AttributeError:
                iteritems = self.stats.items()
            for k, v in iteritems:
                self.stats[k] = float(v)

            self.stats['cpucore'] = self.nb_log_core

        # Update the history list
        self.update_stats_history()

        # Update the view
        self.update_views()

        return self.stats

    def update_views(self):
        """Update stats views."""
        # Call the father's method
        UnicornPlugin.update_views(self)

        # Add specifics informations
        try:
            # Alert and log
            self.views['min15']['decoration'] = self.get_alert_log(self.stats['min15'], maximum=100 * self.stats['cpucore'])
            # Alert onlynb_log_core
            self.views['min5']['decoration'] = self.get_alert(self.stats['min5'], maximum=100 * self.stats['cpucore'])
        except KeyError:
            # try/except mandatory for Windows compatibility (no load stats)
            pass

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        # Init the return message
        ret = []

        # Only process if stats exist...
        if not self.stats:
            return ret

        # Build the string message
        # Header
        msg = '{0:8}'.format('LOAD')
        ret.append(self.curse_add_line(msg, "TITLE"))
        # Core number
        if self.stats['cpucore'] > 0:
            msg = '{0}-core'.format(int(self.stats['cpucore']))
            ret.append(self.curse_add_line(msg))
        # New line
        ret.append(self.curse_new_line())
        # 1min load
        msg = '{0:8}'.format('1 min:')
        ret.append(self.curse_add_line(msg))
        msg = '{0:>6.2f}'.format(self.stats['min1'])
        ret.append(self.curse_add_line(msg))
        # New line
        ret.append(self.curse_new_line())
        # 5min load
        msg = '{0:8}'.format('5 min:')
        ret.append(self.curse_add_line(msg))
        msg = '{0:>6.2f}'.format(self.stats['min5'])
        ret.append(self.curse_add_line(
            msg, self.get_views(key='min5', option='decoration')))
        # New line
        ret.append(self.curse_new_line())
        # 15min load
        msg = '{0:8}'.format('15 min:')
        ret.append(self.curse_add_line(msg))
        msg = '{0:>6.2f}'.format(self.stats['min15'])
        ret.append(self.curse_add_line(
            msg, self.get_views(key='min15', option='decoration')))

        return ret
