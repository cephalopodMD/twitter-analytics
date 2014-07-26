twitter-analytics
=================

A simple data harvesting library for twitter built in python

Required dependencies
=====================

1. A mysql server set up
2. PyMySql
3. twython

In ubuntu, install via the following

``` bash
  sudo apt-get install mysql-client
  sudo apt-get install mysql-server
  pip install PyMySQL
  pip install twython
```

twython requires a twitter developer account

your mysql db should have the following tables (I will try to add a setup module
Sto make this task easier)

TweetBank                |TweetBankTemp           |TweetLog
-------------------------|------------------------|--------
tweet_id bigint(20)      |tweet_id bigint(20)     |RunId int(11)
tweet_datetime datetime  |tweet_datetime datetime |BatchId int(11)
tweet_keyword varchar(50)|tweet_keywordvarchar(50)|RunDate datetime
tweet varchar(200)       |tweet varchar(200)      |Keywordles varchar(50)
tweeter varchar(100)     |tweeter varchar(100)    |HarvestedThisRun int(11)
lang varchar(50)         |lang varchar(50)        |TotalHarvested int(11)
geo varchar(50)          |geo varchar(50)         |

credit to Ryan Robitalle for the original code this was based on originally in
sql server and with an older twitter API at
http://ryrobes.com/python/harvesting-twitter-search-results-for-analysis-using-python-sql-server/
