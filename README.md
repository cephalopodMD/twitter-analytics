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

your mysql db should have the following tables

TweetBank|TweetBankTemp|TweetLog
---------|-------------|--------
tweet_id|tweet_id|RunId
tweet_datetime|tweet_datetime|BatchId
tweet_keyword|tweet_keyword|RunDate
tweet|tweet|Keyword
tweeter|tweeter|HarvestedThisRun
lang|lang|TotalHarvested
geo|geo|

credit to Ryan Robitalle for the original code this was based on originally in
sql server and with an older twitter API at
http://ryrobes.com/python/harvesting-twitter-search-results-for-analysis-using-python-sql-server/
