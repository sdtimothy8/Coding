# -*- coding: utf-8 -*-

"""Per-CPU plugin."""

from sysmonitor.plugins.unicorn_plugin import UnicornPlugin

import psutil


class Plugin(UnicornPlugin):

    """ per-CPU plugin.

    'stats' is a list of dictionaries that contain the utilization percentages
    for each CPU.
    """

    def __init__(self, args=None):
        """Init the plugin."""
        UnicornPlugin.__init__(self, args=args)

        # We want to display the stat in the curse interface
        self.display_curse = True

        # Init stats
        self.reset()

    def get_key(self):
        """Return the key of the list."""
        return 'cpu_number'

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    def update(self):
        """Update per-CPU stats using the input method."""
        # Reset stats
        self.reset()

        # Grab per-CPU stats using psutil's cpu_percent(percpu=True) and
        # cpu_times_percent(percpu=True) methods
        if self.input_method == 'local':
            percpu_times_percent = psutil.cpu_times_percent(interval=0.0, percpu=True)
            for cpu_number, cputimes in enumerate(percpu_times_percent):
                cpu = {'key': self.get_key(),
                       'cpu_number': cpu_number,
                       'total': round(100 - cputimes.idle, 1),
                       'user': cputimes.user,
                       'system': cputimes.system,
                       'idle': cputimes.idle}
                # The following stats are for API purposes only
                if hasattr(cputimes, 'nice'):
                    cpu['nice'] = cputimes.nice
                if hasattr(cputimes, 'iowait'):
                    cpu['iowait'] = cputimes.iowait
                if hasattr(cputimes, 'irq'):
                    cpu['irq'] = cputimes.irq
                if hasattr(cputimes, 'softirq'):
                    cpu['softirq'] = cputimes.softirq
                if hasattr(cputimes, 'steal'):
                    cpu['steal'] = cputimes.steal
                if hasattr(cputimes, 'guest'):
                    cpu['guest'] = cputimes.guest
                if hasattr(cputimes, 'guest_nice'):
                    cpu['guest_nice'] = cputimes.guest_nice
                self.stats.append(cpu)
        else:
            # Update stats using SNMP
            pass

        return self.stats

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        # Init the return message
        ret = []

        # No per CPU stat ? Exit...
        if not self.stats:
            msg = 'PER CPU not available'
            ret.append(self.curse_add_line(msg, "TITLE"))
            return ret

        # Build the string message
        # Header
        msg = '{0:8}'.format('PER CPU')
        ret.append(self.curse_add_line(msg, "TITLE"))

        # Total per-CPU usage
        for cpu in self.stats:
            msg = '{0:>6}%'.format(cpu['total'])
            ret.append(self.curse_add_line(msg))

        # User per-CPU
        ret.append(self.curse_new_line())
        msg = '{0:8}'.format('user:')
        ret.append(self.curse_add_line(msg))
        for cpu in self.stats:
            msg = '{0:>6}%'.format(cpu['user'])
            ret.append(self.curse_add_line(msg, self.get_alert(cpu['user'], header="user")))

        # System per-CPU
        ret.append(self.curse_new_line())
        msg = '{0:8}'.format('system:')
        ret.append(self.curse_add_line(msg))
        for cpu in self.stats:
            msg = '{0:>6}%'.format(cpu['system'])
            ret.append(self.curse_add_line(msg, self.get_alert(cpu['system'], header="system")))

        # Idle per-CPU
        ret.append(self.curse_new_line())
        msg = '{0:8}'.format('idle:')
        ret.append(self.curse_add_line(msg))
        for cpu in self.stats:
            msg = '{0:>6}%'.format(cpu['idle'])
            ret.append(self.curse_add_line(msg))

        # Return the message with decoration
        return ret
