import os
import time
import simplejson
import sqlite3
import logging
import subprocess
import arrow
import re

import praw
import twitter
from twitter import *

# Import our libs last
from common.subtweets import Subtweet
from  conf.twitterbot_config import *

def init_logging():
    try:
        logging.basicConfig(filename=LOG_PATH + LOG_FILE,level=LOG_LEVEL,filemode='w')
        logging.basicConfig(format='%(asctime)s %(message)s \n', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.debug("Initialized Logging variables")
    except:
        exit("log init error")
def init_env():
    logging.debug("Initialize Env variables")

    if os.path.isfile(ENV_PATH):
        command = 'env -i bash -c "source '+ ENV_PATH + ' && env"'
        for line in subprocess.getoutput(command).split("\n"):
            key, value = line.split("=")
            os.environ[key]= value

def get_newest_reddit_posts(subreddit):
    logging.debug("Get newest reddit posts")

    ret = None
    if not subreddit is None:
        ret = subreddit.new(limit=REDDIT_NEWPOST_LIMIT)
    else:
        logging.critical("Subreddit is not defined!")
        exit()

    return ret

def get_reddit_path(pid):
    return REDDIT_SHORTPATH + pid

def get_tweet_text(tp):
    post_title = tp.title
    logging.debug("Building a tweet from reddit title:  " + str(post_title.encode("utf-8")))
    
    ret = ""
    tpslen = len(TWEET_PART_SEPARATOR)
    reddit_shortlink = get_reddit_path(tp.id)
    add_text_len= tpslen #We'll need at least one separator because of the title
    if(len(TWEET_PREFIX)>0):
        add_text_len = add_text_len + len(TWEET_PREFIX) + tpslen
        ret = ret + TWEET_PREFIX + TWEET_PART_SEPARATOR
    #Use a string placeholder to make sure our title fits within the configured tweet length
    ret = ret + "@@@POST_TITLE_PLACEHOLDER@@@" + TWEET_PART_SEPARATOR
    ret = ret + reddit_shortlink + TWEET_PART_SEPARATOR
    if(len(TWEET_SUFFIX)>0):
        add_text_len = add_text_len + len(TWEET_SUFFIX)
        ret = ret + TWEET_SUFFIX
    add_text_len = add_text_len + len(reddit_shortlink) + tpslen
    
    addlen = len(post_title) + add_text_len
    if (addlen) > TWEET_ABSOLUTE_LIMIT:
        logging.debug("Our title was too long (" + str(addlen) + ")")
        add_text_len = add_text_len + len(TWEET_LONGTITLE_HINT)
        trim_len = (addlen + + len(TWEET_LONGTITLE_HINT)) - TWEET_ABSOLUTE_LIMIT 
        post_title = post_title[:-trim_len] + TWEET_LONGTITLE_HINT
    
    p = re.compile('\@\@\@POST_TITLE_PLACEHOLDER\@\@\@')
    ret = p.sub(post_title, ret)
    

    return ret

def is_author_banned(author):

    ret = 0
    if author.lower() in map(str.lower, _BANNED_USERS):
        ret = 1
    return ret

def is_tweetable(submission):
    ret = 0
    if(
        (
            submission.score > TWEET_UPVOTE_THRESHOLD
            or submission.num_comments > TWEET_COMMENT_THRESHOLD
        ) and (
            submission.removed == False
            and submission.num_reports == 0
            and is_author_banned(str(submission.author)) == 0
        )
    ):
        ret = 1

    return ret



def __main():
    global _BANNED_USERS
    logging.debug("Twitterbot - __main Invoked")

    init_env()

    reddit = praw.Reddit(
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET'],
        password=os.environ['REDDIT_PASS'],
        user_agent=USER_AGENT,
        username=os.environ['REDDIT_USERNAME'])
    subreddit = reddit.subreddit(SUBREDDIT)
    subtweet_kwargs = {"tweetdata_path" : TWEETDATA_PATH, "tweetdb_filename" : TWEETDATA_FILENAME}
    subtweets = Subtweet(**subtweet_kwargs)
    logging.debug("Get banned users")
    _BANNED_USERS = subtweets.get_banned_users()


    latest_posts = get_newest_reddit_posts(subreddit)
    tweetable_posts = []

    for post in latest_posts:
        if is_tweetable(post)==1:
            logging.debug("[" + post.id + "] is tweetable")
            tweetable_posts.append(post)

    if len(tweetable_posts) > 0:
        sent_tweets = []
        logging.debug("Beginning tweet procedure")
        TWITTER_API = twitter.Api(consumer_key=os.environ['TWITTER_KEY'],
            consumer_secret=os.environ['TWITTER_SECRET'],
            access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
            access_token_secret=os.environ['TWITTER_TOKEN_SECRET'])
        
        filtered_posts = subtweets.filter_already_tweeted(tweetable_posts)
        logging.debug("After filtering tweetable posts are:  " + str(filtered_posts))
        for tp in filtered_posts:
            tweet_text = get_tweet_text(tp)
            logging.debug("Built tweet text>>  " + tweet_text.encode("utf-8").decode() + " - " + str(len(tweet_text)))
            post = TWITTER_API.PostUpdate(tweet_text)
            tweet_obj = (tp.id, str(tp.author), int(tp.created), tweet_text, arrow.Arrow.strptime(post.created_at, TWITTER_TIMESTAMP_FORMAT).timestamp)
            sent_tweets.append(tweet_obj)
            time.sleep(INTERTWEET_DELAY_SEC)
        subtweets.record_tweeted(sent_tweets)

    logging.debug("Twitterbot - Exiting successfully")







init_logging()
logging.debug("Initialize Twitterbot")
__main()
