def make_sql_url(
    sql_prefix: str,
    db_name: str,
    db_user: str,
    db_pass: str,
    db_port: int,
    db_host: str = "localhost",
) -> str:
    return f"{sql_prefix}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


def make_pg_url(
    db_name: str, db_user: str, db_pass: str, db_port: int, db_host: str = "localhost"
) -> str:
    return make_sql_url("postgresql+psycopg", db_name, db_user, db_pass, db_port, db_host=db_host)
