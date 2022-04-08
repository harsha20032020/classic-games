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

class Cannon:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=2
        self.height=2
        self.strength=8 #king takes 4 hits to destroy cannon
        self.max_health=8
        self.range=2 #cannon can shoot 6 spaces
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
                ratio = self.strength/self.max_health
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
    def damage_taken(self,damage):
        self.strength-=damage
    
    
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
            king.damage_taken(self.damage)
            king.render_king(grid)
            if king.get_strength()<=0:
                king.delete_king(grid)
        elif(minval<=self.range):
            affected_barbarian=barblist[minindex]
            affected_barbarian.damage_taken(self.damage)
            affected_barbarian.render_barbarians(grid)
            if affected_barbarian.get_strength()<=0:
                affected_barbarian.delete_barbarians(grid)
                barblist.remove(affected_barbarian)
            
        
class Wizard_tower:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=2
        self.height=2
        self.strength=8 #king takes 4 hits to destroy Wizard_tower
        self.max_health=8
        self.range=2 #Wizard_tower can shoot 6 spaces
        self.damage=1 #Wizard_tower deals 1 damage
        
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_x(self,x):
        self.x=x
    def set_y(self,y):
        self.y=y
    def render_wizard_tower(self,grid):
        if(self.x=="NONE" and self.y=="NONE"):
            return
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                #grid[i][j]="4"
                ratio = self.strength/self.max_health
                if ratio> 0.5:
                    grid[i][j]=Fore.GREEN+"W"+Style.RESET_ALL
                elif ratio> 0.25:
                    grid[i][j]=Fore.YELLOW+"W"+Style.RESET_ALL
                else:
                    grid[i][j]=Fore.RED+"W"+Style.RESET_ALL
        
        return grid
    def destroy_wizard_tower(self,grid):
        x=self.x
        y=self.y
        for i in range(x,x+self.width):
            for j in range(y,y+self.height):
                grid[i][j]=" "
        del self
    def get_strength(self):
        return self.strength
    def damage_taken(self,damage):
        self.strength-=damage
    
    
    # need to do barbarian and king interactions
    def wizard_tower_attack(self,barblist,baloonlist,king,grid):
        #each cannon attacks the closest barbarian in barblist or if the king is closer than the barbarians, it attacks the king
        #if there are no barbarians, it attacks the king
        #if there are no barbarians and no king, it attacks nothing
        minval=1000
        minindex=0
        ttype=""
        for barbarian in barblist:
            distance=math.sqrt((barbarian.get_x()-self.x)**2+(barbarian.get_y()-self.y)**2)
            if distance<minval:
                minval=distance
                minindex=barblist.index(barbarian)
                ttype="barbarian"
        for baloon in baloonlist:
            distance=math.sqrt((baloon.get_x()-self.x)**2+(baloon.get_y()-self.y)**2)
            if distance<minval:
                minval=distance
                minindex=baloonlist.index(baloon)
                ttype="baloon"
        dist=math.sqrt((king.get_x()-self.x)**2 + (king.get_y()-self.y)**2)
        #print("min barb distance is {} and distance of king is {}".format(minval, dist))
        if(dist<minval and dist<=self.range):
            king.damage_taken(self.damage)
            king.render_king(grid)
            if king.get_strength()<=0:
                king.delete_king(grid)
        elif(minval<=self.range):
            # affected_barbarian=barblist[minindex]
            # affected_barbarian.damage_taken(self.damage)
            # affected_barbarian.render_barbarians(grid)
            # if affected_barbarian.get_strength()<=0:
            #     affected_barbarian.delete_barbarians(grid)
            #     barblist.remove(affected_barbarian)
            if ttype=="barbarian":
                affected_barbarian=barblist[minindex]
                afx=affected_barbarian.get_x()
                afy=affected_barbarian.get_y()
                affected_barbarian.damage_taken(self.damage)
                if affected_barbarian.get_strength()<=0:
                    affected_barbarian.delete_barbarians(grid)
                    barblist.remove(affected_barbarian)
                for barb in barblist:
                    if(math.sqrt((barb.get_x()-afx)**2+(barb.get_y()-afy)**2))<=3:
                        barb.damage_taken(self.damage)
                        if barb.get_strength()<=0:
                            barb.delete_barbarians(grid)
                            barblist.remove(barb)
                for baloon in baloonlist:
                    if(math.sqrt((baloon.get_x()-afx)**2+(baloon.get_y()-afy)**2))<=3:
                        baloon.damage_taken(self.damage)
                        if baloon.get_strength()<=0:
                            baloon.delete_baloon(grid)
                            baloonlist.remove(baloon)
            elif ttype=="baloon":
                affected_baloon=baloonlist[minindex]
                afx=affected_baloon.get_x()
                afy=affected_baloon.get_y()
                affected_baloon.damage_taken(self.damage)
                if affected_baloon.get_strength()<=0:
                    affected_baloon.delete_baloon(grid)
                    baloonlist.remove(affected_baloon)
                for barb in barblist:
                    if(math.sqrt((barb.get_x()-afx)**2+(barb.get_y()-afy)**2))<=3:
                        barb.damage_taken(self.damage)
                        if barb.get_strength()<=0:
                            barb.delete_barbarians(grid)
                            barblist.remove(barb)
                for baloon in baloonlist:
                    if(math.sqrt((baloon.get_x()-afx)**2+(baloon.get_y()-afy)**2))<=3:
                        baloon.damage_taken(self.damage)
                        if baloon.get_strength()<=0:
                            baloon.delete_baloon(grid)
                            baloonlist.remove(baloon)
                
                
            
        
                        
                        
class Huts:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=1
        self.height=1
        self.strength=4 #king takes 4 hits to destroy cannon
        self.max_health=4
        
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
                ratio = self.strength/self.max_health
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
    def damage_taken(self,damage):
        self.strength-=damage

class Townhall:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=4
        self.height=3
        self.strength=16 #king takes 6 hits to destroy th
        self.max_strength=16
        
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
                ratio = self.strength/self.max_strength
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
    def damage_taken(self,damage):
        self.strength-=damage
