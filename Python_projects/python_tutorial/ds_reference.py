print('Simple Assignment')
shoplist = ['apple', 'mango', 'carrot', 'banana']
# mylist 
mylist = shoplist

# delete the first shopping item
del shoplist[0]

print 'shoplist is', shoplist
print 'mylist is', mylist

print 'Copy by making a full slice'
mylist = shoplist[:]
del mylist[0]

print '\nshoplist is:', shoplist
print 'mylist is:', mylist
