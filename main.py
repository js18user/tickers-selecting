""" ticker analysis Python v.3.10.9 PostgresSQL v.14.5  Websocket Binance Poloniex Async/await Asyncpg by js18user """
import os
import yaml
import asyncio
import logging
import asyncpg

from m8_sql_query import sql_create_table_query, time_type
from m8binance import m8binance
from m8poloniex import m8poloniex


async def main(file: any, interspace: int, cloud_db: bool):
    class InitTask:
        def __init__(self, name, ):
            self.__name: str = name
            self.__url: str = ''
            self.__interspace: int = interspace
            self.__tickers: list = []
            self.__cloud_db: bool = cloud_db
            logging.basicConfig(level=logging.INFO, format=f"%({time_type})s : %(message)s", )
            match os.path.exists(self.__name):
                case True:
                    _m8_query = yaml.safe_load(open(self.__name, "r", ), )
                    match isinstance(_m8_query, dict, ):
                        case True:
                            match _m8_query:
                                case {"db": _, "db_vps": _, "tickers": _, }:
                                    self.__tickers = _m8_query['tickers']
                                    match self.__cloud_db:
                                        case True:
                                            self.__url = _m8_query['db_vps']
                                        case False:
                                            self.__url = _m8_query['db']
                                        case _:
                                            logging.info(f'No standard query for cloud_db')
                                            exit()
                                case {}:
                                    logging.info(f'No standard query')
                                    exit()
                        case _:
                            logging.info(f'No standard query')
                            exit()
                case False:
                    logging.info(f'No query')
                    exit()

        @property
        def name(self) -> str:
            return self.__name

        @property
        def tickers(self) -> list:
            return self.__tickers

        @property
        def url(self) -> str:
            return self.__url

        @property
        def interspace(self) -> int:
            return self.__interspace

        @property
        def cloud_db(self) -> bool:
            return self.__cloud_db

    try:
        task = InitTask(name=file, )

        con = await asyncpg.connect(task.url, )
        async with con.transaction():
            await con.fetch(sql_create_table_query, )
        await con.close()

        async with asyncpg.create_pool(task.url, min_size=2, max_size=6, ) as db:
            wss: list = [
                         m8binance(task.interspace, db, task.tickers, ),
                         m8poloniex(task.interspace, db, task.tickers, ),
            ]
            await asyncio.gather(*wss, )

    except KeyboardInterrupt:
        pass
    except (Exception, ValueError, TypeError, ) as error:
        logging.info(f'main() error: {error}')
    finally:
        await db.close()
        pass
try:
    asyncio.run(
        main(
            file="m8query.yaml",
            interspace=8,
            cloud_db=False,
        ),
    )
except KeyboardInterrupt:
    exit()
