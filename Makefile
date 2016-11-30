
# Procude a language model as "data/tweets.klm" which we can use with python's kenlm module
tweetlm:
	# process all the tweets into one file
	# then build them into a language  TODO: need to pack this into a python scrip
	cat data/all_tweets.txt | python process.py | ./kenlm/bin/lmplz -o 3 > data/tweets.arpa
	./kenlm/bin/build_binary data/tweets.arpa data/tweets.klm

# Deal with the PPDB files. Run parser over the raw bzipped files.
parse_ppdb:
	python2 parser.py ppdb/ppdb-1.0-m-o2m ppdb/o2m.parse
	python2 parser.py ppdb/ppdb-1.0-m-lexical ppdb/lexical.parse

