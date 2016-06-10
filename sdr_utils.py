from bitarray import bitarray
import bitarray_io

wordlist = []

def setList(listname):
	bitarray_io.setDirectory(listname)
	_populateWordList(listname)

def _populateWordList(listname):
	"""Builds Python lists from file"""
	global wordlist
	wordlist = []
	with open('lists\{0}.list'.format(listname)) as f:
		for wordCR in f:
			word = wordCR[:-1]  # Remove carriage return
			wordlist.append(word)

def sdrFor(word):
	return bitarray_io.load(word)

def pairsBySimilarity():
	pairs = []
	for i in range(len(wordlist)):
		for j in range(i+1, len(wordlist)):
			w1 = wordlist[i]
			w2 = wordlist[j]
			s = similarity(w1, w2)
			if s > 0:
				pairs.append((w1, w2, s))
	sorted_by_similarity = sorted(pairs, key=lambda tup: tup[2])
	return list(reversed(sorted_by_similarity))

def similarTo(word, numResults=10):
	results = []
	if type(word) == str:
		ba1 = bitarray_io.load(word)
	elif type(word) == bitarray:
		ba1 = word
	else:
		print("Unknown input type '{0}'".format(type(word)))
		return
	for w in wordlist:
		ba2 = bitarray_io.load(w)
		s = similarity(ba1, ba2)
		if s > 0:
			results.append((w, s))
	sorted_by_similarity = sorted(results, key=lambda tup: tup[1])
	oneBits = sum(ba1)
	#return [(i[0], "{0:.0f}%".format(i[1]/oneBits * 100)) for i in list(reversed(sorted_by_similarity))[0:numResults]]
	#return [(i[0], i[1]) for i in list(reversed(sorted_by_similarity))[0:numResults]]
	return list(reversed(sorted_by_similarity))[0:numResults]


def similarity(ba1, ba2):
	if type(ba1) == bitarray and type(ba2) == bitarray:
		return sum(ba1 & ba2)
	elif type(ba1) == str and type(ba2) == str:
		return similarity(sdrFor(ba1), sdrFor(ba2))

