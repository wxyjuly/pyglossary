#!/usr/bin/python
import sys
import io
import gzip

from os.path import abspath, dirname

rootDir = dirname(dirname(dirname(abspath(__file__))))
print("adding:", rootDir)
sys.path.insert(0, rootDir)
from pyglossary import Glossary

g = Glossary()
g.read(sys.argv[1], direct=False)

#g.writeTabfile(filename=sys.argv[1] + ".txt")

fileObj = gzip.open(io.BytesIO(), "w")
g.writeTabfile(fileObj=fileObj)

"""

22244	  direct tabfile -> tabfile
24780	  direct tabfile -> Gzip BytesIO tabfile
38580	  direct tabfile -> StringIO tabfile
52348	indirect tabfile -> tabfile
54668	indirect tabfile -> Gzip BytesIO tabfile
68368	indirect tabfile -> StringIO tabfile

~2.5k	size of Gzip BytesIO tabfile
~16k	size of StringIO tabfile
~30k	size of glos._data

"""

