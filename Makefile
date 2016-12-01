
# Procude a language model as "data/tweets.klm" which we can use with python's kenlm module
tweets:
	# process all the tweets into one file (via compile_tweets.py to all_tweets.txt)
	# process all_tweets.txt into a textual language model
	# process textual language model into a binary blob
	python compile_tweets.py
	cat data/all_tweets.txt | python data/process.py | ./kenlm/bin/lmplz -o 3 > data/tweets.arpa
	./kenlm/bin/build_binary data/tweets.arpa data/tweets.klm

# Deal with the PPDB files. Run parser over the raw bzipped files.
parse_ppdb:
	python2 ppdb/parser.py ppdb/ppdb-1.0-m-o2m ppdb/o2m.parse
	python2 ppdb/parser.py ppdb/ppdb-1.0-m-lexical ppdb/lexical.parse

build_rules:
	# process all of the ppdb/*.parse and put them into a sqlite3 database
	# ppdb/rules.db
	# parse_ppdb should come first
	python build_ppdb.py

