# -*- coding: utf-8 -*-

__version__ = '1.5.4'
__author__ = 'dzoni.prezime@gmail.com'

"""
To convert a number to a word use to_words(n) function
"""


def _iter_flatten(iterable):
    """
    Utility function to flatten iterables.
    :param iterable:
    :return:
    """
    it = iter(iterable)
    for e in it:
        if isinstance(e, (list, tuple)):
            for f in _iter_flatten(e):
                yield f
        else:
            yield e


def _translate(n, words=True):
    word = {0: u'nula', 1: u'jedan', 2: u'dva', 3: u'tri', 4: u'četiri', 5: u'pet', 6: u'šest', 7: u'sedam', 8: u'osam',
            9: u'devet', 10: u'deset', 11: u'jedanaest', 12: u'dvanaest', 13: u'trinaest', 14: u'četrnaest', 15: u'petnaest',
            16: u'šesnaest', 17: u'sedamnaest', 18: u'osamnaest', 19: u'devetnaest'}
    if not words:
        word = {v: k for k, v in word.items()}
    return word[n]


def _parse_parts(n):
    result = []
    string = n
    teen = True if 10 < int(n[-2:]) < 20 else False

    n = int(n)
    if n < 20:
        result.append(_translate(n))
        return result
    elif teen:
        first = int(string[:-2])
        last = int(string[-2:])
        result.append(_translate(first) + 'sto')
        result.append(_translate(last))
    elif 20 <= n:
        string = list(str(n)[::-1])
        rev = []
        for en, i in enumerate(string):
            if en == 0:
                result.append(_translate(int(i)))
            elif en == 1:
                result.append(_translate(int(i)) + _translate(10))
            elif en == 2:
                result.append(_translate(int(i)) + 'sto')
        for i in reversed(result):
            rev.append(i)
        result = rev
    return result


def _correct_words(iterable):
    changes = {u'jedansto': u'sto', u'dvasto': u'dvesta', u'tristo': u'trista', u'devetdeset': u'devedeset',
               u'šestdeset': u'šezdeset', u'petdeset': u'pedeset', u'četirideset': u'ćetrdeset', u'jedandeset': u'deset',
               u'nuladeset': ''}
    for i in iterable:
        if not i == 'nula':
            try:
                yield i.replace(i, changes[i])
            except KeyError:
                yield i


def _final_polish(iterable):
    flat = [i for i in _iter_flatten(iterable)]
    new_list = []
    l = len(flat)
    for n, i in enumerate(flat):
        if i == 'dva' and not n + 1 == l:
            new_list.append(i.replace('dva', 'dve'))
        elif n + 1 < l and flat[n + 1] == 'hiljada':
            new_list.append(i.replace('jedan', 'jedna'))
        elif i == 'hiljada' and n - 1 >= 0 and flat[n - 1] in ['dva', 'tri', u'četiri']:
            new_list.append(i.replace('hiljada', 'hiljade'))
        else:
            new_list.append(i)

    return new_list


def to_words(n, long=True):
    """
    Converts a integer of a paramater n to a list of words in Serbian language.
    :param n:
    :param long: bool. default is True. Specifies if translator should use long or short scale.
                See https://bs.wikipedia.org/wiki/Duga_i_kratka_skala for more information.
    :return: list of strings
    :example: to_words(12456) --> ['dvanaest', 'hiljada', 'cetiristo', 'pedeset', 'sest']
    """
    n = int(n)
    if n == 0:
        return 'nula'
    result = []
    string = str(n)
    l = len(string)
    skip = 3
    rev = string[::-1]
    parts = [rev[i:i + skip][::-1] for i in range(0, l, skip)]
    if long:
        addition = {0: None, 1: {1: 'hiljadu', 2: 'hiljade', 5: 'hiljada'},
                    2: {1: 'milion', 2: 'miliona', 5: 'miliona'},
                    3: {1: 'milijardu', 2: 'milijarde', 5: 'milijardi'}, 4: {1: 'bilion', 2: 'biliona', 5: 'biliona'},
                    5:
                        {1: 'bilijardu', 2: 'bilijarde', 5: 'bilijardi'},
                    6: {1: 'trilion', 2: 'triliona', 5: 'triliona'},
                    7: {1: 'trilijardu', 2: 'trilijarde', 5: 'trilijardi'},
                    8: {1: 'kvadrilion', 2: 'kvadriliona', 5: 'kvadriliona'}}
    else:
        addition = {0: None, 1: {1: 'hiljadu', 2: 'hiljade', 5: 'hiljada'},
                    2: {1: 'milion', 2: 'miliona', 5: 'miliona'},
                    3: {1: 'bilion', 2: 'biliona', 5: 'biliona'}, 4: {1: 'trilion', 2: 'triliona', 5: 'triliona'},
                    5: {1: 'kvadrilion', 2: 'kvadriliona', 5: 'kvadriliona'},
                    6: {1: 'kvintilion', 2: 'kvintiliona', 5: 'kvintiliona'},
                    7: {1: 'sekstilion', 2: 'sekstiliona', 5: 'sekstiliona'},
                    8: {1: 'septilion', 2: 'septiliona', 5: 'septiliona'}}
    for i, p in enumerate(parts):
        part = []
        for cor in _correct_words(_parse_parts(p)):
            if cor:
                part.append(cor)
        result.append(part)
    parse_three = []
    for c, i in enumerate(result):
        num = int(parts[c])
        pos = addition[c]
        if pos:
            # print c, num, i, pos
            if num == 1:
                i = pos[1]
            elif 1 < num < 5:
                i = [i[0], pos[2]]
            elif num >= 5:
                i = [i, pos[5]]

        parse_three.append(i)
    rev = []
    for i in reversed(parse_three):
        rev.append(i)
    return _final_polish(rev)

__all__ = ['to_words']


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('integer', help='this is the integer to transcribe', type=int)
    parser.add_argument('-s', '--short', help='transcribe using short scale numbers', action='store_true')
    parser.add_argument('--string', help='convert to string', action='store_true')
    parser.add_argument('-c', '--capitalize', help='capitalize the output string', action='store_true')
    args = parser.parse_args()
    l = not args.short
    s = to_words(args.integer, long=l)
    if args.string:
        s = ''.join(s)
        if args.capitalize:
            s = s.capitalize()
    print s
