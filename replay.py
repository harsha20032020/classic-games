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
class Board:
    def __init__(self,rows,columns):
        self.rows=rows
        self.columns=columns
        self.grid=[]
        for i in range(self.rows):
            rows=[]   
            for j in range(self.columns):
                if i==0 or i==self.rows-1:
                    rows.append("—")
                elif j==0 or j==self.columns-1:
                    rows.append("|")  
                elif i==1 and j==1:
                    rows.append("p")
                elif i==1 and j==self.columns-2:
                    rows.append("q") 
                elif i==self.columns-2 and j==1:
                    rows.append("r")
                else:
                    rows.append(" ")
            self.grid.append(rows)
            
    def get_board(self):
        return self.grid
    
    def print_board(self):
        for i in range(self.rows):
            for j in range(self.columns):
                print(self.grid[i][j],end="")
            print()
          
class Cannon:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=2
        self.height=2
        self.strength=8 #king takes 4 hits to destroy cannon
        self.range=6 #cannon can shoot 6 spaces
        self.damage=1 #cannon deals 1 damage
        
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_x(self,x):
        self.x=x
    def set_y(self,y):
        self.y=y
    def render_cannon(self,grid):
        if(self.x=="NONE" and self.y=="NONE"):
            return
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                #grid[i][j]="4"
                ratio = self.strength/8
                if ratio> 0.5:
                    grid[i][j]=Fore.GREEN+"C"+Style.RESET_ALL
                elif ratio> 0.25:
                    grid[i][j]=Fore.YELLOW+"C"+Style.RESET_ALL
                else:
                    grid[i][j]=Fore.RED+"C"+Style.RESET_ALL
        
        return grid
    def destroy_cannon(self,grid):
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                grid[i][j]=" "
        del self
    def get_strength(self):
        return self.strength
    def damage_taken(self):
        self.strength-=1
    
    
    # need to do barbarian and king interactions
    def cannon_attack(self,barblist,king,grid):
        #each cannon attacks the closest barbarian in barblist or if the king is closer than the barbarians, it attacks the king
        #if there are no barbarians, it attacks the king
        #if there are no barbarians and no king, it attacks nothing
        minval=1000
        minindex=0
        for barbarian in barblist:
            distance=math.sqrt((barbarian.get_x()-self.x)**2+(barbarian.get_y()-self.y)**2)
            if distance<minval:
                minval=distance
                minindex=barblist.index(barbarian)
        dist=math.sqrt((king.get_x()-self.x)**2 + (king.get_y()-self.y)**2)
        #print("min barb distance is {} and distance of king is {}".format(minval, dist))
        if(dist<minval and dist<=self.range):
            king.damage_taken()
            king.render_king(grid)
            if king.get_strength()<=0:
                king.delete_king(grid)
        elif(minval<=self.range):
            affected_barbarian=barblist[minindex]
            affected_barbarian.damage_taken()
            affected_barbarian.render_barbarians(grid)
            if affected_barbarian.get_strength()<=0:
                affected_barbarian.delete_barbarians(grid)
                barblist.remove(affected_barbarian)
            
        
            
                
class Huts:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=1
        self.height=1
        self.strength=4 #king takes 4 hits to destroy cannon
        
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_x(self,x):
        self.x=x
    def set_y(self,y):
        self.y=y
    def render_hut(self,grid):
        if(self.x=="NONE" and self.y=="NONE"):
            return
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                ratio = self.strength/4
                if ratio> 0.5:
                    grid[i][j]=Fore.GREEN+"H"+Style.RESET_ALL
                elif ratio> 0.25:
                    grid[i][j]=Fore.YELLOW+"H"+Style.RESET_ALL
                else:
                    grid[i][j]=Fore.RED+"H"+Style.RESET_ALL
        
        return grid
    def destroy_hut(self,grid):
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                grid[i][j]=" "
        del self
    def get_strength(self):
        return self.strength
    def damage_taken(self):
        self.strength-=1

