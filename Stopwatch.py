# template for "Stopwatch: The Game"
#http://www.codeskulptor.org/#user29_UMvv8SW7M5_1.py
import simplegui
import time
# define global variables
interval=100
clock=0
A=0
B=0
C=0
D=0
win=0
thetry=0
is_time_run=0
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global A
    global B
    global C
    global D
    D=clock%10
    min_l=clock/10
    C=min_l%10
    min_h=min_l/10
    B=min_h%6
    A=t/(10*60)
    return str(A)+":"+str(B)+str(C)+"."+str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global is_time_run
    timer.start()
    is_time_run=1

def stop():
    global is_time_run
    global win
    global thetry
    if is_time_run==1:
        timer.stop()
        thetry+=1
        if clock>0 and D==0:
            win+=1
        is_time_run=0

def reset():
    global clock
    global thetry
    global win
    win=0
    thetry=0
    clock=0
    timer.stop()

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global clock
    clock+=1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(clock), (75, 100), 20, 'white')
    string=str(win)+"/"+str(thetry)
    canvas.draw_text(string,(165,20),20,"green")
    
# create frame
frame=simplegui.create_frame('Stop Watch', 200, 200)

# register event handlers
frame.add_button('Start', start, 100)
frame.add_button('Stop', stop, 100)
frame.add_button('Reset', reset, 100)
timer = simplegui.create_timer(interval, timer_handler)
frame.set_draw_handler(draw_handler)

# start frame
frame.start()

# Please remember to review the grading rubric
