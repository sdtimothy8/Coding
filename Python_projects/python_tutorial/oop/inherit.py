#!/usr/bin/python
# **** coding: utf-8 ****

class Parent:
    """Define a parent class """
    parentAttr = 100
    def __init__(self):
        print "Call parent's constructor!"

    def parentMethod(self):
        print "Call parent's method!"

    def setAttr(self, attr):
        Parent.parentAttr = attr

    def getAttr(self):
        print "Parent attribute: ", Parent.parentAttr



# Define a subclass

class Child(Parent):
    def __init__(self):
        print "Call child's constructor!"


    def childMethod(self):
        print "Call child's method!"


#Main Code
c = Child()
c.childMethod()
c.parentMethod()
c.setAttr(200)
c.getAttr()
