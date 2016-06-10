from bitarray import bitarray
import os

parentdir = 'data'
directory = 'wordFiles'

def _wordFile(word, flags):
	"""Returns the requested word file"""
	return open('{0}\{1}\{2}'.format(parentdir, directory, word), flags)

def setDirectory(newdir):
	"""Sets the directory used my this module, residing under [parentdir]"""
	global directory
	directory = newdir
	path = '{0}\{1}'.format(parentdir, directory)
	os.makedirs(path, exist_ok=True)
	return path
		
def load(word):
	"""Returns the bitarray from the appropriate word file"""
	bArray = bitarray()
	with _wordFile(word, 'rb') as f:
		bArray.fromfile(f)
	return bArray

def save(word, bArray):
	"""Saves a bitarray to the appropriate word file"""
	with _wordFile(word, 'wb') as f:
		bArray.tofile(f)

def setBit(word, bitIndex, value=1):
	"""Sets a single bit on a word file"""
	bArray = bitarray()
	f = _wordFile(word, 'r+b')
	bArray.fromfile(f)
	bArray[bitIndex] = value
	f.seek(0)
	bArray.tofile(f)
	f.close()

def setBits(word, bitIndexes, values=None):
	"""Sets multiple bits on a word file"""
	bArray = bitarray()
	f = _wordFile(word, 'r+b')
	bArray.fromfile(f)
	if values:
		for i in bitIndexes:
			bArray[i] = values[i]
	else:
		for i in bitIndexes:
			bArray[i] = 1
	f.seek(0)
	bArray.tofile(f)
	f.close()

if __name__ == '__main__':

	setDirectory('test')

	save('testWord', bitarray('0'*2**4))
	print(load('testWord'))

	print('setting the 3rd bit to 1...')
	setBit('testWord', 2)
	print(load('testWord'))

	print('setting the 6th bit to 1...')
	setBit('testWord', 5)
	print(load('testWord'))


