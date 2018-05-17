import os
import sys
import simplejson
import sqlite3


# Do not allow execution from CLI
def main():
    print("This Subtweet class may not be run directly from the CLI.")
    sys.exit(1)
if __name__ == "__main__":
    main()


class Subtweet:
    config = {"path2tweetdata" : "", "filename2tweetdata" : ""}
    tweetdb_path = None



    def __init__(self, **kwargs):
        self.config["path2tweetdata"] = kwargs.pop('tweetdata_path')
        self.config["filename2tweetdata"] = kwargs.pop('tweetdb_filename')

        self.tweetdb_path = self.config["path2tweetdata"] + self.config["filename2tweetdata"]
    def ping(self):
        print('pong - tweets!')


    def get_all_tweeted(self):
        conn = sqlite3.connect(self.tweetdb_path)
        with conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * from tweeted")

            return [dict(zip([column[0] for column in c.description], row))
             for row in c.fetchall()]

    def get_banned_users(self):
        ret = []
        try:
            conn = sqlite3.connect(self.tweetdb_path)
            with conn:
                conn.row_factory = lambda cursor, row: row[0]
                c = conn.cursor()

                c.execute("SELECT redditname from banned")
            ret = c.fetchall()
        except:
            ret = []

        return ret

    def record_tweeted(self, newtweets):
        if len(newtweets) >0:
            conn = sqlite3.connect(self.tweetdb_path)
            with conn:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.executemany("INSERT INTO tweeted(redditid, reddit_author, reddit_created, tweet, tweet_submitted) VALUES (?,?,?,?,?)", newtweets);                    
                conn.commit()
            conn.close()

    def filter_already_tweeted(self, postlist):
        filtered_posts = postlist
        if len(postlist)>0:
            id_list=[]
            for post in postlist:
                id_list.append(post.id)
            conn = sqlite3.connect(self.tweetdb_path)
            conn.row_factory = lambda cursor, row: row[0]
            with conn:
                c = conn.cursor()
                # create an entry for this
                any_dupes = c.execute('SELECT redditid FROM tweeted WHERE redditid IN (%s)' %
                    ','.join('?'*len(id_list)), id_list).fetchall()
                if len(any_dupes)>0:
                    any_dupes = set(any_dupes) #improve performance by making this an actual set
                    filtered_posts = [p for p in filtered_posts if p.id not in any_dupes]
            conn.close()
            
        return filtered_posts