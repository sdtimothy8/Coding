# ab means 'Adress Book'
ab = {
     'ligm': 'Jinan',
     'Huimin': 'Yuncheng',
     'Jiale': 'Wanxiang',
     'God': 'Tianguo'
}

print ' Ligm\'s address is:', ab['ligm'] 

# Delete one key-value pair
del ab['Jiale']
print ('\nThere are {} contacts in the address-book\n'.format(len(ab)))

for name, address in ab.items():
    print 'Contact {} at {}'.format(name, address)

# add new key-value pair
ab['Mama'] = 'Tangwang' 

if 'Mama' in ab:
    print '\nMama\'s address is:', ab['Mama'] 
