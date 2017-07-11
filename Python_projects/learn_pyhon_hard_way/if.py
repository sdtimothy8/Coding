# Two points: 
# 1) Different type object comparison, compare their type name.
# 2) The return type of method raw_input() is string.
number = 23
print 'Please input an integer:'
guess = int(raw_input('> '))

while (number != guess):
    if guess < number:
        print 'No, it is a little higher than that.'
    else:
        print 'No, it is a little lower than that.'

    print(number)
    print(guess)
    guess = int(raw_input('> ')); 

print 'Congratuations! You get it!'
print 'Done'
