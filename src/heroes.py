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
                elif i==self.rows-2 and j==1:
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
          


class King:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=2
        self.height=2
        self.strength=16 #king takes 8 hits to get killed
        self.max_strength=16
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
                ratio = self.strength/self.max_strength
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
    def damage_taken(self,damage):
        self.strength-=damage
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
                cannon.damage_taken(self.damage)
                cannon.render_cannon(grid)
                if(cannon.get_strength()<=0):
                    cannon.destroy_cannon(grid)
                    list1.remove(cannon)
        for hut in list2:
            if(hut.get_x()==x and hut.get_y()==y+2):
                hut.damage_taken(self.damage)
                #print("the strength of hut is {}".format(hut.get_strength()))
                hut.render_hut(grid)
                if(hut.get_strength()<=0):
                    hut.destroy_hut(grid)
                    list2.remove(hut)
        if(th.get_x()==x and th.get_y()==y+2):
            th.damage_taken(self.damage)
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
                cannon.damage_taken(self.damage)
                #print("the cannon at position {} {} has strength {}".format(cannon.get_x(),cannon.get_y(),cannon.get_strength()))
                cannon.render_cannon(grid)
                if(cannon.get_strength()<=0):
                    cannon.destroy_cannon(grid)
                    list1.remove(cannon)
        for hut in list2:
            dist=math.sqrt((hut.get_x() - x)**2 + (hut.get_y() - y)**2)
            if(dist<=5):
                hut.damage_taken(self.damage)
                #print("the strength of hut is {}".format(hut.get_strength()))
                hut.render_hut(grid)
                if(hut.get_strength()<=0):
                    hut.destroy_hut(grid)
                    list2.remove(hut)
        dist=math.sqrt((th.get_x() - x)**2 + (th.get_y() - y)**2)
        if(dist<=5):
            th.damage_taken(self.damage)
            #print("the strength of th is {}".format(th.get_strength()))
            th.render_th(grid)
            if(th.get_strength()<=0):
                th.destroy_th(grid)