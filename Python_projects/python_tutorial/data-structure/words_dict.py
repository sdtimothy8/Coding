#!/usr/bin/python
#coding: utf-8

dictionary = {}
flag = 'a'
page = 'a'
off = 'a'

while flag == 'a' or 'c':
    flag = raw_input("Append or search words:(a\c): ")
    # Append the new word
    if flag == 'a':
        value = raw_input("Please input the new word: ")
        description = raw_input("Please input the description: ")
        dictionary[str(value)] = str(description)

    elif flag == 'c':
        word = raw_input("Please input the word to be searched: ")
        if dictionary.has_key(str(word)):
            print "Word: %s, Description: %s" %(str(word), dictionary[str(word)])
        else:
            print "Not find this word, it will be added into the dict!"
    else:
        print "Invalid input, please input the right value."
        flag = 'a'

