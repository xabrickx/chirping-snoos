PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE tweeted (
`id` INT PRIMARY KEY,
redditid TEXT ,
reddit_author TEXT,
reddit_created NUMBER ,
tweet TEXT ,
tweet_submitted NUMBER
);
COMMIT;

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE banned (
   `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
   `redditname` TEXT,
   `last_change` NUMBER DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')) NOT NULL
 );
COMMIT;
COMMIT;
