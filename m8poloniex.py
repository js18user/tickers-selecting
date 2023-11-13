""" Python v.3.10.9 PostgresSQL v.14.5  Websocket Poloniex Async/await Asyncpg by s18user """
import asyncpg
import orjson as json
import time
import websockets

from loguru import logger as logging
from m8_sql_query import sql_insert_query

""" Additional Information
https://docs.poloniex.com/#websocket-api     
https://docs.poloniex.com/#ticker-data 
"""
ticker_structure: dict = {
      'symbol': 'BTS_BTC',
      'startTime': 1698240660000,
      'open': '0.0000003058',
      'high': '0.0000003058',
      'low': '0.0000002963',
      'close': '0.0000002963',
      'quantity': '14835',
      'amount': '0.0044522288',
      'tradeCount': 5,
      'dailyChange': '-0.0311',
      'markPrice': '0.000000296',
      'closeTime': 1698327098025,
      'ts': 1698342761370
}


async def m8poloniex(interspace: int, db: asyncpg.Pool, file: list):
    """  It is a main procedure for operate with Poloniex exchange """

    try:
        exchange: str = 'poloniex'
        timestamp: str = 'ts'
        symbol: str = 'symbol'
        big: str = 'high'
        ask: str = 'low'
        skip: str = '\n'
        data: dict = {"event": "subscribe", "channel": ["ticker"], "symbols": file, }
        tickers: dict = {}
        logging.info(f'Start of process Poloniex exchange, interspace: { {interspace} }{skip}', )  # You can '#'
        # logging.info(file)                                                                       # You can '#'
        ping_time: float = time.time()
        while 1:
            async with websockets.connect(f"wss://ws.poloniex.com/ws/public", ) as wbs:

                await wbs.send(data.__str__())
                await wbs.recv()
                start_time = time.time()
                tickers.clear()
                ticker_number: int = 0
                while (30 - (time.time() - ping_time)) >= interspace:

                    ticker: dict = json.loads(await wbs.recv())['data'][0]
                    # logging.info(f'{ticker}, {skip}')                                         # You can '#'
                    ticker_number += 1
                    tickers[ticker[symbol]]: dict = (
                                                     exchange,
                                                     ticker[timestamp],
                                                     ticker[symbol],
                                                     float(ticker[big]),
                                                     float(ticker[ask]),
                                                     )
                    match (time.time() - start_time) >= interspace:
                        case False:
                            pass
                        case True:
                            async with db.acquire() as con:
                                async with con.transaction():
                                    await con.executemany(sql_insert_query, [*tickers.values()], )
                            logging.info(f''
                                         f'Poloniex{skip}'                                           # You can '#'                                          
                                         # f'{tickers}{skip}'                                        # You can '#'                        
                                         # f' interspace is ---> ({interspace}){skip}'                 # You can '#'
                                         f' number of tickers received  ---> {ticker_number}{skip}'  # You can '#'
                                         f'number of tickers inserted---> {len(tickers)}{skip}'      # You can '#'
                                         )
                            ticker_number, start_time, tickers = 0, time.time(), {}
            ping_time = time.time()
    except KeyboardInterrupt:
        pass
    except (Exception, TypeError, ValueError, ) as error:
        logging.info(f'm8poloniex error: {error}', )
        pass
    finally:
        logging.info(f'Completion of process Poloniex, interspace: { {interspace} }', )               # You can '#'
        pass
        return ()