class Townhall:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=4
        self.height=3
        self.strength=16 #king takes 6 hits to destroy th
        
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_x(self,x):
        self.x=x
    def set_y(self,y):
        self.y=y
    def render_th(self,grid):
        if(self.x=="NONE" and self.y=="NONE"):
            return
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                #grid[i][j]="4"
                ratio = self.strength/16
                if ratio> 0.5:
                    grid[i][j]=Fore.GREEN+"T"+Style.RESET_ALL
                elif ratio> 0.25:
                    grid[i][j]=Fore.YELLOW+"T"+Style.RESET_ALL
                else:
                    grid[i][j]=Fore.RED+"T"+Style.RESET_ALL
        
        return grid
    def destroy_th(self,grid):
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                grid[i][j]=" "
        del self
    def get_strength(self):
        return self.strength
    def damage_taken(self):
        self.strength-=1


class King:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=2
        self.height=2
        self.strength=16 #king takes 8 hits to get killed
        self.damage=1   #barbarian king deals 2 damage
        
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_x(self,x):
        self.x=x
    def set_y(self,y):
        self.y=y
    def get_strength(self):
        if self.strength<=0:
            return 0
        else:
            return self.strength
    def render_king(self,grid):
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                x=self.x
                y=self.y
                ratio = self.strength/16
                if ratio> 0.5:
                    grid[i][j]=Fore.GREEN+"K"+Style.RESET_ALL
                elif ratio> 0.25:
                    grid[i][j]=Fore.YELLOW+"K"+Style.RESET_ALL
                else:
                    grid[i][j]=Fore.RED+"K"+Style.RESET_ALL
        return grid
    def delete_king(self,grid):
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                grid[i][j]=" "
        del self
    def clear_king(self,grid):
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                grid[i][j]=" "
    def damage_taken(self):
        self.strength-=1
    def move_up(self,grid):
        x=self.x
        self.clear_king(grid)
        self.x=x-1
        self.render_king(grid)
        
    def move_down(self,grid):
        x=self.x
        self.clear_king(grid)
        self.x=x+1
        self.render_king(grid)
        
    def move_left(self,grid):
        y=self.y
        self.clear_king(grid)
        self.y=y-1
        self.render_king(grid)
        
    def move_right(self,grid):
        y=self.y
        self.clear_king(grid)
        self.y=y+1
        self.render_king(grid)
    
    def deal_damage(self,grid,list1,list2,th):
        x=self.x
        y=self.y
        for cannon in list1:
            if(cannon.get_x()==x and cannon.get_y()==y+2):
                cannon.damage_taken()
                cannon.render_cannon(grid)
                if(cannon.get_strength()<=0):
                    cannon.destroy_cannon(grid)
                    list1.remove(cannon)
        for hut in list2:
            if(hut.get_x()==x and hut.get_y()==y+2):
                hut.damage_taken()
                #print("the strength of hut is {}".format(hut.get_strength()))
                hut.render_hut(grid)
                if(hut.get_strength()<=0):
                    hut.destroy_hut(grid)
                    list2.remove(hut)
        if(th.get_x()==x and th.get_y()==y+2):
            th.damage_taken()
            #print("the strength of th is {}".format(th.get_strength()))
            th.render_th(grid)
            if(th.get_strength()<=0):
                th.destroy_th(grid)
    
    def areal_damage(self,grid,list1,list2,th):
        x=self.x
        y=self.y
        for cannon in list1:
            dist=math.sqrt((cannon.get_x() - x)**2 + (cannon.get_y() - y)**2)
            if(dist<=5):
                cannon.damage_taken()
                #print("the cannon at position {} {} has strength {}".format(cannon.get_x(),cannon.get_y(),cannon.get_strength()))
                cannon.render_cannon(grid)
                if(cannon.get_strength()<=0):
                    cannon.destroy_cannon(grid)
                    list1.remove(cannon)
        for hut in list2:
            dist=math.sqrt((hut.get_x() - x)**2 + (hut.get_y() - y)**2)
            if(dist<=5):
                hut.damage_taken()
                #print("the strength of hut is {}".format(hut.get_strength()))
                hut.render_hut(grid)
                if(hut.get_strength()<=0):
                    hut.destroy_hut(grid)
                    list2.remove(hut)
        dist=math.sqrt((th.get_x() - x)**2 + (th.get_y() - y)**2)
        if(dist<=5):
            th.damage_taken()
            #print("the strength of th is {}".format(th.get_strength()))
            th.render_th(grid)
            if(th.get_strength()<=0):
                th.destroy_th(grid)
            
