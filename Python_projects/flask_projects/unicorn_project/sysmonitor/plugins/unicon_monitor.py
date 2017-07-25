# -*- coding: utf-8 -*-

"""Monitor plugin."""

# Import  lib
from sysmonitor.core.unicon_monitor_list import MonitorList as uniconMonitorList
from sysmonitor.plugins.unicorn_plugin import UnicornPlugin


class Plugin(UnicornPlugin):

    """ monitor plugin."""

    def __init__(self, args=None):
        """Init the plugin."""
        UnicornPlugin.__init__(self, args=args)

        # We want to display the stat in the curse interface
        self.display_curse = True

        # Init stats
        self.unicon_monitors = None
        self.stats = []

    def load_limits(self, config):
        """Load the monitored list from the config file, if it exists."""
        self.unicon_monitors = uniconMonitorList(config)

    def update(self):
        """Update the monitored list."""
        if self.input_method == 'local':
            # Monitor list only available in a full unicon environment
            # Check if the unicon_monitor instance is init
            if self.unicon_monitors is None:
                return self.stats

            # Update the monitored list (result of command)
            self.unicon_monitors.update()

            # Put it on the stats var
            self.stats = self.unicon_monitors.get()
        else:
            pass

        return self.stats

    def get_alert(self, nbprocess=0, countmin=None, countmax=None, header="", log=False):
        """Return the alert status relative to the process number."""
        if nbprocess is None:
            return 'OK'
        if countmin is None:
            countmin = nbprocess
        if countmax is None:
            countmax = nbprocess
        if nbprocess > 0:
            if int(countmin) <= int(nbprocess) <= int(countmax):
                return 'OK'
            else:
                return 'WARNING'
        else:
            if int(countmin) == 0:
                return 'OK'
            else:
                return 'CRITICAL'

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        # Init the return message
        ret = []

        # Only process if stats exist and display plugin enable...
        if not self.stats or args.disable_process:
            return ret

        # Build the string message
        for m in self.stats:
            msg = '{0:<16} '.format(m['description'])
            ret.append(self.curse_add_line(
                msg, self.get_alert(m['count'], m['countmin'], m['countmax'])))
            msg = '{0:<3} '.format(m['count'] if m['count'] > 1 else '')
            ret.append(self.curse_add_line(msg))
            msg = '{0:13} '.format('RUNNING' if m['count'] >= 1 else 'NOT RUNNING')
            ret.append(self.curse_add_line(msg))
            # Decode to UTF8 (only for Python 3)
            try:
                msg = m['result'].decode('utf-8') if m['count'] >= 1 else ''
            except (UnicodeError, AttributeError):
                try:
                    msg = m['result'] if m['count'] >= 1 else ''
                except UnicodeError:
                    msg = m['result'].encode('utf-8') if m['count'] >= 1 else ''
            ret.append(self.curse_add_line(msg, optional=True, splittable=True))
            ret.append(self.curse_new_line())

        # Delete the last empty line
        try:
            ret.pop()
        except IndexError:
            pass

        return ret
