""" Python v.3.10.9  PostgresSQL v.14.5 websocket Binance asyncio/await asyncpg   by js18user """
import asyncpg
import orjson as json
import websockets
import time
import logging
from m8_sql_query import sql_insert_query, time_type

""" Additional Information 
 https://binance-docs.github.io/apidocs/futures/en/#all-market-tickers-streams 
 url = 'wss://stream.binance.com/ws/' 
"""
ticker_structure: dict = {
    "e": "24hrTicker",  # Event type
    "E": 123456789,  # + 1 Event time
    "s": "symbol",  # + 2
    "p": "0.0015",  # Price change
    "P": "250.00",  # Percentage price change
    "w": "0.0018",  # Average weighted price
    "x": "0.0009",  # Closing price of the previous day
    "c": "0.0025",  # Closing price of the current day
    "Q": "10",      # Closing volume
    "b": "0.0024",  # + 9 Best Bid (bid/buy) price
    "B": "10",      # Best Bid Volume
    "a": "0.0026",  # + 11 Best ask price (offer/sale)
    "A": "100",     # Volume of the best ask
    "o": "0.0010",  # Opening price
    "h": "0.0025",  # High
    "l": "0.0010",  # Low
    "v": "10000",   # Total trading volume in base currency
    "q": "18",      # Total trading volume in quote currency
    "O": 0,         # Statistics collection start time
    "C": 86400000,  # Statistics collection end time
    "F": 0,         # First trade ID
    "L": 18150,     # Last trade ID
    "n": 18151      # Total number of transactions
}
""" Ended information for operate """


async def m8binance(interspace: int, db: asyncpg.Pool, file: list, ):
    """  It is a main procedure for operate with binance exchange """
    try:
        logging.basicConfig(level=logging.INFO, format=f"%({time_type})s : %(message)s", )
        exchange: str = 'binance'
        timestamp: str = "C"
        symbol: str = 's'
        big: str = 'b'
        ask: str = 'a'
        ticker_number: int = 0
        skip: str = '\n'
        tickers: dict = {}
        url: str = f"wss://stream.binance.com/ws/{'@ticker/'.join(file).replace('_', '')}@ticker"
        logging.info(f'Start of process Binance exchange, interspace: { {interspace} }{skip}', )  # You can '#'

        async with websockets.connect(url, ) as wbs:
            start_time: float = time.time()
            while 1:

                ticker: dict = json.loads(await wbs.recv(), )
                ticker_number += 1
                # logging.info(ticker, )                                                        # You can '#'
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
                                     f'Binance{skip}'                                            # You can '#'
                                     f'{tickers}{skip}'  # You can '#'                         # You can '#'
                                     f' interspace is ---> ({interspace}){skip}'               # You can '#'
                                     f"number of tickers received---> {ticker_number}{ skip}"  # You can '#'
                                     f'number of tickers inserted---> {len(tickers)}{skip}'      # You can '#'
                                     )
                        ticker_number,  start_time = 0,  time.time()
                        tickers.clear()
    except KeyboardInterrupt:
        pass
    except (Exception, TypeError, ValueError, ) as error:
        logging.info(f'm8binance error : {error}', )
    finally:
        logging.info(f'Completion of process Binance, interspace: { {interspace} }', )  # You can '#'
        return ()
