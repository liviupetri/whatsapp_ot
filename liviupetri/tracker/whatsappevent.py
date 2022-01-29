from datetime import datetime, timedelta

from liviupetri.whatsapp.helpers.status import Status
from liviupetri.tracker.streamevent import StreamEvent


class WhatsAppEvent:
    def __init__(self):
        # self.__eventlist = [(Status.INITIAL_STATUS, datetime.now())]
        # self.__channels = [LogChannels.SCREEN, LogChannels.FILE]
        self.previous_status = Status.NOT_DEFINED
        self.previous_timestamp = datetime.now()
        self.actual_status = Status.INITIAL_STATUS
        self.actual_timestamp = datetime.now()

    def process_event(self, actual_status) -> bool:
        if actual_status in [None, Status.LAST_SEEN]:
            return False

        if actual_status == self.actual_status:
            return False

        # if actual_status == Status.USER_CHANGED:
        #     return False

        self.previous_status = self.actual_status
        self.previous_timestamp = self.actual_timestamp
        self.actual_status = actual_status
        self.actual_timestamp = datetime.now()
        # process WhatsApp delays
        if actual_status == Status.OFFLINE and self.actual_timestamp > (self.previous_timestamp + timedelta(seconds=12)):
            self.actual_timestamp -= timedelta(seconds=8)
        if actual_status == Status.ONLINE and self.actual_timestamp > (self.previous_timestamp + timedelta(seconds=2)):
            self.actual_timestamp -= timedelta(seconds=2)
        # save and stream event
        se = StreamEvent(self)
        se.stream_event()

        # self.previous_timestamp = datetime.now()
        # self.previous_status = actual_status

        return True

    # def __stream_event(self):
    #     if LogChannels.SCREEN in self.__channels:
    #         print_status_change(self.previous_status, self.previous_timestamp, self.actual_status,
    #                             self.actual_timestamp)
    #     if LogChannels.FILE in self.__channels:
    #         save_status_change_to_file(self.previous_status, self.previous_timestamp,
    #                                    self.actual_status, self.actual_timestamp)

    # def add_channel(self, channel):
    #     self.__channels.append(channel)
    #
    # def remove_channel(self, channel):
    #     self.__channels.remove(channel)

    # def set_logfile(self, logfile):
    #     self.__logfile = logfile

    # def set_web(self, web_address):
    #     pass
