# -*- coding: utf-8 -*-

"""Process count plugin."""

# Import libs
from sysmonitor.core.unicon_processes import unicon_processes
from sysmonitor.plugins.unicorn_plugin import UnicornPlugin

# Note: history items list is not compliant with process count
#       if a filter is applyed, the graph will show the filtered processes count


class Plugin(UnicornPlugin):

    """ process count plugin.

    stats is a list
    """

    def __init__(self, args=None):
        """Init the plugin."""
        UnicornPlugin.__init__(self, args=args)

        # We want to display the stat in the curse interface
        self.display_curse = True

        # Note: 'unicon_processes' is already init in the unicon_processes.py script

    def reset(self):
        """Reset/init the stats."""
        self.stats = {}

    def update(self):
        """Update processes stats using the input method."""
        # Reset stats
        self.reset()

        if self.input_method == 'local':
            # Update stats using the standard system lib
            # Here, update is call for processcount AND processlist
            unicon_processes.update()

            # Return the processes count
            self.stats = unicon_processes.getcount()
        elif self.input_method == 'snmp':
            # Update stats using SNMP
            # !!! TODO
            pass

        return self.stats

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        # Init the return message
        ret = []

        # Only process if stats exist and display plugin enable...
        if args.disable_process:
            msg = "PROCESSES DISABLED (press 'z' to display)"
            ret.append(self.curse_add_line(msg))
            return ret

        if not self.stats:
            return ret

        # Display the filter (if it exists)
        if unicon_processes.process_filter is not None:
            msg = 'Processes filter:'
            ret.append(self.curse_add_line(msg, "TITLE"))
            msg = ' {0} '.format(unicon_processes.process_filter)
            ret.append(self.curse_add_line(msg, "FILTER"))
            msg = '(press ENTER to edit)'
            ret.append(self.curse_add_line(msg))
            ret.append(self.curse_new_line())

        # Build the string message
        # Header
        msg = 'TASKS'
        ret.append(self.curse_add_line(msg, "TITLE"))
        # Compute processes
        other = self.stats['total']
        msg = '{0:>4}'.format(self.stats['total'])
        ret.append(self.curse_add_line(msg))

        if 'thread' in self.stats:
            msg = ' ({0} thr),'.format(self.stats['thread'])
            ret.append(self.curse_add_line(msg))

        if 'running' in self.stats:
            other -= self.stats['running']
            msg = ' {0} run,'.format(self.stats['running'])
            ret.append(self.curse_add_line(msg))

        if 'sleeping' in self.stats:
            other -= self.stats['sleeping']
            msg = ' {0} slp,'.format(self.stats['sleeping'])
            ret.append(self.curse_add_line(msg))

        msg = ' {0} oth '.format(other)
        ret.append(self.curse_add_line(msg))

        # Display sort information
        if unicon_processes.auto_sort:
            msg = 'sorted automatically'
            ret.append(self.curse_add_line(msg))
            msg = ' by {0}'.format(unicon_processes.sort_key)
            ret.append(self.curse_add_line(msg))
        else:
            msg = 'sorted by {0}'.format(unicon_processes.sort_key)
            ret.append(self.curse_add_line(msg))
        ret[-1]["msg"] += ", %s view" % ("tree" if unicon_processes.is_tree_enabled() else "flat")

        # Return the message with decoration
        return ret
