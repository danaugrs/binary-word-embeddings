import re

class WordData:
	def __init__(self, word=None, index=0):
		self.word = word
		self.index = index # Index of word in global wordlist
		self._END = False
		self.matcher = re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE)

	def endToken(self):
		self._END = True
		return self

	def isEndToken(self):
		return self._END

	def isPresentIn(self, text):
		return self.matcher.search(text)


class Response(object):
	def __init__(self, word=None, index=0):
		self.word = word
		self.index = index # Index of bit to set in word file
		self._END = False

	def endToken(self):
		self._END = True
		return self

	def isEndToken(self):
		return self._END