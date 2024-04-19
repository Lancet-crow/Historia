import datetime
import sqlalchemy

from data.db_session import SqlAlchemyBase


class Uploads(SqlAlchemyBase):
    __tablename__ = 'uploads'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    file = sqlalchemy.Column(sqlalchemy.String(length=255))
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime,
                                  default=datetime.datetime.now,
                                  onupdate=datetime.datetime.now)
