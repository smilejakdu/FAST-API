import sqlalchemy


def to_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in sqlalchemy.inspect(obj).mapper.column_attrs}


def response_updated_as_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
