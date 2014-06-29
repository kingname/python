# implementation of card game - Memory
# http://www.codeskulptor.org/#user30_6DkCiA2OMN_4.py

import simplegui
import random
state=0
turn=0
a=range(16)
lst1=range(8)
lst2=range(8)
lst=lst1+lst2
click_time=0
random.shuffle(lst)
two=[]
color0=("green","green","green","green","green","green","green","green",
       "green","green","green","green","green","green","green","green")
color=list(color0)
color_f="green"
# helper function to initialize globals
def new_game():
    global turn,color,state,click_time,two
    turn = 0
    label.set_text("Turns = 0")
    color=list(color0)
    click_time=0
    state=0
    random.shuffle(lst)
    two=[]
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state,turn,click_time
    k=pos[0]/50
    if color[k]=="green": 
        click_time+=1
        turn=click_time/2
        label.set_text("Turns = "+str(turn)) 
        two.append(k)        
        color[k]="black"
        if state==2:            
            state=1
            if lst[two[click_time-3]]!=lst[two[click_time-2]]:              
                color[two[click_time-3]]="green"
                color[two[click_time-2]]="green"               
            #turn+=1
                       
        else:
            state+=1          
                                 
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in a:
        canvas.draw_polygon([[i*50, 0], [(i+1)*50, 0],[(i+1)*50, 100],[i*50, 100] ], 1, 'black',color[i])
        canvas.draw_text(str(lst[i]), (i*50+17, 60), 30, color_f)


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
