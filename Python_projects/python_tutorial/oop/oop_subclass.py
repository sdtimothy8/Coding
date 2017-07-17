#!/usr/bin/env python
# *-* coding: utf-8 *-*

class SchoolMember:
    """Any member in school"""
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print ('(Initialized SchoolMember: {})'.format(self.name))

    def tell(self):
        """show my detail info"""
        print('Name:"{}" Age:"{}"'.format(self.name, self.age))


class Teacher(SchoolMember):
    """Teacher in school"""
    def __init__(self, name, age, salary):
        SchoolMember.__init__(self, name, age)
        self.salary = salary
        print 'Initialized Teacher: %s'  %self.name

    def tell(self):
        SchoolMember.tell(self)
        print('Salary: "{:d}"'.format(self.salary))


class Student(SchoolMember):
    """ Student in school"""
    def __init__(self, name, age, marks):
        SchoolMember.__init__(self, name, age)
        self.marks = marks
        print 'Intialized student: %s' %self.name

    def tell(self):
        SchoolMember.tell(self)
        print 'Marks: %d' %self.marks


t = Teacher('Ligm', 28, 20000)
s = Student('Jiale', 3, 5000)

print '\n'

members = [t, s]
for member in members:
    member.tell()
