# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
# http://www.codeskulptor.org/#user29_zoglME4wEf_0.py
import simplegui
import random
import math
# initialize global variables used in your code
secret_number=0
limit=0
up=100

# helper function to start and restart the game
def new_game():
    global secret_number
    global limit
    if(up==100):
        limit=7
        secret_number=random.randrange(0,100)
    else:
        limit=10
        secret_number=random.randrange(0,1000)
    print "New game. Range is from 0 to",up
    print "Number of remaining guesses is",limit,"\n"

# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global up
    up=100
    new_game()

def range1000():
    # button that changes range to range [0,1000) and restarts
    global up
    up=1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here
    global secret_number
    global limit
    guess=int(guess)
    limit-=1
    if(limit==-1):
        print "You lose!\n"
        new_game()
        return
    print "Guess was",guess
    print "Number of remaining guesses is",limit
    if(secret_number==guess):
        print "Correct!\n"
        new_game()
    elif(secret_number<guess):
        print "Lower\n"
    else:
        print "Higher\n"
    
# create frame
frame=simplegui.create_frame('guss number',200,200)

# register event handlers for control elements
frame.add_button("Range is [0,100)",range100,200)
frame.add_button("Range is [0,1000)",range1000,200)
guess=frame.add_input("Enter a guess:",input_guess,200)

# call new_game and start frame
new_game()
frame.start()
# always remember to check your completed program against the grading rubric
