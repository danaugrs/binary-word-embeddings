# Binary word embeddings from Wikipedia

Generates binary word embeddings for a provided list of words by naively analyzing Wikipedia.
Was meant partially as an exercise in Python for multi-threading and web requests.

For each word in the provided list the program fetches `n` Wikipedia articles.
Each article is represented by a bit in the embedding - if the word appears in that article the bit is set to 1.
This is an extremely simple approach to word embedding but the latent space discovered still shows very sensible semantic properties.

I only show similarity experiments here but word additions and subtractions also give sensible results in some cases.

## Nearest Neighbors

Once you've generated the data you can easily list a word's nearest neighbors.
The similarity metric used is the L1-norm of the bitwise AND.

- `similarTo('Google')` outputs `[('Microsoft', 5), ('Amazon', 3), ('Samsung', 3), ...]`
- `similarTo('Toyota')` outputs `[('Lexus', 13), ('Volkswagen', 7), ('Ford', 6), ('Hyundai', 4), ...]`
- `similarTo('Colombia')` outputs `[('Venezuela', 11), ('Ecuador', 10), ('Peru', 9), ...]`

## How to generate the data

To see available command line options: `generate.py -h`

Example usages:
- `generate.py -l countries`
- `generate.py --list topBrands --nworkers 10`

Several example lists are provided in the `/lists` directory.

## Example output from `test.py`

##### topBrands.list
```
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
```

##### countries.list
```
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
```
