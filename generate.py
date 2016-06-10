# Python modules
import argparse
import threading
import queue
import logging
import sys
import os.path 
from logging.handlers import RotatingFileHandler
from string import ascii_lowercase

# Third party
import wikipedia
from bitarray import bitarray

# My modules
import worker
import bitarray_io
from thread_messaging import WordData

#---------------------------------------------------------

LOGFILE = 'logs\main_thread.txt'

log = logging.getLogger('root')
log.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s %(levelname)s: %(threadName)s - %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)

fh = logging.handlers.RotatingFileHandler(LOGFILE, maxBytes=(1048576*5), backupCount=7)
fh.setFormatter(format)
log.addHandler(fh)

#---------------------------------------------------------------

def progressFilename(listname):
	"""Returns the progress filename for the provided listname"""
	return 'data\{0}.processed'.format(listname)

def saveProgress(listname, wordIndexes=[]):
	"""Saves to disk the list of word indexes (representing processed words)"""
	with open(progressFilename(listname), 'w') as f:
		f.writelines([ "{0}\n".format(str(x)) for x in wordIndexes ])

def loadProgress(listname):
	"""Retrieves from disk the list of indexes of words already processed"""
	if not os.path.isfile(progressFilename(listname)):
		saveProgress(listname)
	with open(progressFilename(listname), 'r') as f:
		return [ int(x) for x in f.readlines() ]

def listsFromFile(filename):
	"""Builds Python lists from file"""
	wordList = []
	wordDataList = []
	with open('lists\{0}'.format(filename)) as f:
		for wordCR in f:
			word = wordCR[:-1]  # Remove carriage return
			wordList.append(word)
			wordDataList.append(WordData(word))
	return (wordList, wordDataList)

def createWordFiles(wordlist, nbits):
	"""Creates a file with the specified number of bits for each word in the list"""
	log.debug('Creating word files for {0} words, each with {1} bits'.format(len(wordlist), nbits))
	for word in wordlist:
		log.debug(word)
		bitarray_io.save(word, bitarray('0'*nbits))
		
def main():
	global log

	# Parse command line options
	parser = argparse.ArgumentParser(description="Wikipedia Word SDR Scraper")
	parser.add_argument('-l', '--list',
		type        = str,
		default		= 'topBrands', #countries (best example)
		required    = False,
		help        = 'File containing list of words'
	)
	parser.add_argument('-d', '--wordsdirectory',
		type        = str,
		required    = False,
		help        = 'Directory for word files (defaults to filename of word list)'
	)
	parser.add_argument('-w', '--nworkers',
		type        = int,
		default		= 10,
		required    = False,
		help        = 'Number of workers (threads)'
	)
	parser.add_argument('-reset', '--reset',
		type        = bool,
		default		= False,
		required    = False,
		help        = 'Creates word files (DELETES ALL EXISTING DATA)'
	)
	args = parser.parse_args()
	print(args)

	if args.wordsdirectory:  # a directory to store the word files was specified
		listDir = bitarray_io.setDirectory(args.wordsdirectory)
	else:  # use the wordlist filename as the name of the directory
		listDir = bitarray_io.setDirectory(args.list)

	# Populate word list
	wordlist, wordDataList = listsFromFile(args.list + '.list')
	listsize = len(wordlist)

	# TODO Create statistics of unused bits, returned by worker
	# compile stats and show
	# Make sure that articles with most overlap are used by workers
	# TODO Allow user to specify overlap range
	# TODO Make argument
	articlesPerWord = 10

	if (args.reset or not os.listdir(listDir)):
		saveProgress(args.list)
		createWordFiles(wordlist, listsize * articlesPerWord)

	# Create queues
	word_queue = queue.Queue()
	resp_queue = queue.Queue()

	# Populate word_queue
	alreadyProcessedIndexes = loadProgress(args.list)
	for i in range(listsize):
		if i in alreadyProcessedIndexes:
			continue
		word_queue.put(WordData(wordlist[i], i))

	# add 'end's to work_queue for each worker
	for idx in range(args.nworkers):
		word_queue.put(WordData().endToken())

	# Create and start workers
	for idx in range(args.nworkers):

		# Create worker configuration dictionary
		wcfg = {
			'word_queue'		: word_queue,
			'resp_queue'		: resp_queue,
			'idx'				: idx,
			'wordDataList'		: wordDataList,
			'articlesPerWord'	: articlesPerWord,
			'numWords'			: len(wordlist),
			'overlap'			: 2 # min overlap
		}

		# Create worker thread and start it
		w = worker.Worker(wcfg)
		wt = threading.Thread(target=w.run, name="worker:%d" % idx)

		# Sets thread daemon to FALSE:
		# Program exits when no alive non-daemon threads are left.
		wt.daemon = False
		wt.start()

	done = 0  # Keep track of workers that are done

	while done < args.nworkers:

		# Get next Response object
		response = resp_queue.get()

		if type(response) == int:
			log.debug("Finished processing {0} ({1}/{2}) - saving progress...".format(wordlist[response], response, listsize))
			# Worker is done finding articles with that word
			# remove from remaining list
			currentProgress = loadProgress(args.list)
			currentProgress.append(response)
			saveProgress(args.list, currentProgress)
			continue

		# If Response is an end token it means the worker found an end token in the word_queue
		# and there are no more words to process
		if response.isEndToken():
			done += 1  # Increment the count of workers that are done		
			log.info('Received END token {0}'.format(done))

		else:
			# Set the appropriate bit on the appropriate word file
			bitarray_io.setBit(response.word, response.index)

			# Flood the log
			#log.debug('Set bit {0} on word {1}'.format(response.index, response.word))
			
	log.info('Done')

main()