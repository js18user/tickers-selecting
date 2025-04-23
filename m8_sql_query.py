sql_insert_query = ("INSERT "
                    "INTO tickers "
                    "(exchange, timestamp, symbol, big, ask) "
                    "VALUES ($1,$2,$3,$4,$5);"
                    )
sql_create_table_query = ('CREATE TABLE IF NOT EXISTS tickers '
                          ' (id SERIAL PRIMARY KEY, '
                          '  exchange VARCHAR,   '
                          '  timestamp BIGINT,   '
                          '  symbol    VARCHAR,   ' 
                          '  big       NUMERIC,   '
                          '  ask       NUMERIC  );'
                          )
