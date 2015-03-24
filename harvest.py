from twython import Twython
import string, json, pprint
import urllib
from datetime import timedelta
from datetime import date
from time import *
import string, os, sys, subprocess, time
import pymysql

class TwitterAnalyzer:
    
    def __init__(self):
        # connect to our database and create a cursor to do some work
        conn = pymysql.connect(host='localhost',  user='root', passwd='YOUR DB PASSWORD HERE!!!', database='analytics')
        cur = conn.cursor()
        
        #connect to my twitter developer account
        APP_KEY = 'INSERT YOUR APP KEY HERE!!!'
        ACCESS_TOKEN = 'INSERT YOUR ACCESS TOKEN HERE!!!'
        twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
        
    def harvest(self, language):
        
        ''' define your harvest lists by language, use as many as you want, 
            they will all be separated in the database by keyword '''
        if language=='en':harvest_list = ['good', 'bad', 'ugly']
        if language=='de':harvest_list = []

        # grabbing the last "batch id", if it exists so we
        # can make log entries that make SOME sense
        self.cur.execute("select max(batchid) from TweetLog")
        batch_id_cur = self.cur.fetchall()
        if batch_id_cur[0][0] is None:
            batch_id = 0
        else:
            batch_id = batch_id_cur[0][0]+1

        #harvest until Twitter gets pissed off
        while True:
            for tweet_keyword in harvest_list:
                # whack the temp table in case we didn't exit cleanly
                self.cur.execute("""delete from TweetBankTemp where tweet_keyword = '"""+str(tweet_keyword)+"""'""")
                self.conn.commit()
                
                # run our search for the current keywords
                search_results = self.twitter.search(q=tweet_keyword, count = 1000, result_type="recent", lang=language)

                for tweet in search_results['statuses']:
                    # show me the tweet, jerry!
                    print "Tweet from @%s Date: %s" % (tweet['user']['screen_name'].encode('utf-8'),tweet['created_at'])
                    print "",tweet['text'].encode('utf-8'),"\n"

                    try:
                        # lets try to to put each tweet in our temp table for now
                        self.cur.execute("""insert into TweetBankTemp (tweet_id, tweet_datetime, tweet_keyword, tweet, tweeter, lang)
                            values ('"""+str(tweet['id_str'].encode('utf-8').replace("'","''").replace(';',''))+"""',
                                    cast(substring('"""+str(tweet['created_at'].encode('utf-8'))+"""',5,21) as datetime),
                                    '"""+str(tweet_keyword)+"""',
                                    '"""+str(tweet['text'].encode('utf-8').replace("'","''").replace(';',''))+"""',
                                    '"""+str(tweet['user']['screen_name'].encode('utf-8').replace("'","''").replace(';',''))+"""',
                                    '"""+str(tweet['metadata']['iso_language_code'].encode('utf-8').replace("'","''").replace(';',''))+"""'
                            ) """)
                    except:
                        # No soup for you!
                        print "############### Unexpected error:", sys.exc_info()[0], "##################################"

                # take all the tweets that we DIDNT already have
                # and put them in the REAL tweet table
                self.cur.execute("""insert into TweetBank (tweet_id, tweet_datetime, tweet_keyword, tweet, tweeter, lang)
                select * from TweetBankTemp where tweet_id NOT in
                (select distinct tweet_id from TweetBank)""")

                # take all THESE out of the temp table to not
                # interfere with the next keyword
                self.cur.execute("""delete from TweetBankTemp where tweet_keyword = '"""+str(tweet_keyword)+"""'""")

                # add a record to the log table saying what we did
                self.cur.execute(
                """insert into TweetLog (BatchId, Keyword, RunDate, HarvestedThisRun, TotalHarvested) values
                    (
                        '"""+str(batch_id)+"""',
                        '"""+" "+str(tweet_keyword)+"""',
                        CURRENT_DATE(),
                        (select count(*) from TweetBank where tweet_keyword = '"""+str(tweet_keyword)+"""'),
                        (select count(*) from TweetBank where tweet_keyword = '"""+str(tweet_keyword)+"""')
                    )
                """)

                # hot soup!
                self.conn.commit()

    def wordsToFile(self, sqlQuery, filename):
        self.cur.execute(sqlQuery)
        textFile = open(filename, "w")
        fullText = ''
        for a in cur.fetchall():
            for tweet in a:
                fullText+=tweet
                fullText+=' '
        textFile.write(fullText)
        textFile.close()
        
if __name__ == '__main__':
    tanalyzer = TwitterAnalyzer()
    tanalyzer.harvest('en')
    tanalyzer.wordsToFile("select tweet from TweetBank where lang='en'", 'alltweets.txt')

