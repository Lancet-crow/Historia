import datetime
import sqlalchemy

from data.db_session import SqlAlchemyBase


class Entries(SqlAlchemyBase):
    __tablename__ = 'entries'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    entries = sqlalchemy.Column(sqlalchemy.String())
    date_time = sqlalchemy.Column(sqlalchemy.DateTime,
                                  default=datetime.datetime.now,
                                  onupdate=datetime.datetime.now)
