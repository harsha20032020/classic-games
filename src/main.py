import numpy as np 
import os
from colorama import Fore, init, Back, Style
import time
import sys
import termios
import tty
import signal
import math
import time

from sqlalchemy import false

from buildings import Cannon,Huts,Wizard_tower,Townhall
from troops import Barbarians,Archers
from heroes import Board,King
class Get:
    """Class to get input."""

    def __call__(self):
        """Defining __call__."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class AlarmException(Exception):
    """Handling alarm exception."""
    pass


def alarmHandler(signum, frame):
    """Handling timeouts."""
    raise AlarmException


def input_to(getch, timeout=1):
    """Taking input from user."""
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        text = getch()
        signal.alarm(0)
        return text
    except AlarmException:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return None

blank_arr=[]   
th_destroyed=False

            

          
            
width=30
height=120
display = Board(width,height) #width=30, height=30
display.get_board()
#display.print_board()
print("Please Enter the level you want to play!!")
level=input()
print("The level requested is "+level)
print("Please Enter the Hero to use (k for king and q for queen)")
hero=input()
print("The hero requested is "+hero)

#rendering Huts
hut_list=[Huts(10,50), Huts(20,50), Huts(10,60), Huts(20,60)]
for hut in hut_list:
    hut.render_hut(display.get_board())
    
#cannons rendered
# cannon_list=[]
# cannon_list.append(Cannon(10,55))
# cannon_list.append(Cannon(20,55))
# for cannon in cannon_list:
#     cannon.render_cannon(display.get_board())
if level=='1':
    cannon_list=[Cannon(10,53),Cannon(20,53)]
elif level=='2':
    cannon_list=[Cannon(10,53),Cannon(20,53),Cannon(15,40)]
elif level=='3':
    cannon_list=[Cannon(10,53),Cannon(20,53),Cannon(15,40),Cannon(15,70)]
#rendering cannons
for cannon in cannon_list:
    cannon.render_cannon(display.get_board())   
    
 
#wizard towers rendering 
if level=='1':
    wizard_list=[Wizard_tower(15,45),Wizard_tower(15,60)]
elif level=='2':
    wizard_list=[Wizard_tower(15,45),Wizard_tower(15,60),Wizard_tower(15,30)]
elif level=='3':
    wizard_list=[Wizard_tower(15,45),Wizard_tower(15,60),Wizard_tower(15,30),Wizard_tower(15,75)]
for wizard in wizard_list:
    wizard.render_wizard_tower(display.get_board())

    


#rendering th   
th=Townhall(13,53)
th.render_th(display.get_board())

#rendering barbarian King
if hero=='k':
    king=King(3,3)
    king.render_king(display.get_board())

total_max_barbarians=30
barbarian_list=[] #(2,1) is p and (2,28) is q and (27,1)
total_max_archers=6
archer_list=[]

def verify_win():
    if len(hut_list)==0 and len(cannon_list)==0 and th.get_strength()<=0:
        print ("""

        ██╗░░░██╗░█████╗░██╗░░░██╗  ░██╗░░░░░░░██╗██╗███╗░░██╗
        ╚██╗░██╔╝██╔══██╗██║░░░██║  ░██║░░██╗░░██║██║████╗░██║
        ░╚████╔╝░██║░░██║██║░░░██║  ░╚██╗████╗██╔╝██║██╔██╗██║
        ░░╚██╔╝░░██║░░██║██║░░░██║  ░░████╔═████║░██║██║╚████║
        ░░░██║░░░╚█████╔╝╚██████╔╝  ░░╚██╔╝░╚██╔╝░██║██║░╚███║
        ░░░╚═╝░░░░╚════╝░░╚═════╝░  ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝
        """)
        return True
    elif total_max_barbarians==0 and king.get_strength()<=0:
        print ("""
               
        ██╗░░░██╗░█████╗░██╗░░░██╗  ██╗░░░░░░█████╗░░██████╗███████╗
        ╚██╗░██╔╝██╔══██╗██║░░░██║  ██║░░░░░██╔══██╗██╔════╝██╔════╝
        ░╚████╔╝░██║░░██║██║░░░██║  ██║░░░░░██║░░██║╚█████╗░█████╗░░
        ░░╚██╔╝░░██║░░██║██║░░░██║  ██║░░░░░██║░░██║░╚═══██╗██╔══╝░░
        ░░░██║░░░╚█████╔╝╚██████╔╝  ███████╗╚█████╔╝██████╔╝███████╗
        ░░░╚═╝░░░░╚════╝░░╚═════╝░  ╚══════╝░╚════╝░╚═════╝░╚══════╝
        """)
        return True
    else:
        return False

starttime=time.time()
characters_list=[]
timestamp_list=[]
while True:
    
    #king.areal_damage(display.get_board(),cannon_list,hut_list,th)
    #king.deal_damage(display.get_board(),cannon_list,hut_list,th)
    ch=input_to(Get())
    #print("Health of king is {}".format(king.get_strength()))
    king_ratio=(king.get_strength()/16)*100
    print("King Health Bar {}%".format(king_ratio))
    for i in range(0,int(king_ratio)):
        print("█",end="")
    print("\n")
    print("Total Available Barbarians are {}".format(total_max_barbarians))
    print("Total Available Archers are {}".format(total_max_archers))
    if ch=='f':
        break
    if ch=='w':
        king.move_up(display.get_board())
    if ch=='s':
        king.move_down(display.get_board())
    if ch=='a':
        king.move_left(display.get_board())
    if ch=='d':
        king.move_right(display.get_board())
    if ch=='l':
        king.areal_damage(display.get_board(),cannon_list,hut_list,th)
    if ch==' ':
        king.deal_damage(display.get_board(),cannon_list,hut_list,th)
    if ch=='p':
        barb=Barbarians(2,1)
        barb.render_barbarians(display.get_board())
        barbarian_list.append(barb)
        total_max_barbarians-=1
    if ch=='q':
        barb=Barbarians(2,height-2)
        barb.render_barbarians(display.get_board())
        barbarian_list.append(barb)
        total_max_barbarians-=1
    if ch=='r':
        barb=Barbarians(width-3,1)
        barb.render_barbarians(display.get_board())
        barbarian_list.append(barb)
        total_max_barbarians-=1
    if ch=='b':
        arch=Archers(2,1)
        arch.render_archers(display.get_board())
        archer_list.append(arch)
        total_max_archers-=1
    if ch=='n':
        arch=Archers(2,height-2)
        arch.render_archers(display.get_board())
        archer_list.append(arch)
        total_max_archers-=1
    if ch=='m':
        arch=Archers(width-3,1)
        arch.render_archers(display.get_board())
        archer_list.append(arch)
        total_max_archers-=1
    for cannon in cannon_list:
        cannon.cannon_attack(barbarian_list,king,display.get_board())
    for wizard in wizard_list:
        wizard.wizard_tower_attack(barbarian_list,[],king,display.get_board())
    for barbarian in barbarian_list:
        barbarian.barbarian_motion(cannon_list,hut_list,wizard_list,th,display.get_board())
        print("The barbarian has health: {}".format(barbarian.get_strength())) 
        #barbarian.barbarian_motion(cannon_list,hut_list,th,display.get_board())
    for archer in archer_list:
        archer.archer_motion(cannon_list,hut_list,th,display.get_board())
        archer.archer_motion(cannon_list,hut_list,th,display.get_board())
    
    characters_list.append(ch)
    timestamp_list.append(time.time()-starttime)
    #time.sleep(1)
    display.print_board()
    if(verify_win()==True):
        break

file = open("list.txt", "w")
for index in range(len(characters_list)):
    file.write(str(characters_list[index]) + " " + str(timestamp_list[index]) + "\n")
file.close()