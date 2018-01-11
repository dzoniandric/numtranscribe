# numtranscribe

This is simple Python program that enables you to convert integer numbers to list of words in Serbian language. It supports integers under 10^25 (Septilion in short scale or Kvadrilion in long scale).

## INSTALLATION

Simply copy numtranscribe.py to your project, package or site-packages. 
Setup.py will be available with the next major version.

## RUNNING

### How to check if the package is installed?

import numtranscribe
print numtranscribe.__version__

## HOW TO USE?

Simpli import the module and call to_words() function with integer as a paramater. With long=[bool] you can specify if you want to use a long or a short scale for translating. Default for Serbian language is long=True. You can find more about scales on: https://bs.wikipedia.org/wiki/Duga_i_kratka_skala

>>> from numtranscribe import to_words
>>> w = to_words(12456)
[u'dvanaest', 'hiljada', u'\u010detiristo', u'pedeset', u'\u0161est']

### Difference between long and short scales:

>>> from numtranscribe import to_words
>>> l = to_words(7831284232315690) # long paramater defaults to True, so you can ommit it.
>>> s = to_words(7831284232315690, long=False)
>>> print l
>>> print '------'
>>> print s
[u'sedam', 'bilijardi', u'osamsto', u'trideset', u'jedan', 'biliona', u'dvesta', u'osamdeset', u'\u010detiri', 'milijardi', u'dvesta', u'trideset', u'dve', 'miliona', u'trista', u'petnaest', 'hiljada', u'\u0161eststo', u'devedeset']
------
[u'sedam', 'kvadriliona', u'osamsto', u'trideset', u'jedan', 'triliona', u'dvesta', u'osamdeset', u'\u010detiri', 'biliona', u'dvesta', u'trideset', u'dve', 'miliona', u'trista', u'petnaest', 'hiljada', u'\u0161eststo', u'devedeset']


then you can convert it to a string like you would do normally in Python (and Capitalize the first letter):

>>> ''.join(w).capitalize()
Dvanaesthiljadačetiristopedesetšest


for help on using the to_words() use: 
>>> import numtranscribe
>>> help(numtranscribe.to_words)

