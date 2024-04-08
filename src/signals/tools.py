from datetime import datetime

from signals.models import Signal


class SignalLastUpdatedParser:

    def __init__(self, covidcast_meta_data: list) -> None:
        self.covidcast_meta_data = covidcast_meta_data
        self.year_month_date_format = '%Y%m'
        self.year_month_day_date_format = '%Y%m%d'

    def format_date(self, date: str,) -> datetime:
        """
        Format the date string to a specific format.

        :param date: The date string to format.
        :return: The formatted date string.
        :rtype: str
        """
        formated_date: datetime
        if len(date) == 6:
            formated_date = datetime.strptime(date, self.year_month_date_format)
        elif len(date) == 8:
            formated_date = datetime.strptime(date, self.year_month_day_date_format)
        return formated_date

    def set_data(self) -> None:
        """
        Set the last updated date for signals in the database.
        """

        for db_source in self.covidcast_meta_data:
            for signal_data in db_source['signals']:
                try:
                    signal = Signal.objects.get(name=signal_data['signal_basename'], source__name=signal_data['source'])
                except Signal.DoesNotExist:
                    # TODO: Log this
                    continue
                signal.last_updated = self.format_date(str(signal_data['max_issue']))
                signal.from_date = self.format_date(str(signal_data['min_time']))
                signal.to_date = self.format_date(str(signal_data['max_time']))
                signal.save()
