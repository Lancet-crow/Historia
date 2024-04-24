import sqlalchemy

from data.db_session import SqlAlchemyBase


class Article(SqlAlchemyBase):
    __tablename__ = 'articles'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    slug = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer(), sqlalchemy.ForeignKey('users.id'), nullable=False)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean(), default=True, nullable=False)
