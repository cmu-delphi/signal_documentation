import logging
import os
from datetime import datetime

import requests
import sqlalchemy
from sqlalchemy import create_engine, update
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SQLALCHEMY_DATABASE_URI",
    "mysql+mysqlconnector://root:ROOT_PASSWORD@localhost:3306/mysql_database",
)
engine: Engine = create_engine(
    SQLALCHEMY_DATABASE_URI, execution_options={"engine_id": "default"}
)
Session = sessionmaker(bind=engine)


COVID_CAST_META_URL = os.environ.get(
    "COVID_CAST_META_URL", "https://api.delphi.cmu.edu/epidata/covidcast/meta"
)


class Base(DeclarativeBase):
    pass


class Signal(Base):

    __tablename__ = "signals_signal"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    display_name = sqlalchemy.Column(sqlalchemy.String)
    active = sqlalchemy.Column(sqlalchemy.Boolean)
    short_description = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    format_type = sqlalchemy.Column(sqlalchemy.String)
    time_type = sqlalchemy.Column(sqlalchemy.String)
    time_label = sqlalchemy.Column(sqlalchemy.String)
    is_smoothed = sqlalchemy.Column(sqlalchemy.Boolean)
    is_weighted = sqlalchemy.Column(sqlalchemy.Boolean)
    is_cumulative = sqlalchemy.Column(sqlalchemy.Boolean)
    has_stderr = sqlalchemy.Column(sqlalchemy.Boolean)
    has_sample_size = sqlalchemy.Column(sqlalchemy.Boolean)
    high_values_are = sqlalchemy.Column(sqlalchemy.String)
    base_id = sqlalchemy.Column(sqlalchemy.Integer)
    category_id = sqlalchemy.Column(sqlalchemy.Integer)
    source_id = sqlalchemy.Column(sqlalchemy.Integer)
    created = sqlalchemy.Column(sqlalchemy.DateTime)
    modified = sqlalchemy.Column(sqlalchemy.DateTime)
    last_updated = sqlalchemy.Column(sqlalchemy.Date)
    age_breakdown = sqlalchemy.Column(sqlalchemy.String)
    data_censoring = sqlalchemy.Column(sqlalchemy.Text)
    gender_breakdown = sqlalchemy.Column(sqlalchemy.Integer)
    missingness = sqlalchemy.Column(sqlalchemy.Text)
    race_breakdown = sqlalchemy.Column(sqlalchemy.Integer)
    reporting_cadence = sqlalchemy.Column(sqlalchemy.String)
    restrictions = sqlalchemy.Column(sqlalchemy.Text)
    severity_pyramid_rungs = sqlalchemy.Column(sqlalchemy.String)
    temporal_scope_end = sqlalchemy.Column(sqlalchemy.String)
    temporal_scope_end_note = sqlalchemy.Column(sqlalchemy.Text)
    temporal_scope_start = sqlalchemy.Column(sqlalchemy.String)
    temporal_scope_start_note = sqlalchemy.Column(sqlalchemy.Text)
    typical_reporting_lag = sqlalchemy.Column(sqlalchemy.String)
    typical_revision_cadence = sqlalchemy.Column(sqlalchemy.String)
    license_id = sqlalchemy.Column(sqlalchemy.Integer)
    signal_type_id = sqlalchemy.Column(sqlalchemy.Integer)
    from_date = sqlalchemy.Column(sqlalchemy.Date)
    to_date = sqlalchemy.Column(sqlalchemy.Date)
    geographic_scope_id = sqlalchemy.Column(sqlalchemy.Integer)
    signal_availability_days = sqlalchemy.Column(sqlalchemy.Integer)


class Source(Base):
    __tablename__ = "datasources_sourcesubdivision"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    display_name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    db_source = sqlalchemy.Column(sqlalchemy.String)
    data_source_id = sqlalchemy.Column(sqlalchemy.Integer)
    created = sqlalchemy.Column(sqlalchemy.DateTime)
    modified = sqlalchemy.Column(sqlalchemy.DateTime)
    external_name = sqlalchemy.Column(sqlalchemy.String)


class SignalLastUpdatedParser:

    def __init__(self, covidcast_meta_data: list) -> None:
        self.covidcast_meta_data = covidcast_meta_data
        self.year_week_date_format = "%Y-%W-%w"
        self.year_month_day_date_format = "%Y%m%d"

    def format_date(
        self,
        date: str,
    ) -> datetime:
        """
        Format the date string to a specific format.

        :param date: The date string to format.
        :return: The formatted date string.
        :rtype: str
        """
        formated_date: datetime
        if len(date) == 6:
            year, week = date[:4], date[4:]
            logger.info(f"Date: {date}, year: {year}, week: {int(week)-1}")
            formated_date = datetime.strptime(
                f"{int(year)}-{int(week)-1}-1", self.year_week_date_format
            )
        elif len(date) == 8:
            formated_date = datetime.strptime(date, self.year_month_day_date_format)
        return formated_date

    def set_data(self) -> None:
        """
        Set the last updated date for signals in the database.
        """
        with Session() as session:
            for db_source in self.covidcast_meta_data:
                for signal_data in db_source["signals"]:
                    source = (
                        session.query(Source)
                        .filter(Source.name == signal_data["source"])
                        .first()
                    )
                    last_updated = self.format_date(str(signal_data["max_issue"]))
                    from_date = self.format_date(str(signal_data["min_time"]))
                    to_date = self.format_date(str(signal_data["max_time"]))
                    signal_availability_days = abs((to_date - from_date).days)
                    try:
                        session.execute(
                            update(Signal)
                            .where(Signal.name == signal_data["signal"])
                            .where(Signal.source_id == source.id)
                            .values(
                                last_updated=last_updated,
                                from_date=from_date,
                                to_date=to_date,
                                signal_availability_days=signal_availability_days,
                            )
                        )
                        session.commit()
                        logger.info(
                            f"Signal {signal_data['signal']} successfully updated."
                        )
                    except AttributeError:
                        logger.error(
                            f"""Failed to update signal {signal_data['signal']}.
                            Probably the issue is with the source or source with name
                            {signal_data['source']} does not exist."""
                        )


def main():
    response = requests.get(COVID_CAST_META_URL)
    if response.status_code == 200:
        covidcast_meta_data = response.json()
        parser = SignalLastUpdatedParser(covidcast_meta_data)
        parser.set_data()
    else:
        logger.error(f"Failed to get data from {COVID_CAST_META_URL}")


if __name__ == "__main__":
    main()
