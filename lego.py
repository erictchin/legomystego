"""
Given a tweet from a user, do a couple of things.

1.

"""

from nltk import word_tokenize

import hmac
import sqlite3
import dataset
import kenlm

RULES_DATABASE_URI = "sqlite:///ppdb/rules.db"
LEGO_HASH_KEY = "legomystego"


def tweet_hash(tweet, hash_key=LEGO_HASH_KEY):
    """
    Implement a keyed hash function according to section 3.3:

    1. Generate a keyed hash digest (HMAC-MD5) for each word
    2. Get the last four bits of the hash
    3. Bitwise rotate each value according to its position in the tweet
    4. XOR all the values together
    """
    tokens = word_tokenize(tweet)

    token_hashes = []
    tweet_hash = 0     # Start with 0, the XOR identity
    for n, token in enumerate(tokens):
        # Generate the keyed hash with the given key
        m = hmac.new(hash_key.encode(), msg=token.encode())

        m_hash = m.digest()

        # Get the last nibble of the hash
        m_bits = int(m_hash[-1]) & 0x0f


        # ROT-N for the position in the tweet
        for i in range(n):
            m_bits_shifted = m_bits << 1
            m_bits_overflow = m_bits_shifted & 0xf0
            m_bits_lower = m_bits_shifted & 0x0f

            m_bits = m_bits_lower + (m_bits_overflow >> 4)

        tweet_hash ^= m_bits
        token_hashes.append(m_bits)

    return hex(tweet_hash)

# Code to perform transformations for us

def get_synonyms(rules, token):
    """
    Get a list of synonyms for the given token and a given set of rules

    Args:

    token: a string of the token for which to find synonyms

    Return:

    a list of synonyms
    """
    return list(set([r['target'] for r in list(rules.find(source=token))]))

def get_synonyms_for_list(rules, tokens):
    """
    Generate synonyms for each token.

    Return as a dictionary
    """
    synonyms = {}

    for token in tokens:
        current_synonyms = get_synonyms(rules, token)

        if current_synonyms:
            synonyms[token] = current_synonyms

    return synonyms


def get_possible_stego_tweet_helper(rules, tweet):
    tokens = word_tokenize(tweet)
    synonyms = get_synonyms_for_list(rules, tokens)

    tweet_lm = kenlm.LanguageModel('data/tweets.klm')

    # A list of tuples (score, cover tweet)
    possibilities = []

    for token, alternatives in synonyms.items():
        for alt in alternatives:
            alt_tweet = tweet.replace(token, alt).replace(" &apos;", "'")
            alt_score = tweet_lm.score(alt_tweet)

            possibilities.append((alt_score, alt_tweet, tweet_hash(alt_tweet)))

    possibilities = sorted(possibilities, reverse=True)

    return possibilities

def get_possible_stego_tweets(tweet):
    rules_database = dataset.connect(RULES_DATABASE_URI)

    lexical_rules = rules_database["lexical"]
    o2m_rules = rules_database["o2m"]

    possibilities_o2m = get_possible_stego_tweet_helper(o2m_rules, tweet)
    possibilities_lexical = get_possible_stego_tweet_helper(lexical_rules, tweet)

    possibilities = set()
    possibilities.update(possibilities_o2m)
    possibilities.update(possibilities_lexical)
    possibilities = sorted(list(possibilities), key=lambda t:t[0], reverse=True)

    return possibilities

if __name__ == "__main__":
    cover_tweet = input("Enter the possible cover tweet: ")

    stego_tweets = get_possible_stego_tweets(cover_tweet)

    for tweet in stego_tweets[0:10]:
        print(tweet)
