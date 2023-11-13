""" ticker analysis Python v.3.10.9 PostgresSQL v.14.5  Websocket Binance Poloniex Async/await Asyncpg by js18user """
import os
import yaml
import asyncio
from loguru import logger as logging
import asyncpg

from m8_sql_query import sql_create_table_query
from m8binance import m8binance
from m8poloniex import m8poloniex


async def main():
    class InitTask:
        def __init__(self, ):
            self.__name: str = 'm8query.yaml'
            self.__url: str
            self.__interspace: int
            self.__tickers: list
            self.__cloud_db: bool
            match os.path.exists(self.__name):
                case True:
                    _m8_query = yaml.safe_load(open(self.__name, "r", ), )
                    match isinstance(_m8_query, dict, ):
                        case True:
                            match _m8_query:
                                case {"cloud": _, "db": _, "db_vps": _, "interspace": _, "tickers": _, }:
                                    self.__tickers = _m8_query['tickers']
                                    self.__interspace = _m8_query['interspace']
                                    self.__cloud_db = _m8_query['cloud']
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

        async def db_init(self):
            _connect = await asyncpg.connect(self.__url, )
            async with _connect.transaction():
                await _connect.fetch(sql_create_table_query, )
            await _connect.close()
            
        async def ws_start(self):
            async with asyncpg.create_pool(self.__url, min_size=2,  max_size=2, ) as _db:
                _wss = [
                        m8binance(self.__interspace, _db, self.__tickers, ),
                        m8poloniex(self.__interspace, _db, self.__tickers, ),
                ]

                await asyncio.gather(*_wss, )

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
        task = InitTask()
        await task.db_init()
        await task.ws_start()

    except KeyboardInterrupt:
        pass
    except (Exception, ValueError, TypeError, ) as error:
        logging.info(f'main() error: {error}')
    finally:
        pass
try:
    asyncio.run(main())
    
except KeyboardInterrupt:
    exit()
