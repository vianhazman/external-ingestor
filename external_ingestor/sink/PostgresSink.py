import csv
from io import StringIO
from sqlalchemy import create_engine

from external_ingestor.utils.logging import get_logger


class PostgresSink:
    def __init__(self, settings):
        self.name = self.__class__.__name__
        self.logger = get_logger(self.name)
        self.url = 'postgresql+psycopg2://{user}:{pass}@{host}:{port}/{db}'.format(**settings)
        self.table_name = settings['table_name']

    def psql_insert_copy(self, table, conn, keys, data_iter):
        # gets a DBAPI connection that can provide a cursor
        dbapi_conn = conn.connection
        with dbapi_conn.cursor() as cur:
            s_buf = StringIO()
            writer = csv.writer(s_buf)
            writer.writerows(data_iter)
            s_buf.seek(0)

            columns = ', '.join('"{}"'.format(k) for k in keys)
            if table.schema:
                table_name = '{}.{}'.format(table.schema, table.name)
            else:
                table_name = table.name

            sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
                table_name, columns)
            cur.copy_expert(sql=sql, file=s_buf)

    def sink(self, df):
        self.logger.info("Begin sinking to PostgreSQL")
        try:
            engine = create_engine(self.url)
            df.to_sql(self.table_name, engine, method=self.psql_insert_copy, if_exists="append")
        except Exception as e:
            self.logger.error(str(e))
        self.logger.info("Sinked to PostgreSQL")







