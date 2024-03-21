from sqlalchemy import text


class SQLBase:
    @classmethod
    def create(cls, session, **data):
        instance = cls(**data)
        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def select(cls, session, condition=None, column_name=None, column_value=None):
        session.commit()
        if condition:
            results = session.execute(text(condition)).fetchall()
            return results
        elif column_name and column_value:
            column_attr = getattr(cls, column_name, None)
            return session.query(cls).filter(column_attr == column_value).first()
        else:
            results = session.query(cls).all()
            return results
