name = 'liguimin'
if name.startswith('lig'):
    print 'Yes, the string starts with "lig"'

if 'g' in name:
    print 'Yes, it contains the string "g"'

if name.find('gui') != -1:
    print 'Yes, it contains the string "gui"'

delimiter = '_*_'
mylist = ['Brazil', 'Russia', 'India', 'China']
print (delimiter.join(mylist))
