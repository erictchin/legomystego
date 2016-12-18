
# coding: utf-8

# In[1]:

# Read in some tweets
import csv
jack_reader = csv.reader(open('data/realdonaldtrump.csv', 'r'))

columns = next(jack_reader)


# In[2]:

jack_tweets = list(jack_reader)


# In[3]:

# Filter out retweets
jack_tweets_no_rts = list(filter(lambda x: not x[1].startswith('RT'), jack_tweets))

for i in range(10):
    print(jack_tweets_no_rts[i][1])


# In[4]:

# Canonicalize the tweet text as lowercase
import re
jack_tweets_no_rts_lowercase = [tweet[1].lower() for tweet in jack_tweets_no_rts]

# Canonicalize links to "URL" and @mentions to "USER"
jack_tweets_no_rts_lowercase = [re.sub(r'(https?:\/\/t\.co\/\w+)', 'URL', tweet) for tweet in jack_tweets_no_rts_lowercase]
jack_tweets_normalized = [re.sub(r'(@\w+)', 'USER', tweet) for tweet in jack_tweets_no_rts_lowercase]

for i in range(10):
    print(jack_tweets_no_rts_lowercase[i])
    print("  -> {}".format(jack_tweets_normalized[i]))


# In[5]:

import nltk
from nltk import word_tokenize
# note: need to nltk.download() all the models the first time aroudn

# Frequency distribution of words.
main_dist = nltk.FreqDist([])
for tweet in jack_tweets_normalized:
    tokens = word_tokenize(tweet)
    
    # We don't want to count the mentions and hashtags
    # tokens = list(filter(lambda x: not (x[0] == '@' or x[0] == '#'), tokens))
    
    main_dist.update(tokens)


# In[6]:

main_dist.most_common()[0:40]


# In[7]:

import hmac
import binascii
import struct
from nltk import word_tokenize

hash_key = "legomystego"

def tweet_hash(tweet):
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
    


# In[8]:

tweet_hash("ferociosu world")


# In[9]:

tweet_hash("world hello")


# In[10]:

tweet_hash("magical wonderful magic")


# In[119]:

# Substitutions
import sqlite3
import dataset
RULES_DATABASE_URI = "sqlite:///ppdb/rules.db"

rules_database = dataset.connect(RULES_DATABASE_URI)
lexical_rules = rules_database["lexical"]


# In[120]:

print(list(lexical_rules.find(source="attraction")))
rules = list(lexical_rules.all())


# In[121]:

def get_synonyms(rules, token):
    """
    Get a list of synonyms for the given token
    
    Args:
    
    token: a string of the token for which to find synonyms
    
    Return:
    
    a list of synonyms
    """
    return list(set([r['target'] for r in list(rules.find(source=token))]))

# Test
get_synonyms(lexical_rules, "attraction")


# In[122]:


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


# In[123]:

print(get_synonyms_for_list(lexical_rules, "I'm fairly attractive".split()))
print(get_synonyms_for_list(lexical_rules, "What movie are you seeing this evening".split()))


# In[136]:

import kenlm
model = kenlm.LanguageModel('data/tweets.klm')


def get_possible_cover_tweet(rules, tweet):
    tokens = word_tokenize(tweet)
    synonyms = get_synonyms_for_list(rules, tokens)

    # A list of tuples (score, cover tweet)
    possibilities = []

    for token, alternatives in synonyms.items():
        for alt in alternatives:
            alt_tweet = tweet.replace(token, alt)
            alt_score = model.score(alt_tweet)
            
            possibilities.append((alt_score, alt_tweet, tweet_hash(alt_tweet)))
                        
    possibilities = sorted(possibilities, reverse=True)
    
    for possibility in possibilities:
        print(possibility)
        
    return possibilities


# In[137]:

possibilities = get_possible_cover_tweet(lexical_rules, "what movie do you want to see this evening")


# In[138]:

possibilities = get_possible_cover_tweet(lexical_rules, "i am going to see grandma")


# In[139]:

o2m_rules = rules_database["o2m"]


# In[140]:

possibilities_o2m = get_possible_cover_tweet(o2m_rules, "i am going to see grandma")
possibilities_lexical = get_possible_cover_tweet(o2m_rules, "i am going to see grandma")

possibilities = []
possibilities.extend(possibilities_o2m)
possibilities.extend(possibilities_lexical)
possibilities = list(set(possibilities))


# In[135]:

possibilities = sorted(possibilities, reverse=True)


# In[ ]:

# TODO: these are possibities within the  the language model

