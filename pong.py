# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos=[WIDTH/2,HEIGHT/2]
paddle1_pos=[0,HEIGHT/2-HALF_PAD_HEIGHT]
paddle2_pos=[WIDTH,HEIGHT/2-HALF_PAD_HEIGHT]
paddle1_vel=0
paddle2_vel=0
score1=0
score2=0
vel=[0,0]
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    global LEFT,RIGHT
    ball_pos=[WIDTH/2,HEIGHT/2]
    vel[0]=random.randrange(120,240)/60
    vel[1]=-random.randrange(60,180)/60
    if direction==LEFT:
        vel[0]=vel[0]*(-1)
    elif direction==RIGHT:
        vel[0]=vel[0]*1
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos=[0,HEIGHT/2-HALF_PAD_HEIGHT]
    paddle2_pos=[WIDTH,HEIGHT/2-HALF_PAD_HEIGHT]
    paddle1_vel=0
    paddle2_vel=0
    score1=0
    score2=0
    spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    player1=str(score1)
    player2=str(score2)
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0]+=vel[0]
    ball_pos[1]+=vel[1]
    if (ball_pos[1]<=BALL_RADIUS) or (ball_pos[1]>=HEIGHT-BALL_RADIUS):
        vel[1]=-vel[1]
    if ball_pos[0]<=(BALL_RADIUS+PAD_WIDTH):     
        if ball_pos[1]>=paddle1_pos[1]:
            if ball_pos[1]<=paddle1_pos[1]+PAD_HEIGHT:                
                vel[0]=-vel[0]
                vel[0]*=1.1
                vel[1]*=1.1
            
            elif ball_pos[1]>paddle1_pos[1]+PAD_HEIGHT: 
                score2+=1
                spawn_ball(RIGHT)
        else:
            score2+=1
            spawn_ball(RIGHT)
            
    if ball_pos[0]>=(WIDTH-BALL_RADIUS-PAD_WIDTH):            
            if ball_pos[1]>=paddle2_pos[1]:                
                if ball_pos[1]<=paddle2_pos[1]+PAD_HEIGHT:                    
                    vel[0]=-vel[0]
                    vel[0]*=1.1
                    vel[1]*=1.1

                elif ball_pos[1]>paddle2_pos[1]+PAD_HEIGHT:                 
                    score1+=1 
                    spawn_ball(LEFT)
            else:
                score1+=1 
                spawn_ball(LEFT)        
        
    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,1,'White','White')
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos[1]>0 and paddle1_vel<0) or (paddle1_pos[1]<HEIGHT-PAD_HEIGHT and paddle1_vel>0):        
        paddle1_pos[1]+=paddle1_vel
    if (paddle2_pos[1]>0 and paddle2_vel<0) or (paddle2_pos[1]<HEIGHT-PAD_HEIGHT and paddle2_vel>0):
        paddle2_pos[1]+=paddle2_vel
    # draw paddles
    canvas.draw_line(paddle1_pos,[0,paddle1_pos[1]+PAD_HEIGHT],2*PAD_WIDTH,"White")
    canvas.draw_line(paddle2_pos,[WIDTH,paddle2_pos[1]+PAD_HEIGHT],2*PAD_WIDTH,"White")
    # draw scores
    canvas.draw_text(player1,(180, 100), 40, 'Green')
    canvas.draw_text(player2,(400,100),40,'Green') 
    
def keydown(key):
    global paddle1_vel, paddle2_vel,time
    if key==simplegui.KEY_MAP['w']:
            paddle1_vel-=5
    elif key==simplegui.KEY_MAP['s']:
            paddle1_vel+=5
    elif key==simplegui.KEY_MAP['up']:
            paddle2_vel-=5
    elif key==simplegui.KEY_MAP['down']:
            paddle2_vel+=5
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP['w']:
        paddle1_vel=0
    elif key==simplegui.KEY_MAP['s']:
        paddle1_vel=0
    elif key==simplegui.KEY_MAP['up']:
        paddle2_vel=0
    elif key==simplegui.KEY_MAP['down']:
        paddle2_vel=0

def button_restart():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', button_restart,100)

# start frame
new_game()
frame.start()
