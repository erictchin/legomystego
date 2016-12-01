# Leggo My Stego

A Linguistic Stegonographic System.  Inspired by smart people.  Hacked by @etchin and @zankuda.

## General Steps

### Dependencies

* KenLM
    - Installed according to [this tutorial](http://victor.chahuneau.fr/notes/2012/07/03/kenlm.html) to directory `kenlm`

### Preparation

#### Gather Tweets and Generate the Tweet Language Model

`make tweets`

The idea of this is to generate a language model of how people write tweets.  With a sufficiently large number of Tweets (filtered of useless ones) we can deal generate this model using the KenLM package.

0. Use the Twitter API (via the [Technica Demo](http://zetaware.net/technica-twitter/) to download tweets of a bunch of tweeters. Dump these CSV files into data/
1. Process all of these tweet CSV files into a single flat text file
    - `python compile_tweets.py`
2. Process all of the Tweets into a `.arpa` language model file
    - `cat data/all_tweets.txt | python data/process.py | ./kenlm/bin/lmplz -o 3 > data/tweets.arpa`
3. Convert the textual language model into a binary blob
    - `./kenlm/bin/build_binary data/tweets.arpa data/tweets.klm`

#### Generate the Paraphrase Databse

`make parse_ppdb` and `make build_rules`

Download some PPDB databases from [Download a PPDB file from the right website](https://www.cis.upenn.edu/~ccb/ppdb/).

0. Generate the PPDB database from PPDB web files
    - `python2 ppdb/parser.py ppdb/ppdb-1.0-m-o2m ppdb/o2m.parse`
    - `python2 ppdb/parser.py ppdb/ppdb-1.0-m-lexical ppdb/lexical.parse`
1. Convert the PPDB database rules to `ppdb/rules.db`
    - `python build_ppdb.py`

#### Canonicalization of tweets

1. Parse and canonicalize tweets of a person.
    - this is necessary to build the proper language model
    - language model is used to score each possible cover tweet
    - best scoring covers are presented to user as possible tweets
    - each cover tweet is associated with a hash, which is used to communicate a message
2. Tweet -> Cover
    - for a given tweet a user is about to write, generate possible cover tweets

