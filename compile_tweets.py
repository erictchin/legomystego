"""
Compile and normalize tweets among all of the CSV files in the `data` directory.

Writes the normalized tweets into "data/all_tweets.txt"
"""
import csv
import re
import glob

def get_tweet_files():
    return list(glob.glob("data/*.csv"))

def normalize_tweets(raw_tweets):
    """
    Normalize the tweets according to a particular scheme:

    Replace @mentions with USER
    Replace a series of USER with a single USER
    Replace links with URL
    Replace a series of links with a single URL
    Make everything lowercase

    Return a normalized list of tweets
    """

    # Filter out retweets
    tweets_no_rts = list(filter(lambda x: not x[1].startswith('RT'), raw_tweets))

    # Make everything lowercase
    tweets_no_rts = [tweet[1].lower() for tweet in tweets_no_rts]

    # Canonicalize links to "URL" and @mentions to "USER"
    tweets_normalized = [re.sub(r'(https?:\/\/t\.co\/\w+)', 'URL', tweet) for tweet in tweets_no_rts]
    tweets_normalized = [re.sub(r'(@\w+)', 'USER', tweet) for tweet in tweets_normalized]

    # Replace multiple URLS and USERS with single user
    tweets_normalized = [re.sub("(USER\s*)+", "USER ", tweet) for tweet in tweets_normalized]
    tweets_normalized = [re.sub("(URL\s*)+", "URL ", tweet) for tweet in tweets_normalized]

    # Replace \n with a space
    tweets_normalized = [tweet.replace("\n", " ") for tweet in tweets_normalized]

    # Filter out tweets that are less than three words
    tweets_normalized = list(filter(lambda x: len(x.split()) > 3, tweets_normalized))

    return tweets_normalized

def go():
    tweet_corpus = get_tweet_files()
    # tweet_corpus = ['data/jack.csv', 'data/peterthiel.csv', 'data/realDonaldTrump.csv']

    # Build a language model from the tweets

    all_tweets = []
    for someone in tweet_corpus:
        csv_reader = csv.reader(open(someone, 'r'))

        columns = next(csv_reader)
        someones_tweets = list(csv_reader)

        someones_normalized_tweets = normalize_tweets(someones_tweets)

        all_tweets.extend(someones_normalized_tweets)

    # Write everyone's tweets into a single file, "all_tweets.txt"
    with open("data/all_tweets.txt", "w") as f:
        for tweet in all_tweets:
              f.write("{}\n".format(tweet))

if __name__ == "__main__":
    go()
