#! /usr/bin/python
# Encoding: UTF-8

# The interesting part of this file are the functions that generate
#  a pair of recursive tries: one to encode, the other to decode the same
#  encoding.

# The following license applies to this file, "table.py", not to the GUI
# frontend.

# Copyright (c) 2008 Petr Viktorin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from trie import Trie

external=False

"""
Put the NoReverse singleton in a trie definition item to omit that item
in the decoding trie. Useful for n-to-1 mappings.
"""
class _nrclass: pass
NoReverse=_nrclass()

rev_tries={}

def mkEncTrie(dct):
  """
  Makes an "encoding" trie from a description dict.
  Only call from mkTries to ensure that the reverse trie gets built as well
  """
  rv=Trie()
  for key, value in dct.iteritems():
    try:
      if value[1] is not NoReverse:
        raise Exception
    except: rv.add(key, value)
    else: rv.add(key, value[0])
  return rv

def mkDecTrie(dct):
  """
  Makes a "decoding", or "reverse" trie from a description dict
  Only call from mkTries to ensure that the encoding trie gets built as well
  """
  rv=Trie()
  for key, value in dct.iteritems():
    try: 
      if value[1] is not NoReverse:
        raise Exception
    except:
      try:
        if not callable(value[1].find_prefix):
          raise Exception
      except: rv.add(value, key)
      else:
        new_key=value[0]
        new_val=(key,revTrie(value[1]))+value[2:]
        rv.add(new_key, new_val)
  return rv

def mkTries(dct):
  """ Makes a (encoding, decoding) trie pair from a description dict """
  dirT, revT= mkEncTrie(dct), mkDecTrie(dct)
  rev_tries[id(dirT)]=revT
  return dirT, revT

def mkTrie(dct):
  """ Makes a (encoding, decoding) pair but only returns the encoding one """
  dirT, revT=mkTries(dct)
  return dirT

def revTrie(dirT):
  """ Returns the reversed trie from global storage. """
  return rev_tries[id(dirT)]

def check(*items):
  """ Check that the items have the trie functionality we need """
  for item in items:
    if not callable(item.forgiving_convert):
      raise TypeError("%r is not a trie" % item)

def load(file):
  """
  Load the given configuration file
  """
  exec file
  check(phonetic, r_phonetic, devanagari, r_devanagari)
  return phonetic, r_phonetic, devanagari, r_devanagari

try:
  phonetic, r_phonetic, devanagari, r_devanagari = load(open("transl_table.py","r"))
  external=True

