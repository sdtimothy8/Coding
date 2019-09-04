#!/usr/bin/python
#**** coding:utf-8 ******

class Employee:
    """ Define a class named Employee """
    empCount = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1


    def displayCount(self):
        print "Total Employee %d" % Employee.empCount
    
    def displayEmployee(self):
        print "Name: ", self.name, ", Salary: ", self.salary


emp1 = Employee("ligm", 10000)
emp2 = Employee("huimin", 3000)

emp1.displayEmployee()
emp2.displayEmployee()

print "Toatal Employee count: %d" %Employee.empCount

# The attribute of Class
print "Employee.__doc__", Employee.__doc__
print "Employee.__name__", Employee.__name__
print "Employee.__module__", Employee.__module__
print "Employee.__bases__", Employee.__bases__
print "Employee.__dict__", Employee.__dict__
