#! /usr/bin/python
# Encoding: UTF-8

# The following license applies to this file, "devanagari.py", not to the GUI
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

import sys,unicodedata
from trie import Trie
import table

transl_table={
  u"ab": u"XY",
  u"abc": u"XYZ",
}

_debug=False
#_debug=True

def make_trie(items):
  trie=Trie()
  for key,item in items:
    if _debug: print ": ".join([x.encode('UTF-8') for x in key,item])
    trie.add(*(unicodedata.normalize('NFC',x) for x in (key,item)))
  return trie

devanagari_trie=table.devanagari
phonetic_trie=table.phonetic

r_phonetic_trie=table.r_phonetic
r_devanagari_trie=table.r_devanagari

devanagari=devanagari_trie.forgiving_convert
phonetic=phonetic_trie.forgiving_convert

r_phonetic=r_phonetic_trie.forgiving_convert
r_devanagari=r_devanagari_trie.forgiving_convert

to_devanagari=lambda x: devanagari(phonetic(x))
to_phonetic=lambda x: r_devanagari(unicodedata.normalize('NFC',unicode(x)))

if __name__=="__main__":
  assert to_devanagari(u"abcdefghijklmnopqrstuvwxyz")==u"अब्च्देfघिज्क्ल्म्नोप्क्व्र्स्तुव्व्क्स्य्z"
