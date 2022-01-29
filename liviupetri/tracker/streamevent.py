from liviupetri.whatsapp.helpers.status import Status
from liviupetri.whatsapp.helpers.logchannels import LogChannels

from colorama import Fore
from datetime import timedelta

ScreenColors = {
    'NORMAL_TEXT': Fore.WHITE,
    'INITIAL_STATUS': Fore.LIGHTBLUE_EX,
    'SETUP': Fore.LIGHTBLUE_EX,
    'ONLINE': Fore.LIGHTGREEN_EX,
    'OFFLINE': Fore.RED,
    'TYPING': Fore.LIGHTMAGENTA_EX,
    'RECORDING': Fore.MAGENTA,
    'NOT_DEFINED': Fore.LIGHTBLUE_EX,
    'LAST_SEEN': Fore.WHITE,
    'DURATION': Fore.LIGHTYELLOW_EX
}


def format_duration(d: timedelta) -> str:
    minutes, seconds = divmod(d.seconds, 60)
    return str(minutes) + 'm ' + str(seconds) + 's'


class StreamEvent:
    __channels = [LogChannels.SCREEN, LogChannels.FILE]
    __event = None
    __previous_event_duration = None
    __eventlist = [(None, None)]
    __logfile = None

    def __init__(self, event):
        self.__event = event
        self.__previous_event_duration: timedelta = self.__event.actual_timestamp - self.__event.previous_timestamp

    def stream_event(self):
        # always save in memory
        self.__eventlist.append((self.__event.actual_status, self.__event.actual_timestamp))
        # if configured display
        if LogChannels.SCREEN in self.__channels:
            self.print_status_change(self.__event.previous_status, self.__event.previous_timestamp,
                                     self.__event.actual_status, self.__event.actual_timestamp)
        # if configured save to a file
        if LogChannels.FILE in self.__channels:
            self.save_status_change_to_file(self.__event.previous_status, self.__event.previous_timestamp)

    def print_status(self, status: Status) -> str:
        return ScreenColors[status.name] + status.name + ScreenColors['NORMAL_TEXT']

    def print_status_change(self, previous_status, previous_timestamp, actual_status, actual_timestamp):
        print(ScreenColors['NORMAL_TEXT'] +
              'On: ' + previous_timestamp.strftime("%d/%m/%y at %H:%M:%S") +
              ', was <' + self.print_status(previous_status) + ">, for [" +
              ScreenColors['DURATION'] + format_duration(self.__previous_event_duration) + ScreenColors['NORMAL_TEXT'] +
              "] and went <" + self.print_status(actual_status) + "> on: " +
              actual_timestamp.strftime("%d/%m/%y at %H:%M:%S") + ScreenColors['NORMAL_TEXT'])

    def save_status_change_to_file(self, actual_status, actual_timestamp):
        # TODO: change the hard coding of the output file
        logfile = open("WAlogfile_001.log", "a")
        logfile.write(actual_status.name + ',' + actual_timestamp.strftime("%d/%m/%y,%H:%M:%S") + ', [' +
                      format_duration(self.__previous_event_duration) + ']\n')
        logfile.close()
