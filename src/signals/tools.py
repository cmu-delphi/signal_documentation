from datetime import datetime

from signals.models import Signal


class SignalLastUpdatedParser:

    def __init__(self, covidcast_meta_data: list) -> None:
        self.covidcast_meta_data = covidcast_meta_data
        self.incoming_date_format = '%Y%m%d'

    def set_data(self) -> None:
        """
        Set the last updated date for signals in the database.
        """

        for db_source in self.covidcast_meta_data:
            for signal_data in db_source['signals']:
                try:
                    signal = Signal.objects.get(name=signal_data['signal_basename'])
                except Signal.DoesNotExist:
                    # TODO: Log this
                    continue
                if signal:
                    signal.last_updated = datetime.strptime(str(signal_data['max_issue']), self.incoming_date_format)
                    signal.from_date = datetime.strptime(str(signal_data['min_time']), self.incoming_date_format)
                    signal.to_date = datetime.strptime(str(signal_data['max_time']), self.incoming_date_format)
                    signal.save()
