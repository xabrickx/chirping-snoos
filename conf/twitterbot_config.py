import os
import logging

#[PATHS]
# Paths will be based on the location of this file which is ./conf by default.  Adjust accordingly!
FILEPATH = os.path.abspath(os.path.dirname(__file__))  
ENV_PATH = FILEPATH + "/env"

#[LOGGING]
LOG_PATH = FILEPATH + "/../logs/"
LOG_FILE = "twitterbot.log"
LOG_LEVEL = logging.DEBUG

#[PRAW]
USER_AGENT = "" #Your Unique USER AGENT for Reddit
SUBREDDIT = "" # The Subreddit you want to target
REDDIT_NEWPOST_LIMIT = 100 #How many new posts to check
REDDIT_SHORTPATH = "redd.it/" # For creating the shortlink to reddit

#[DB]
TWEETDATA_PATH = FILEPATH + "/../db/"
TWEETDATA_FILENAME = "chirping-snoos.db"
subtweet_kwargs = {"tweetdata_path" : TWEETDATA_PATH, "tweetdb_filename" : TWEETDATA_FILENAME}

#[TWITTER]
TWEET_UPVOTE_THRESHOLD = 10 #Minimum upvotes to be considered for tweeting
TWEET_COMMENT_THRESHOLD = 20 #minimum comments to be considered for tweeting
TWEET_ABSOLUTE_LIMIT = 270 #Max characters for a tweet
TWEET_PREFIX="" #This text will appear before the title from reddit
TWEET_SUFFIX="" #This text will appear after the title and link from reddit
TWEET_PART_SEPARATOR = " " #This is used to separate the prefix, title, link and suffix if desired
INTERTWEET_DELAY_SEC = 0.7 # Delay between tweets.  Recommended 0.5 or more to avoid flooding twitter
TWITTER_TIMESTAMP_FORMAT = "%a %b %d %H:%M:%S %z %Y" #Import Twitters timestamnp  into arrow
#If the title is too long, it will be shortened to fit.  
#Longtitle_Hint is shown at the end of the shortened text to symbolize shortening
TWEET_LONGTITLE_HINT = "..." 