# Chirping Snoos

This is a python service which will monitor the subreddit of your choosing and tweet the top posts.  Thresholds for upvote and comments are configurable to allow you define what a top post is.  It uses sqlite3 to track processed posts and maintain a ban list  

## Getting Started

1. Clone the repo
2. Configure the application accordingly via ./twitterbot/twitterbot_config.py
3. Set up a scheduled task to run the service at your desired interval

### Prerequisites

* python3
* sqlite3
* Task scheduler of your choice
* A reddit account with API credentials

    Read more at https://www.reddit.com/wiki/api

* A twitter account with API credentials for your bot

    Read more at https://apps.twitter.com/



### Installing

1. Install all python dependencies:
  1. praw
  2. python-twitter
  3. simplejson
  4. arrow
     (ex - pip3 install praw python-twitter simplejson arrow)
2. Clone the git repository
3. Set up sql with the included script  

    ex: sqlite3 -init ./sql/chirping-snoos.sql /path/to/your/database.db  

4. Configure the environment variables via ./common/env (see env.example for a template)
5. Configure the application via ./twitterbot/twitterbot_config.py  

    Don't forget the sqlite file you created above  


## Deployment

1. Set up a scheduled task to run the service at your desired interval

   cron ex: */5 * * * * /path/to/your/python3 /path/to/your/chirping-snoos.py )

## Built With

* [praw](https://praw.readthedocs.io/en/latest/) - Reddit API wrapper for python
* [python-twitter](https://github.com/bear/python-twitter) - Twitter API wrapper for python
* [arrow](http://arrow.readthedocs.io/en/latest/) - Date/Time management for python
* [simplejson](https://simplejson.readthedocs.io/en/latest/) - Improved JSON support for python

## Authors

* **Albert Brick** -  [xabrickx](https://github.com/xabrickx)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

#Comments

Praw is arguably  overkill to  obtain a json payload from /new, but most people who manage Reddits API with python seem to use it