# Python Modules
import logging
from logging.handlers import RotatingFileHandler
import sys

# Third Party
import wikipedia

# My modules
from thread_messaging import Response

logDir = 'logs'

# Worker receives a word, finds related articles, and then searches each article for all words in wordlist
class Worker:
	def __init__(self, wcfg):
		self.cfg = wcfg

		# Set up logger
		logName = 'worker-{0}'.format(self.cfg['idx'])
		logFormat = logging.Formatter("%(asctime)s %(levelname)s: %(threadName)s - %(message)s")

		self.log = logging.getLogger(logName)
		self.log.setLevel(logging.DEBUG)

		ch = logging.StreamHandler(sys.stdout)
		ch.setFormatter(logFormat)
		self.log.addHandler(ch)

		fh = logging.handlers.RotatingFileHandler("{0}\{1}.txt".format(logDir, logName), maxBytes=(1048576*5), backupCount=7)
		fh.setFormatter(logFormat)
		self.log.addHandler(fh)

	def parseArticle(self, articleName, articleIndex):
		# NOTE: The article index is the same as the index of the bit in the word files
		#self.log.debug("    {0}: Parsing article '{1}'".format(articleIndex, articleName))
		articleName.encode('ascii', 'ignore')
		try:
			# Request article summary from Wikipedia
			text = wikipedia.summary(articleName)

		# Catch exceptions from wikipedia module
		except wikipedia.exceptions.DisambiguationError:
			self.log.debug("{0}: DisambiguationError parsing '{1}'".format(articleIndex, articleName)) # Expected to happen often
			return 0
		except wikipedia.exceptions.PageError:
			self.log.error("{0}: PageError parsing '{1}'".format(articleIndex, articleName))
			return 0
		except wikipedia.exceptions.HTTPTimeoutError:
			self.log.error("{0}: HTTPTimeoutError parsing '{1}'".format(articleIndex, articleName))
			return 0
		except wikipedia.exceptions.RedirectError:
			self.log.error("{0}: RedirectError parsing '{1}'".format(articleIndex, articleName))
			return 0
		except wikipedia.exceptions.WikipediaException:
			self.log.error("{0}: WikipediaException parsing '{1}'".format(articleIndex, articleName))
			return 0

		# For each word in our list - attempt to find it in the given article
		distinctWordsFound = 0
		for word in self.cfg['wordDataList']:
			#self.log.debug('Attempting to find word {0}, res = {1}'.format(word.word, word.matcher.search(text)))
			if word.isPresentIn(text):				
				#print("Found word '{0}' in '{1}'".format(word, articleName))
				distinctWordsFound += 1
				self.cfg['resp_queue'].put(Response(word.word, articleIndex))
		self.log.debug("{0}: Found {1} distinct words in '{2}'".format(articleIndex, distinctWordsFound, articleName))

		# Any context (article) should have a minimum number of distinct words (2) else it's useless
		if distinctWordsFound < self.cfg['overlap']:
			return 0
		return 1

	def run(self):
		self.log.info('Starting...')

		# Run until worker grabs END token from word_queue
		while True:

			# Get next word on the queue
			wData = self.cfg['word_queue'].get()

			# If obtained END token then reply with END and quit
			if wData.isEndToken() == True:
				self.log.info('Done.')
				self.cfg['resp_queue'].put(Response().endToken())
				break

			self.log.info("{0}/{1}: Finding articles related to '{2}'".format(wData.index, self.cfg['numWords'], wData.word))

			# Obtain articles related to word (get more than we actually want since many may fail to meet overlap criteria)
			articleList = wikipedia.search(wData.word, results=self.cfg['articlesPerWord']*3)

			# Parse each article until we have parsed as many as 'articlesPerWord' denotes
			articleIndex = wData.index * self.cfg['articlesPerWord']
			count = 0
			for articleName in articleList:
				if count >= self.cfg['articlesPerWord']:
					break
				if articleName.endswith('(disambiguation)'):
					self.log.debug("Skipping article '{0}'".format(articleName))
					continue
				success = self.parseArticle(articleName, articleIndex)
				count += success
				articleIndex += success

			self.log.debug("Responding with word index {0}".format(wData.index))
			self.cfg['resp_queue'].put(wData.index)