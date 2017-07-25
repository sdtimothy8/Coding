# -*- coding: utf-8 -*-

"""Manage the standalone session."""

from time import sleep

from sysmonitor.core.unicorn_globals import is_windows
from sysmonitor.core.unicorn_logging import logger
from unicon_processes import unicon_processes
from unicon_stats import UniconStats


class UniconStandalone(object):

    """This class creates and manages the  standalone session."""

    def __init__(self, config=None, args=None):
        # Quiet mode
        self._quiet = args.quiet
        self.refresh_time = args.time

        # Init stats
        self.stats = UniconStats(config=config, args=args)

        # If process extended stats is disabled by user
        if not args.enable_process_extended:
            logger.debug("Extended stats for top process are disabled")
            unicon_processes.disable_extended()
        else:
            logger.debug("Extended stats for top process are enabled")
            unicon_processes.enable_extended()

        # Manage optionnal process filter
        if args.process_filter is not None:
            unicon_processes.process_filter = args.process_filter

        if (not is_windows) and args.no_kernel_threads:
            # Ignore kernel threads in process list
            unicon_processes.disable_kernel_threads()

        try:
            if args.process_tree:
                # Enable process tree view
                unicon_processes.enable_tree()
        except AttributeError:
            pass

        # Initial system informations update
        self.stats.update()

        if self.quiet:
            logger.info("Quiet mode is ON: Nothing will be displayed")
            # In quiet mode, nothing is displayed
            unicon_processes.max_processes = 0
        else:
            # Default number of processes to displayed is set to 50
            unicon_processes.max_processes = 50

    @property
    def quiet(self):
        return self._quiet

    def __serve_forever(self):
        """Main loop for the CLI."""
        while True:
            # Update system informations
            self.stats.update()

            # if not self.quiet:
            #     # Update the screen
            #     # self.screen.update(self.stats)
            # else:
            #     # Wait...
            #     sleep(self.refresh_time)

            # Export stats using export modules
            self.stats.export(self.stats)

    def serve_forever(self):
        """Wrapper to the serve_forever function.

        This function will restore the terminal to a sane state
        before re-raising the exception and generating a traceback.
        """
        try:
            return self.__serve_forever()
        finally:
            self.end()

    def end(self):
        """End of the standalone CLI."""
        # if not self.quiet:
        # self.screen.end()

        # Exit from export modules
        self.stats.end()
