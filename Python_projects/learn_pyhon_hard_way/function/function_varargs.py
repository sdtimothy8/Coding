#!/usr/bin/env python
# *-* coding: utf-8 *-*

def total(a=3, *numbers, **phonebook):
    print 'a:%d' %a

    #Loop the values in tuple
    for single_item in numbers:
        print 'single_item: %d' %single_item


    # Loop values in Dict
    for first_part, second_part in phonebook.items():
        print(first_part, second_part)

#print(total(10, 1, 2, 3, Jack=1123, John=2231, Inge=1560))
total(10, 1, 2, 3, Jack=1123, John=2231, Inge=1560)

