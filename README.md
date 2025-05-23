# tickers selecting
Analysis of cryptocurrency exchange tickers

The software stack for implementing the task is as follows:
- Python 3.10.9 
- Websockes
- Asyncio
- Async/await
- Yaml
- Asyncpg
- SQL
- Postgresql 14.5  DBaaS  or Localhost
- WebSocket Binance and Poloniex exchanges

Statement of the problem (Technical specifications for programming)

At a given time interval, generate an array of tickers from the specified cryptocurrency exchanges and save them in the database.
If there are several tickers of the same symbol, then the last ticker must be saved in the database, that is, the most relevant one at the end of the time interval.
The task must run continuously and is completed by "Ctrl C"
There can be several crypto currency exchanges and the processes must be parallel.

List and functions of the presented scripts:
- Dockerfile  no comment
- m8bilance.py  this program to perform a task with cryptocurrency exchange Bilance
- m8poloniex.py this program to perform a task with cryptocurrency exchange Poloniex
- main.py       the main program
- m8_sql_query.py this is a module containing SQL queries in the database
- requirements.txt no comments
- m8query.yaml  this is a file with request parameters
  - tickers - list of tickers
  - interspace - time in seconds for selecting tickers and storing them in the database
  - сloud - DB selection sign
    - False- for debugging localhost
    - True -  for work, the database is relevant, you can work

This publication shows how to work with two cryptocurrency exchanges:
- Binance
- Poloniex

In the working version, work with 11 cryptocurrency exchanges is implemented

- docker build -t tickers:bp -f Dockerfile .
- docker run tickers:bp

For a quick start from my personal public depository:
- docker pull js18user/exchange:bp
- docker run exchange:bp

