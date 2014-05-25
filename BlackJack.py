# Mini-project #6 - Blackjack
# http://www.codeskulptor.org/#user31_n2tQqlub3t_4.py
import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
p_score = 0
d_score = 0
pocker=[]
p_win=0
d_win=0
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        if in_play==True:
            canvas.draw_image(card_back,CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        else:            
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
         
# define hand class
class Hand:
    def __init__(self):
        self.deck=[]	# create Hand object

    def __str__(self):
        ans = ""
        for i in range(len(self.deck)):            
            ans =ans+" "+ str(self.deck[i])       
        return "con"+ans
    
    def add_card(self, card):
        self.deck.append(card)	# add a card object to a hand

    def get_value(self):
        va=0
        flag=0 # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        if self.deck==[]:
            va=0
        else:            
            for i in range(len(self.deck)):                           
                va+=VALUES[self.deck[i].get_rank()]	# compute the value of the hand, see Blackjack video
                if self.deck[i].get_rank()=="A":
                    flag=1
            if flag==1 and va+10<21:
                va+=10
        return va  
    
    def draw(self, canvas, pos):
            # draw a hand on the canvas, use the draw method for cards        
        for i in range(len(player.deck)):
            card=player.deck[i]
            card.draw(canvas, [100+CARD_SIZE[0]*i, 100])     
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck=[]     # create a Deck object
        for i in range(0,4):        
            for j in range(0,13):            
                self.deck.append(Card(SUITS[i],RANKS[j]))

    def shuffle(self):        # shuffle the deck 
        random.shuffle(self.deck)    # use random.shuffle()

    def deal_card(self):       # deal a card object from the deck
        value=self.deck[0]
        self.deck.pop(0)
        return value
    
    def __str__(self):
        ans=""
        for i in range(len(self.deck)):            
            ans =ans+" "+ str(self.deck[i])
        return "xxxx"+ans	# return a string representing the deck 

#define event handlers for buttons
def deal():
    global outcome, in_play,pocker,player,dealer,p_win,d_win,d_score
    p_win=0
    d_win=0
    pocker=Deck()
    c1=pocker.deal_card
    pocker.shuffle()
    player=Hand()
    dealer=Hand()    
    player.add_card(pocker.deal_card()) 
    dealer.add_card(pocker.deal_card())
    player.add_card(pocker.deal_card())
    dealer.add_card(pocker.deal_card())
    if in_play==True:
        d_score+=1
    # your code goes here    
    in_play = True

def hit():
    global in_play,d_win,d_score
    if in_play==True and player.get_value()<=21:
        player.add_card(pocker.deal_card())
        if player.get_value()>21:
            d_win=2
            d_score+=1
            in_play=False    
       
def stand():
    global in_play,d_win,p_win,p_score,d_score
    if player.get_value()>21:
        d_win=2
        d_score+=1
    else:
        while dealer.get_value()<17:
            dealer.add_card(pocker.deal_card())
        if dealer.get_value()>21:
            p_win=2
            p_score+=1
        else:
            if dealer.get_value()>=player.get_value():
                d_win=1
                d_score+=1
            else:
                p_win=1
                p_score+=1
    in_play=False        
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('BlackJack!!', (200, 50), 40, 'white')
    canvas.draw_text('Dealer', (100, 180), 30, 'white')
    canvas.draw_text('Player', (100, 540), 30, 'white')
    canvas.draw_text('player '+str(p_score)+":"+str(d_score)+" dealer", (300, 120), 30, 'white')
    for i in range(len(player.deck)):        
        card=player.deck[i]
        card.draw(canvas, [100+CARD_SIZE[0]*i, 400])
    for i in range(len(dealer.deck)):        
        card2=dealer.deck[i]
        card2.draw(canvas, [100+CARD_SIZE[0]*i, 200])
    if in_play==True:
        canvas.draw_text('Hit or Stand?', (300, 540), 30, 'white')
    else:
        canvas.draw_text('Have a new deal?', (300, 540), 30, 'white')
        if p_win==1:
            canvas.draw_text('You win!!', (100, 350), 30, 'white') 
        elif d_win==1:
            canvas.draw_text('The dealer win the tie!!', (100, 350),30, 'white')
        elif d_win==2:
            canvas.draw_text('You have busted!!', (100, 350),30, 'white')
        elif p_win==2:
            canvas.draw_text('the dealer has busted!! YOU WIN!!', (100, 350),30, 'white')
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Black")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
player=Hand()
dealer=Hand()
deal()
frame.start()
# remember to review the gradic rubric