except Exception, e:
  """ Load the hard-wired default tables if something goes wrong. """
  print e
  phonetic, r_phonetic, devanagari, r_devanagari = load("""
# Encoding: UTF-8

phonetic, r_phonetic=mkTries({
    u"á":  u"ā",
    u"í":  u"ī",
    u"ú":  u"ū",
    u"ů": (u"ū", NoReverse),
    u"ĺ":  u"ḷ",
    u"ľ":  u"ḹ",
    u"ŕ":  u"ṛ",
    u"ř":  u"ṝ",
    u"é": (u"e", NoReverse),
    u"ái":(u"ai",NoReverse),
    u"o": (u"o", NoReverse),
    u"ó":  u"o",
    u"áu":(u"au",NoReverse),

    u"H": u"ḥ",
    u"M": u"ṃ",
    u"´m": u"ṁ",

    u"ń": u"ṅ",
    u"ň": u"ñ",
    u"ť": u"ṭ",
    u"ď": u"ḍ",
    u"N": u"ṇ",
    u"č": u"c",
    u"š": u"ṣ",
    u"ś": u"ś",

    u"x": (u"ks",NoReverse),
    u"q": (u"kv",NoReverse),
    u"w": (u"v", NoReverse),
})

suffix2=mkTrie({
  u"":   u"",
  u"ḥ":  u"ः",
  u"ṁ":  u"ँ",
  u"ṃ":  u"ं",
})

suffix1=mkTrie({
  u"":    u"्",
  u"a":  (u"",  suffix2),
  u"ā":  (u"ा",  suffix2),
  u"i":  (u"ि",  suffix2),
  u"ī":  (u"ी",  suffix2),
  u"u":  (u"ु",  suffix2),
  u"ū":  (u"ू",  suffix2),
  u"ḷ":  (u"ॢ",  suffix2),
  u"ḹ":  (u"ॣ",  suffix2),
  u"ṛ":  (u"ृ",  suffix2),
  u"ṝ":  (u"ॄ",  suffix2),
  u"e":  (u"े",  suffix2),
  u"ai": (u"ै",  suffix2),
  u"o":  (u"ो",  suffix2),
  u"au": (u"ौ",  suffix2),
})

devanagari,r_devanagari=mkTries({
  u".":   u"।",
  u"..":  u"॥",
  u"...": u"॰",
  u"'":   u"ऽ",

  u"0": u"०",
  u"1": u"१",
  u"2": u"२",
  u"3": u"३",
  u"4": u"४",
  u"5": u"५",
  u"6": u"६",
  u"7": u"७",
  u"8": u"८",
  u"9": u"९",

  u"a": (u"अ",  suffix2),
  u"i": (u"इ",  suffix2),
  u"u": (u"उ",  suffix2),
  u"ṛ": (u"ऋ",  suffix2),
  u"ḷ": (u"ऌ",  suffix2),
  u"e": (u"ए",  suffix2),
  u"o": (u"ओ",  suffix2),
  u"ā": (u"आ",  suffix2),
  u"ī": (u"ई",   suffix2),
  u"ū": (u"ऊ",  suffix2),
  u"ṝ": (u"ॠ",  suffix2),
  u"ḹ": (u"ॡ",  suffix2),
  u"ai":(u"ऐ",  suffix2),
  u"au":(u"औ", suffix2),

  u"k": (u"क",   suffix1),
  u"kh": (u"ख",   suffix1),
  u"g": (u"ग",   suffix1),
  u"gh": (u"घ",   suffix1),
  u"ṅ": (u"ङ",   suffix1),
  u"c": (u"च",   suffix1),
  u"ch": (u"छ",   suffix1),
  u"j": (u"ज",   suffix1),
  u"jh": (u"झ",   suffix1),
  u"ñ": (u"ञ",   suffix1),
  u"ṭ": (u"ट",   suffix1),
  u"ṭh": (u"ठ",   suffix1),
  u"ḍ": (u"ड",   suffix1),
  u"ḍh": (u"ढ",   suffix1),
  u"ṇ": (u"ण",   suffix1),
  u"t": (u"त",   suffix1),
  u"th": (u"थ",   suffix1),
  u"d": (u"द",   suffix1),
  u"dh": (u"ध",   suffix1),
  u"n": (u"न",   suffix1),
  u"p": (u"प",   suffix1),
  u"ph": (u"फ",   suffix1),
  u"b": (u"ब",   suffix1),
  u"bh": (u"भ",   suffix1),
  u"m": (u"म",   suffix1),
  u"y": (u"य",   suffix1),
  u"r": (u"र",   suffix1),
  u"l": (u"ल",   suffix1),
  u"v": (u"व",   suffix1),
  u"ś": (u"श",   suffix1),
  u"ṣ": (u"ष",   suffix1),
  u"s": (u"स",   suffix1),
  u"h": (u"ह",   suffix1),
  u"kr": (u"क्र",   suffix1),
  u"kṣ": (u"क्ष",   suffix1),
  u"gr": (u"ग्र",   suffix1),
  u"gl": (u"ग्ल",   suffix1),
  u"ghr": (u"घ्र",   suffix1),
  u"cñ": (u"च्ञ",   suffix1),
  u"cm": (u"ज्म",   suffix1),
  u"jñ": (u"ज्ञ",   suffix1),
  u"jr": (u"ज्र",   suffix1),
  u"ḍr": (u"ड्र",   suffix1),
  u"ṇth": (u"ण्ठ",   suffix1),
  u"ṇḍh": (u"ण्ढ",   suffix1),
  u"ṇṇ": (u"ण्ण",   suffix1),
  u"ṇm": (u"ण्म",   suffix1),
  u"tr": (u"त्र",   suffix1),
  u"dr": (u"द्र",   suffix1),
  u"dhr": (u"ध्र",   suffix1),
  u"pr": (u"प्र",   suffix1),
  u"bj": (u"ब्ज",   suffix1),
  u"bb": (u"ब्ब",   suffix1),
  u"br": (u"ब्र",   suffix1),
  u"bhr": (u"भ्र",   suffix1),
  u"mp": (u"म्प",   suffix1),
  u"mr": (u"म्र",   suffix1),
  u"rk": (u"र्क",   suffix1),
  u"rkh": (u"र्ख",   suffix1),
  u"rg": (u"र्ग",   suffix1),
  u"rgh": (u"र्घ",   suffix1),
  u"rc": (u"र्च",   suffix1),
  u"rch": (u"र्छ",   suffix1),
  u"rj": (u"र्ज",   suffix1),
  u"rjh": (u"र्झ",   suffix1),
  u"rṇ": (u"र्ण",   suffix1),
  u"rt": (u"र्त",   suffix1),
  u"rth": (u"र्थ",   suffix1),
  u"rd": (u"र्द",   suffix1),
  u"rdh": (u"र्ध",   suffix1),
  u"rn": (u"र्न",   suffix1),
  u"rp": (u"र्प",   suffix1),
  u"rb": (u"र्ब",   suffix1),
  u"rbh": (u"र्भ",   suffix1),
  u"rm": (u"र्म",   suffix1),
  u"ry": (u"र्य",   suffix1),
  u"rl": (u"र्ल",   suffix1),
  u"rv": (u"र्व",   suffix1),
  u"rś": (u"र्श",   suffix1),
  u"rṣ": (u"र्ष",   suffix1),
  u"rs": (u"र्स",   suffix1),
  u"rh": (u"र्ह",   suffix1),
  u"lk": (u"ल्क",   suffix1),
  u"lg": (u"ल्ग",   suffix1),
  u"lh": (u"ल्ह",   suffix1),
  u"vr": (u"व्र",   suffix1),
  u"śr": (u"श्र",   suffix1),
  u"ṣv": (u"श्व",   suffix1),
  u"hr": (u"ह्र",   suffix1),
  u"sr": (u"स्र",   suffix1),
  u"sm": (u"स्म",   suffix1),
  u"sph": (u"स्फ",   suffix1),
  u"skh": (u"स्ख",   suffix1),

  u"kkh": (u"क्ख",   suffix1),
  u"km": (u"क्म",   suffix1),
  u"ky": (u"क्य",   suffix1),
  u"khy": (u"ख्य",   suffix1),
  u"gg": (u"ग्ग",   suffix1),
  u"gd": (u"ग्द",   suffix1),
  u"gdh": (u"ग्ध",   suffix1),
  u"gm": (u"ग्म",   suffix1),
  u"gy": (u"ग्य",   suffix1),
  u"ghm": (u"घ्म",   suffix1),
  u"ghy": (u"घ्य",   suffix1),
  u"cch": (u"च्छ",   suffix1),
  u"cy": (u"च्य",   suffix1),
  u"chy": (u"छ्य",   suffix1),
  u"jj": (u"ज्ज",   suffix1),
  u"jjh": (u"ज्झ",   suffix1),
  u"jm": (u"ज्म",   suffix1),
  u"jy": (u"ज्य",   suffix1),
  u"ñś": (u"ञ्श",   suffix1),
  u"ṭy": (u"ट्य",   suffix1),
  u"ṇṭ": (u"ण्ट",   suffix1),
  u"ṇḍ": (u"ण्ड",   suffix1),
  u"ṇy": (u"ण्य",   suffix1),
  u"ṇv": (u"ण्व",   suffix1),
  u"tk": (u"त्क",   suffix1),
  u"tth": (u"त्थ",   suffix1),
  u"tp": (u"त्प",   suffix1),
  u"tm": (u"त्म",   suffix1),
  u"ty": (u"त्य",   suffix1),
  u"tv": (u"त्व",   suffix1),
  u"ts": (u"त्स",   suffix1),
  u"thy": (u"थ्य",   suffix1),
  u"dm": (u"द्म",   suffix1),
  u"dhm": (u"ध्म",   suffix1),
  u"dhy": (u"ध्य",   suffix1),
  u"dhv": (u"ध्व",   suffix1),
  u"nt": (u"न्त",   suffix1),
  u"nth": (u"न्थ",   suffix1),
  u"nd": (u"न्द",   suffix1),
  u"ndh": (u"न्ध",   suffix1),
  u"nm": (u"न्म",   suffix1),
  u"ny": (u"न्य",   suffix1),
  u"nv": (u"न्व",   suffix1),
  u"ns": (u"न्स",   suffix1),
  u"pm": (u"प्म",   suffix1),
  u"py": (u"प्य",   suffix1),
  u"ps": (u"प्स",   suffix1),
  u"bd": (u"ब्द",   suffix1),
  u"bdh": (u"ब्ध",   suffix1),
  u"by": (u"ब्य",   suffix1),
  u"bhy": (u"भ्य",   suffix1),
  u"bhv": (u"भ्व",   suffix1),
  u"mb": (u"म्ब",   suffix1),
  u"mbh": (u"म्भ",   suffix1),
  u"my": (u"म्य",   suffix1),
  u"yy": (u"य्य",   suffix1),
  u"lp": (u"ल्प",   suffix1),
  u"ly": (u"ल्य",   suffix1),
  u"lv": (u"ल्व",   suffix1),
  u"vy": (u"व्य",   suffix1),
  u"śm": (u"श्म",   suffix1),
  u"śy": (u"श्य",   suffix1),
  u"ṣk": (u"ष्क",   suffix1),
  u"ṣṇ": (u"ष्ण",   suffix1),
  u"ṣp": (u"ष्प",   suffix1),
  u"ṣm": (u"ष्म",   suffix1),
  u"ṣy": (u"ष्य",   suffix1),
  u"ṣv": (u"ष्व",   suffix1),
  u"sk": (u"स्क",   suffix1),
  u"st": (u"स्त",   suffix1),
  u"sth": (u"स्थ",   suffix1),
  u"sp": (u"स्प",   suffix1),
  u"sy": (u"स्य",   suffix1),
  u"sv": (u"स्व",   suffix1),
  u"hm": (u"ह्म",   suffix1),
  u"hy": (u"ह्य",   suffix1),
  u"kk": (u"क्क",   suffix1),
  u"kc": (u"क्च",   suffix1),
  u"kn": (u"क्न",   suffix1),
  u"kv": (u"क्व",   suffix1),
  u"gn": (u"ग्न",   suffix1),
  u"ghn": (u"घ्न",   suffix1),
  u"ṅk": (u"ङ्क",   suffix1),
  u"ṅg": (u"ङ्ग",   suffix1),
  u"ṅkh": (u"ङ्ख",   suffix1),
  u"cc": (u"च्च",   suffix1),
  u"ñc": (u"ञ्च",   suffix1),
  u"ñj": (u"ञ्ज",   suffix1),
  u"ṭṭ": (u"ट्ट",   suffix1),
  u"ḍg": (u"ड्ग",   suffix1),
  u"ḍv": (u"ड्व",   suffix1),
  u"tn": (u"त्न",   suffix1),
  u"dg": (u"द्ग",   suffix1),
  u"dn": (u"द्न",   suffix1),
  u"db": (u"द्ब",   suffix1),
  u"dv": (u"द्व",   suffix1),
  u"dhn": (u"ध्न",   suffix1),
  u"nn": (u"न्न",   suffix1),
  u"pt": (u"प्त",   suffix1),
  u"pn": (u"प्न",   suffix1),
  u"pl": (u"प्ल",   suffix1),
  u"pv": (u"प्व",   suffix1),
  u"mn": (u"म्न",   suffix1),
  u"ml": (u"म्ल",   suffix1),
  u"ll": (u"ल्ल",   suffix1),
  u"ṣṭ": (u"ष्ट",   suffix1),
  u"ṣṭh": (u"ष्ठ",   suffix1),
  u"sn": (u"स्न",   suffix1),
  u"hṇ": (u"ह्ण",   suffix1),
  u"hn": (u"ह्न",   suffix1),
  u"hl": (u"ह्ल",   suffix1),
  u"hv": (u"ह्व",   suffix1),
  u"kt": (u"क्त",   suffix1),
  u"kl": (u"क्ल",   suffix1),
  u"tt": (u"त्त",   suffix1),
  u"dd": (u"द्द",   suffix1),
  u"ddh": (u"द्ध",   suffix1),
  u"dbh": (u"द्भ",   suffix1),
  u"dy": (u"द्य",   suffix1),
  u"śc": (u"श्च",   suffix1),
  u"śn": (u"श्न",   suffix1),
  u"śl": (u"श्ल",   suffix1),
  u"śv": (u"श्व",   suffix1),
  u"kty": (u"क्त्य",   suffix1),
  u"ktv": (u"क्त्व",   suffix1),
  u"kṣm": (u"क्ष्म",   suffix1),
  u"kṣmy": (u"क्ष्म्य",   suffix1),
  u"kṣy": (u"क्ष्य",   suffix1),
  u"gbhy": (u"ग्भ्य",   suffix1),
  u"cchr": (u"च्छ्र",   suffix1),
  u"jjv": (u"ज्ज्व",   suffix1),
  u"tkv": (u"त्क्व",   suffix1),
  u"tkṣ": (u"त्क्ष",   suffix1),
  u"ttr": (u"त्त्र",   suffix1),
  u"ttv": (u"त्त्व",   suffix1),
  u"tpr": (u"त्प्र",   suffix1),
  u"tmy": (u"त्म्य",   suffix1),
  u"try": (u"त्र्य",   suffix1),
  u"tsth": (u"त्स्थ",   suffix1),
  u"tsn": (u"त्स्न",   suffix1),
  u"tsy": (u"त्स्य",   suffix1),
  u"tsv": (u"त्स्व",   suffix1),
  u"ddv": (u"द्द्व",   suffix1),
  u"ddhy": (u"द्ध्य",   suffix1),
  u"ddhv": (u"द्ध्व",   suffix1),
  u"dbr": (u"द्ब्र",   suffix1),
  u"dbhy": (u"द्भ्य",   suffix1),
  u"dry": (u"द्र्य",   suffix1),
  u"dvy": (u"द्व्य",   suffix1),
  u"nty": (u"न्त्य",   suffix1),
  u"ntr": (u"न्त्र",   suffix1),
  u"ntv": (u"न्त्व",   suffix1),
  u"ndr": (u"न्द्र",   suffix1),
  u"nvy": (u"न्व्य",   suffix1),
  u"nsy": (u"न्स्य",   suffix1),
  u"nhr": (u"न्ह्र",   suffix1),
  u"pty": (u"प्त्य",   suffix1),
  u"ptry": (u"प्त्र्य",   suffix1),
  u"psy": (u"प्स्य",   suffix1),
  u"bdhy": (u"ब्ध्य",   suffix1),
  u"ṣkr": (u"ष्क्र",   suffix1),
  u"ṣṭr": (u"ष्ट्र",   suffix1),
  u"ṣṭv": (u"ष्ट्व",   suffix1),
  u"sty": (u"स्त्य",   suffix1),
  u"str": (u"स्त्र",   suffix1),
  u"stv": (u"स्त्व",   suffix1),
  u"rtsny": (u"र्त्स्न्य",   suffix1),
})
""")
