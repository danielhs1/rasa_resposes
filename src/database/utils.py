def get_defaults(db_table):
    defaults = {}
    for column in db_table.columns:
        if column.default is not None:
            value = column.default.arg
            if callable(value):
                defaults[column.name] = value(column.name)
            else:
                defaults[column.name] = value
    return defaults
