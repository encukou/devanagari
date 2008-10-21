# Based on the Trie by James Tauber:
#  http://jtauber.com/blog/2005/02/10/updated_python_trie_implementation/

# Modified by Petr Viktorin:
#  - Support of recursive tries - put a (value, next) in a Trie value
#     where next is a Trie of suffixes to include the word with all of
#     the suffixes. (To match the word itself, alse include an empty suffix)
#    The values of the trie need to be strings (or at least concatenable with +
#     to make this work
#  - Added the forgiving_convert method that converts the whole string, and
#     leave the unmatched parts unchanged
#  - Made the lookup method use find_prefix to avoid duplication of code.
#  - Added the [] operator, iteritems(), iterkeys(), itervalues(), items(),
#     keys(), values(). All of these respect recursive tries.
#  - Added the dictionary method, which returns a sorted list of (key, value)
#     pairs.

class Trie:
    """
    A Trie is like a dictionary in that it maps keys to values. However,
    because of the way keys are stored, it allows look up based on the
    longest prefix that matches.
    """

    def __init__(self, dct={}):
        self.root = [None, {}]
        for key, value in dct.iteritems():
          self.add(key, value)


    def add(self, key, value):
        """
        Add the given value for the given key.
        """
        
        curr_node = self.root
        for ch in key:
            curr_node = curr_node[1].setdefault(ch, [None, {}])
        curr_node[0] = value


    def find(self, key):
        """
        Return the value for the given key or None if key not found.
        """
        
        value, remainder=self.find_prefix(key)
        if remainder: return None
        return value


    def find_prefix(self, key):
        """
        Find as much of the key as one can, by using the longest
        prefix that has a value. Return (value, remainder) where
        remainder is the rest of the given string.
        """
        
        #import pprint,sys; print pprint.pprint((key, self.root))
        
        curr_node = self.root
        remainder = key
        value=curr_node[0]
        for ch in key:
            try:
                curr_node = curr_node[1][ch]
                value=curr_node[0]
            except KeyError:
                break
            remainder = remainder[1:]
        #print u",".join("%s"%x for x in (key,curr_node[0],remainder))
        try:
          next_find_prefix=value[1].find_prefix
          if not callable(next_find_prefix):
            raise Exception
          value=value[0]
        except (IndexError, AttributeError, AssertionError, TypeError):
          return (value, remainder)
        else:
          next_value, next_remainder = next_find_prefix(remainder)
          if next_value is None:
            return (None, remainder)
          else:
            return (value+next_value, next_remainder)

    def convert(self, keystring):
        """
        convert the given string using successive prefix look-ups.
        """
        
        valuestring = ""
        key = keystring
        while key:
            value, key = self.find_prefix(key)
            if not value:
                return (valuestring, key)
            valuestring += value
        return (valuestring, key)
        
    def forgiving_convert(self, keystring):
        """
        convert the given string using successive prefix look-ups.
        Leaves unmatched input untouched.
        """
        
        valuestring = ""
        key = keystring
        while key:
            old_key=key
            value, key = self.find_prefix(key)
            if not value:
              if len(old_key):
                value, key = old_key[0], old_key[1:]
              else:
                break
            valuestring += value
        return valuestring
        
    def iteritems(self):
      def iternode(node,prefix=""):
        if node[0] is not None:
          try:
            next_find_prefix=node[0][1].find_prefix
            if not callable(next_find_prefix):
              raise Exception
          except:
            yield prefix, node[0]
          else:
            for key, value in node[0][1].iteritems():
              yield prefix+key, node[0][0]+value
        for ch, inner_node in node[1].iteritems():
          for key, value in iternode(inner_node,prefix+ch):
            yield key, value
      for key, value in iternode(self.root):
        yield key, value

    def iterkeys(self):   return (k for k,v in self.iteritems())
    def itervalues(self): return (v for k,v in self.iteritems())
    def items(self):  return [x for x in self.iteritems()]
    def keys(self):   return [x for x in self.iterkeys()]
    def values(self): return [x for x in self.itervalues()]
    def __getitem__(self,key):
      value=self.find(key)
      if key is None:
        raise KeyError(key)
      return value
    
    def dictionary(self):
      items=self.items()
      items.sort(key=lambda itm: itm[0])
      return items

if __name__ == "__main__":    
    t = Trie()
    t.add("foo", "A")
    t.add("fo", "B")
    t.add("l", "C")
    
    assert t.find("fo") == "B"
    assert t.find("fool") == None

    assert t.find_prefix("fo") == ("B", "")
    assert t.find_prefix("fool") == ("A", "l")

    assert t.convert("fo") == ("B", "")
    assert t.convert("fool") == ("AC", "")
    assert t.forgiving_convert("f") == "f"
    assert t.forgiving_convert("foolish lump") == "ACish Cump"

    # A recursive trie
    rt = Trie()
    rt.add("bar", ("X", t))
    rt.add("ba", ("Y", t))
    rt.add("r", ("Z", t))
    assert rt.forgiving_convert("barfoo, rfool, baba") == "XA, ZAl, baba"
    t.add("", "")
    assert rt.forgiving_convert("barfoo, rfool, baba, rl") == "XA, ZAl, YY, ZC"
