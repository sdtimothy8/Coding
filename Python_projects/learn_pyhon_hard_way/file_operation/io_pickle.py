#!/usr/bin/env python
#*-* coding: utf-8 *-*

import pickle
# The name of the file where we will store the object
shoplistfile = 'shoplist.data'
shoplist = ['apple', 'mango', 'carrot']

# write to the file
f = open(shoplistfile, 'wb')

# dump the object to a file
pickle.dump(shoplist, f)
f.close()

# destroy the shoplist variable
del shoplist

# Read back from the storage
f = open(shoplistfile, 'rb')

#Load the object from the file
storedlist = pickle.load(f)
print storedlist
