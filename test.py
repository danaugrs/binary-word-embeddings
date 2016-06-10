from sdr_utils import *

def review(listname, examples):

	print("\nReviewing '{0}' {1}\n".format(listname, '-'*50))

	# Set the list being analyzed
	setList(listname)

	# Find most similar SDRs to the ones in 'examples'
	for ex in examples:
		print('[{0}] is similar to: {1}'.format(ex, similarTo(ex, numResults=3)[1:]))

	# Print most similar pairs 
	print('\nMost similar pairs (in complete list):\n')
	topPairs = pairsBySimilarity()
	for pair in topPairs[:5]:
		print(pair)

# Top Brands ----------------------------------

review('topBrands', [
	'Google',
	'Toyota',	
	'AT&T',
	'Canon',
	'IBM',
	'HSBC',
	'MasterCard',
	'Costco',	
	'Netflix',
	'Pepsi',
	'NIKE',
	'Ford'
])

"""""""""""""""""""""""""""""""""""""""""""""""
Example output:

[Google] is similar to: [('Microsoft', 5), ('Amazon', 3)]
[Toyota] is similar to: [('Lexus', 13), ('Volkswagen', 7)]
[AT&T] is similar to: [('Verizon', 10), ('T-Mobile', 3)]
[Canon] is similar to: [('Panasonic', 3), ('Sony', 2)]
[IBM] is similar to: [('Microsoft', 6), ('SAP', 3)]
[HSBC] is similar to: [('Citi', 1), ('Chase', 1)]
[MasterCard] is similar to: [('Visa', 4), ('American Express', 3)]
[Costco] is similar to: [('Target', 5), ('Home Depot', 4)]
[Netflix] is similar to: [('Facebook', 1)]
[Pepsi] is similar to: [('Frito-Lay', 4), ('Coca-Cola', 4)]
[NIKE] is similar to: [('Adidas', 4), ('Uniqlo', 2)]
[Ford] is similar to: [('Chevrolet', 8), ('Toyota', 6)]

Most similar pairs (in complete list):

('Toyota', 'Lexus', 13)
('Disney', 'ESPN', 12)
('Audi', 'Volkswagen', 11)
('AT&T', 'Verizon', 10)
('J.P. Morgan', 'Chase', 8)

"""""""""""""""""""""""""""""""""""""""""""""""

# Countries -----------------------------------

review('countries', [
	'United States',
	'Russian Federation',
	'China',
	'India',
	'Colombia',
	'Singapore',
	'Norway',
	'Brazil',
	'Argentina'
])

"""""""""""""""""""""""""""""""""""""""""""""""
Example output:

[United States] is similar to: [('Canada', 47), ('United Kingdom', 42)]
[Russian Federation] is similar to: [('Ukraine', 7), ('Lithuania', 4)]
[China] is similar to: [('United States', 39), ('Taiwan', 38)]
[India] is similar to: [('China', 28), ('Pakistan', 17)]
[Colombia] is similar to: [('Venezuela', 11), ('Ecuador', 10)]
[Singapore] is similar to: [('Malaysia', 16), ('Indonesia', 15)]
[Norway] is similar to: [('Denmark', 20), ('Iceland', 16)]
[Brazil] is similar to: [('Argentina', 20), ('Portugal', 15)]
[Argentina] is similar to: [('Brazil', 20), ('Falkland Islands', 17)]

Most similar pairs (in complete list):

('American Samoa', 'Samoa', 59)
('Ireland', 'United Kingdom', 48)
('Guinea', 'Papua New Guinea', 47)
('Canada', 'United States', 47)
('South Sudan', 'Sudan', 46)

"""""""""""""""""""""""""""""""""""""""""""""""

# Other tests ---------------------------------

print('\nOther tests {0}\n'.format('-'*50))

brazil = sdrFor('Brazil')
argentina = sdrFor('Argentina')
portugal = sdrFor('Portugal')

print(similarTo('Brazil', numResults=6))
print(similarTo('Portugal', numResults=6))

# Brazil minus Portugal removes similarity with Europe
print(similarTo(brazil & ~portugal, numResults=6))