class Barbarians:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=1
        self.height=1
        self.strength=4 #kbarbarians takes 4 hits to get killed
        self.damage=1   #barbarian king deals 1 damage
        
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_x(self,x):
        self.x=x
    def set_y(self,y):
        self.y=y
    def get_strength(self):
        if self.strength<=0:
            return 0
        else:
            return self.strength
    def render_barbarians(self,grid):
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                x=self.x
                y=self.y
                ratio = self.strength/4
                if ratio> 0.5:
                    grid[i][j]=Fore.GREEN+"B"+Style.RESET_ALL
                elif ratio> 0.25:
                    grid[i][j]=Fore.YELLOW+"B"+Style.RESET_ALL
                else:
                    grid[i][j]=Fore.RED+"B"+Style.RESET_ALL
        return grid
    def delete_barbarians(self,grid):
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                grid[i][j]=" "
        del self
    def clear_barbarians(self,grid):
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                grid[i][j]=" "
    def damage_taken(self):
        self.strength-=1
    # def move_up(self,grid):
    #     x=self.x
    #     self.clear_barbarians(grid)
    #     self.x=x-1
    #     self.render_barbarians(grid)
        
    # def move_down(self,grid):
    #     x=self.x
    #     self.clear_barbarians(grid)
    #     self.x=x+1
    #     self.render_barbarians(grid)
        
    # def move_left(self,grid):
    #     y=self.y
    #     self.clear_barbarians(grid)
    #     self.y=y-1
    #     self.render_barbarians(grid)
        
    # def move_right(self,grid):
    #     y=self.y
    #     self.clear_king(grid)
    #     self.y=y+1
    #     self.render_king(grid)
    def move_to(self,x,y,grid):
        self.clear_barbarians(grid)
        self.y=y
        self.x=x
        self.render_barbarians(grid)
    def barbarian_motion(self,cannon_list,hut_list,th,grid):
        x=self.x
        y=self.y
        # barbarian goes to the closest structure 
        mindist=1000
        entity="None"
        t_index=0
        for cannon in cannon_list:
            if(math.sqrt((cannon.get_x()-x)**2 + (cannon.get_y()-y)**2))<mindist:
                mindist=math.sqrt((cannon.get_x()-x)**2 +(cannon.get_y()-y)**2)
                entity="cannon"
                t_index=cannon_list.index(cannon)
        for hut in hut_list:
            if(math.sqrt((hut.get_x()-x)**2 +(hut.get_y()-y)**2))<mindist:
                mindist=math.sqrt((hut.get_x()-x)**2 + (hut.get_y()-y)**2)
                entity="hut"
                t_index=hut_list.index(hut)
        if(math.sqrt((th.get_x()-x)**2 + (th.get_y()-y)**2))<mindist and th.get_strength()>0:
            mindist=math.sqrt((th.get_x()-x)**2 + (th.get_y()-y)**2)
            entity="th"
        #move in the direction of the entity
        targetx=0
        targety=0
        if entity=="th":
            targetx=th.get_x()
            targety=th.get_y()
        elif entity=="cannon":
            targetx=cannon_list[t_index].get_x()
            targety=cannon_list[t_index].get_y()
        elif entity=="hut":
            targetx=hut_list[t_index].get_x()
            targety=hut_list[t_index].get_y()
        # self.move_to(self.get_x(), self.get_y()+1,grid) works
        flx=0
        fly=0            
        if(self.x>targetx-1) and (self.y==targety-1):
            flx=-1
        elif(self.x<targetx-1) and (self.y==targety-1):
            flx=1
        elif(self.x==targetx-1) and (self.y>targety-1):
            fly=-1
        elif(self.x==targetx-1) and (self.y<targety-1):
            fly=1
        elif(self.x>targetx-1) and (self.y>targety-1):
            flx=-1   
            fly=-1
        elif(self.x<targetx-1) and (self.y<targety-1):
            flx=1
            fly=1
        elif(self.x<targetx-1) and (self.y>targety-1):
            flx=1
            fly=-1
        elif(self.x>targetx-1) and (self.y<targety-1):
            flx=-1
            fly=1
        self.move_to(self.x+flx,self.y+fly,grid)
        if (self.x==targetx-1) and (self.y==targety-1):
            if entity == "hut":
                hut=hut_list[t_index]
                hut.damage_taken()
                hut.render_hut(grid)
                #print("Barbarians strength is {} and huts is {}".format(self.strength, hut.strength))
                if(hut.get_strength()<=0):
                    hut.destroy_hut(grid)
                    hut_list.remove(hut)
            elif entity == "cannon":
                cannon=cannon_list[t_index]
                cannon.damage_taken()
                cannon.render_cannon(grid)
                #print("Barbarians strength is {} and cannon is {}".format(self.strength, cannon.strength))
                if(cannon.get_strength()<=0):
                    cannon.destroy_cannon(grid)
                    cannon_list.remove(cannon)
            elif entity == "th":
                th.damage_taken()
                th.render_th(grid)
                #print("Barbarians strength is {} and th is {}".format(self.strength, th.strength))
                if(th.get_strength()<=0):
                    th.destroy_th(grid)
                    th_destroyed=True
            
        
            
        
        
    # def deal_damage(self,grid,list1,list2,th):
    # todo
        

