# -*- encodig utf-8 -*-

import feedparser
import time
from subprocess import check_output
import sys
feed_name="Data Science"
urlrss='https://news.google.com/news/rss/search/section/q/data%20science/data%20science?hl=pt-BR&ned=pt-BR_br'
db = "/tmp/arquivo.txt"
limit = 12 * 3600 * 1000

#
# function to get the current time
#
current_time_millis = lambda: int(round(time.time() * 1000))
current_timestamp = current_time_millis()

def post_is_in_db(title):
    with open(db, 'r') as database:
        for line in database:
            if title in line:
                return True
    return False

# return true if the title is in the database with a timestamp > limit
def post_is_in_db(title):
    with open(db, 'r') as database:
        for line in database:
            if title in line:
                return True
    return False

def get():
    current_time_millis = lambda: int(round(time.time() * 1000))
    current_timestamp = current_time_millis()
    #
    # get the feed data from the url
    #
    feed = feedparser.parse(urlrss)

    #
    # figure out which posts to print
    #
    posts_to_print = []
    posts_to_skip = []

    for post in feed.entries:
        # if post is already in the database, skip it
        # TODO check the time
        title = post.title #+ '|' + post.links[0].href

        if post_is_in_db(title):
            posts_to_skip.append(title)
        else:
            posts_to_print.append(title)

    #
    # add all the posts we're going to print to the database with the current timestamp
    # (but only if they're not already in there)
    #
    f = open(db, 'a')
    for title in posts_to_print:
        if not post_is_in_db(title):
            f.write(title + "|" + str(current_timestamp) + "\n")
    f.close

    #
    # output all of the new posts
    #
    count = 1
    blockcount = 1
    for title in posts_to_print:
        if count % 5 == 1:
            print("\n" + time.strftime("%a, %b %d %I:%M %p") + '  ((( ' + feed_name + ' - ' + str(blockcount) + ' )))')
            print("-----------------------------------------\n")
            blockcount += 1
        print(title + "\n")
        count += 1

def getNoticia():
    #//get()
    feed = feedparser.parse(urlrss)
    for post in feed.entries:
        title = post.title
        if post_is_in_db(title):
            pass
        else:
            with open(db, 'a') as f:
                f.write(title + "|" + str(current_timestamp) + "\n")
            return  (title,post.links[0].href)


if __name__ == "__main__":
    print(getNoticia())
