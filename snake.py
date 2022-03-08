#Snake Tutorial Python
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


def redrawWindow(surface):
    win.fill((0,0,0))
    drawGrid(surface)
    pygame.display.update()
    

def main():
    width = 500
    height = 500
    rows=20
    win=pygame.display.set_mode((width,height))
    s=snake((255,0,0),(10,10)) # 255,0,0 is the color of the snake and (10,10) is the starting position
    flag=True
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        redrawWindow(win)
        
    pass