display = Board(30,30) #width=30, height=30
display.get_board()
#display.print_board()

#cannons rendered
cannon_list=[Cannon(10,10), Cannon(20,20), Cannon(20,10), Cannon(10,20)]
for cannon in cannon_list:
    cannon.render_cannon(display.get_board())

#rendering Huts
hut_list=[Huts(15,10), Huts(15,20), Huts(10,15), Huts(20,15),Huts(3,5)]
for hut in hut_list:
    hut.render_hut(display.get_board())

#rendering th   
th=Townhall(14,14)
th.render_th(display.get_board())

#rendering barbarian King
king=King(3,3)
king.render_king(display.get_board())

total_max_barbarians=30
barbarian_list=[] #(2,1) is p and (2,28) is q and (27,1)

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
 
my_file = open("list.txt", "r")
content = my_file.read()
character_list=[]
timestamp_list=[]
# 1st word of each line to be inserted to character_list and the 2nd word of each line to be inserted to timestamp_list
for line in content.splitlines():
    if len(line.split())==1:
        character_list.append(" ")
        timestamp_list.append(line.split()[0])
    else:
        character_list.append(line.split()[0])
        timestamp_list.append(line.split()[1])
ctr=0
while True:
    
    #king.areal_damage(display.get_board(),cannon_list,hut_list,th)
    #king.deal_damage(display.get_board(),cannon_list,hut_list,th)
    ch=character_list[ctr]
    if ctr==0:
        time.sleep(float(timestamp_list[ctr]))
    else:
        time.sleep(float(timestamp_list[ctr])-float(timestamp_list[ctr-1]))
    ctr+=1
    #print("Health of king is {}".format(king.get_strength()))
    king_ratio=(king.get_strength()/16)*100
    print("King Health Bar {}%".format(king_ratio))
    for i in range(0,int(king_ratio)):
        print("█",end="")
    print("\n")
    print("Total Available Barbarians are {}".format(total_max_barbarians))
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
        barb=Barbarians(2,28)
        barb.render_barbarians(display.get_board())
        barbarian_list.append(barb)
        total_max_barbarians-=1
    if ch=='r':
        barb=Barbarians(27,1)
        barb.render_barbarians(display.get_board())
        barbarian_list.append(barb)
        total_max_barbarians-=1
    for cannon in cannon_list:
        cannon.cannon_attack(barbarian_list,king,display.get_board())
    for barbarian in barbarian_list:
        barbarian.barbarian_motion(cannon_list,hut_list,th,display.get_board())
    display.print_board()
    if(verify_win()==True):
        break


