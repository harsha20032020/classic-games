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

class Barbarians:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=1
        self.height=1
        self.strength=4 #kbarbarians takes 4 hits to get killed
        self.damage=1   #barbarian king deals 1 damage
        self.max_strength=4
        
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
                ratio = self.strength/self.max_strength
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
    def damage_taken(self,damage):
        self.strength-=damage
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
    def barbarian_motion(self,cannon_list,hut_list,wizard_list,th,grid):
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
        for wizard in wizard_list:
            if(math.sqrt((wizard.get_x()-x)**2 +(wizard.get_y()-y)**2))<mindist:
                mindist=math.sqrt((wizard.get_x()-x)**2 + (wizard.get_y()-y)**2)
                entity="wizard"
                t_index=wizard_list.index(wizard)
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
        elif entity=="wizard":
            targetx=wizard_list[t_index].get_x()
            targety=wizard_list[t_index].get_y()
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
                hut.damage_taken(self.damage)
                hut.render_hut(grid)
                
                #print("Barbarians strength is {} and huts is {}".format(self.strength, hut.strength))
                time.sleep(1)
                if(hut.get_strength()<=0):
                    hut.destroy_hut(grid)
                    hut_list.remove(hut)
            elif entity == "cannon":
                cannon=cannon_list[t_index]
                cannon.damage_taken(self.damage)
                cannon.render_cannon(grid)
                #print("Barbarians strength is {} and cannon is {}".format(self.strength, cannon.strength))
                time.sleep(1)
                if(cannon.get_strength()<=0):
                    cannon.destroy_cannon(grid)
                    cannon_list.remove(cannon)
            elif entity == "th":
                th.damage_taken(self.damage)
                th.render_th(grid)
                #print("Barbarians strength is {} and th is {}".format(self.strength, th.strength))
                time.sleep(1)
                if(th.get_strength()<=0):
                    th.destroy_th(grid)
                    th_destroyed=True
            elif entity == "wizard":
                wizard=wizard_list[t_index]
                wizard.damage_taken(self.damage)
                wizard.render_wizard_tower(grid)
                #print("Barbarians strength is {} and wizard is {}".format(self.strength, wizard.strength))
                time.sleep(1)
                if(wizard.get_strength()<=0):
                    wizard.destroy_wizard_tower(grid)
                    wizard_list.remove(wizard)
        
            
        
        
    # def deal_damage(self,grid,list1,list2,th):
    # todo
        


class Archers:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=1
        self.height=1
        self.strength=2 #kArchers takes 2 hits to get killed
        self.damage=0.5   #Archer king deals 0.5 damage
        self.max_strength=2
        self.range=3
        
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
    def render_archers(self,grid):
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                x=self.x
                y=self.y
                ratio = self.strength/self.max_strength
                if ratio> 0.5:
                    grid[i][j]=Fore.GREEN+"A"+Style.RESET_ALL
                elif ratio> 0.25:
                    grid[i][j]=Fore.YELLOW+"A"+Style.RESET_ALL
                else:
                    grid[i][j]=Fore.RED+"A"+Style.RESET_ALL
        return grid
    def delete_archers(self,grid):
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                grid[i][j]=" "
        del self
    def clear_archers(self,grid):
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                grid[i][j]=" "
    def damage_taken(self,damage):
        self.strength-=damage
    def move_to(self,x,y,grid):
        self.clear_archers(grid)
        self.y=y
        self.x=x
        self.render_archers(grid)
    def archer_motion(self,cannon_list,hut_list,th,grid):
        x=self.x
        y=self.y
        # archer goes to the closest structure 
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
        if(self.x>targetx-self.range) and (self.y==targety-self.range):
            flx=-1
        elif(self.x<targetx-self.range) and (self.y==targety-self.range):
            flx=1
        elif(self.x==targetx-self.range) and (self.y>targety-self.range):
            fly=-1
        elif(self.x==targetx-self.range) and (self.y<targety-self.range):
            fly=1
        elif(self.x>targetx-self.range) and (self.y>targety-self.range):
            flx=-1   
            fly=-1
        elif(self.x<targetx-self.range) and (self.y<targety-self.range):
            flx=1
            fly=1
        elif(self.x<targetx-self.range) and (self.y>targety-self.range):
            flx=1
            fly=-1
        elif(self.x>targetx-self.range) and (self.y<targety-self.range):
            flx=-1
            fly=1
        self.move_to(self.x+flx,self.y+fly,grid)
        if (self.x-targetx<=self.range) and (self.y-targety<=self.range):
            if entity == "hut":
                hut=hut_list[t_index]
                hut.damage_taken(self.damage)
                hut.render_hut(grid)
                #print("archers strength is {} and huts is {}".format(self.strength, hut.strength))
                if(hut.get_strength()<=0):
                    hut.destroy_hut(grid)
                    hut_list.remove(hut)
            elif entity == "cannon":
                cannon=cannon_list[t_index]
                cannon.damage_taken(self.damage)
                cannon.render_cannon(grid)
                #print("archers strength is {} and cannon is {}".format(self.strength, cannon.strength))
                if(cannon.get_strength()<=0):
                    cannon.destroy_cannon(grid)
                    cannon_list.remove(cannon)
            elif entity == "th":
                th.damage_taken(self.damage)
                th.render_th(grid)
                #print("archers strength is {} and th is {}".format(self.strength, th.strength))
                if(th.get_strength()<=0):
                    th.destroy_th(grid)
                    th_destroyed=True
          