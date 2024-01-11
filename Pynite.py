import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0]))+"\\dependencies")
import pygame
import time
import random
import math
import pyperclip
from linecache import getline as linecache_getline
from linecache import getlines as linecache_getlines
import json
import shutil
import inspect
import ctypes
import numpy as np
import colorsys
import subprocess
import platform
import win32con
import win32gui

import pygame.draw
from pygame import gfxdraw
from mutagen.mp3 import MP3


# Initializing default font
defaultFont = "Arial"
if os.path.exists("fonts/Roboto-Medium.ttf"):
    defaultFont = "fonts/Roboto-Medium.ttf"

pygame.init()

pygame.mixer.init()

tile_group = pygame.sprite.Group()
collision_group = pygame.sprite.Group()

_textBoxList = []

_windowObject = None

_collidableCirclesList = []

_drawnObjects = []

_changingCursor = None

_allObjects = []

_clickableObjects = []
_clickedObjects = []

_filePath = os.path.dirname(os.path.abspath(__file__))

_disablePropertiesTempList = []

# Class for initializing window
class window_init():
    def __init__(self, **kwargs):
        global _windowObject
        pyniteLogoPath = "assets/logo/logo.png"
        pyniteLogo = None
        if os.path.isfile(pyniteLogoPath):
            pyniteLogo = pyniteLogoPath
        self.run: bool = True
        self.screen_width: int = kwargs['screen_width']
        self.screen_height: int = kwargs['screen_height']
        self._title: str = kwargs.get("title", "Window")
        self._title: str = kwargs.get("_title", self._title)
        self.background: tuple = kwargs.get("background", (0,0,0))
        self.FPS: int = kwargs.get("FPS", 60)
        self.icon: str = kwargs.get("icon", None)  # .png format only
        self.changeCursor: bool = False
        self.collidingWith = None
        self._collidingObject = None
        if self.icon != None:
            pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.previous_time = time.time()
        self.delta = 0
        self.resizable = kwargs.get("resizable", False)
        self._customTitleBar = kwargs.get("customTitleBar", False)
        self._customTitleBar = kwargs.get("_customTitleBar", self._customTitleBar)
        self._titleBarColor = kwargs.get("titleBarColor", (12,12,12))
        self._titleBarColor = kwargs.get("_titleBarColor", self._titleBarColor)

        self._closeButtonHoverColor = kwargs.get("closeButtonHoverColor", (225,0,0))
        self._closeButtonHoverColor = kwargs.get("_closeButtonHoverColor", self._closeButtonHoverColor)
        self._maximizeButtonHoverColor = kwargs.get("maximizeButtonHoverColor", (35,35,35))
        self._maximizeButtonHoverColor = kwargs.get("_maximizeButtonHoverColor", self._maximizeButtonHoverColor)
        self._minimizeButtonHoverColor = kwargs.get("minimizeButtonHoverColor", (35,35,35))
        self._minimizeButtonHoverColor = kwargs.get("_minimizeButtonHoverColor", self._minimizeButtonHoverColor)

        self.showWindowTitle = kwargs.get("showWindowTitle", True)
        self.showWindowIcon = kwargs.get("showWindowIcon", False)

        self.scrolling_up: bool = False
        self.scrolling_down: bool = False

        self._ENTERED_MAIN_LOOP = False

        self._offsetY = 0
        if self.customTitleBar:
            self._offsetY = 30

        if not(self.customTitleBar):
            if self.resizable:
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
            else:
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.NOFRAME)

        pygame.display.set_caption(self._title)

        if pyniteLogo != None:
            logoIcon = pygame.image.load(pyniteLogo)
            pygame.display.set_icon(logoIcon)

        _windowObject = self

        self._dragingWindow = False
        self._pos = (0,0)
        
        self.closeWindowImage = None
        self.maximizeWindowImage = None
        self.minimizeWindowImage = None

        self.titleBar = Rectangle(width=self.screen_width, height=30, background=self._titleBarColor, x=0, y=0)
        self.closeWindowButton = Button(text="", x=-1000, y=0, height=2, width=34, fontSize=13, background=self._titleBarColor, hoverBackground=self.closeButtonHoverColor, activeBackground=self._closeButtonHoverColor)
        self.closeWindowButton.x = self.screen_width - self.closeWindowButton.rect.width
        if os.path.exists("PyniteAssets/closewindowimage.png"):
            self.closeWindowImage = Image(image="PyniteAssets/closewindowimage.png", x=self.closeWindowButton.x+16, y=self.closeWindowButton.y+10)
        self.maximizeWindowButton = Button(text="", x=-1000, y=0, height=2, width=34, fontSize=13, background=self._titleBarColor, hoverBackground=self.maximizeButtonHoverColor, activeBackground=self._maximizeButtonHoverColor)
        self.maximizeWindowButton.x = self.closeWindowButton.x - self.maximizeWindowButton.rect.width
        if os.path.exists("PyniteAssets/maximizewindowimage.png"):
            self.maximizeWindowImage = Image(image="PyniteAssets/maximizewindowimage.png", x=self.maximizeWindowButton.x+16, y=self.maximizeWindowButton.y+10)
        self.minimizeWindowButton = Button(text="", x=-1000, y=0, height=2, width=34, fontSize=13, background=self._titleBarColor, hoverBackground=self.minimizeButtonHoverColor, activeBackground=self._minimizeButtonHoverColor)
        if self.resizable:
            self.minimizeWindowButton.x = self.maximizeWindowButton.x - self.minimizeWindowButton.rect.width
        else:
            self.minimizeWindowButton.x = self.closeWindowButton.x - self.minimizeWindowButton.rect.width
        if os.path.exists("PyniteAssets/minimizewindowimage.png"):
            self.minimizeWindowImage = Image(image="PyniteAssets/minimizewindowimage.png", x=self.minimizeWindowButton.x+16, y=self.minimizeWindowButton.y+11)
            self.minimizeWindowImage.x = self.minimizeWindowButton.x+16
        self.windowTitleLabel = Label(text=self.title, x=10,y=8, fontSize=13)

        if self.resizable:
            self.titleBar.width -= (self.closeWindowButton.rect.width+self.maximizeWindowButton.rect.width+self.minimizeWindowButton.rect.width)
        else:
            self.titleBar.width -= (self.closeWindowButton.rect.width+self.minimizeWindowButton.rect.width)

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value: str):
        self._title = value
        pygame.display.set_caption(self._title)

    @property
    def customTitleBar(self):
        return self._customTitleBar
    
    @customTitleBar.setter
    def customTitleBar(self, value: bool):
        self._customTitleBar = value
    
    @property
    def titleBarColor(self):
        return self._titleBarColor
    
    @titleBarColor.setter
    def titleBarColor(self, value: tuple):
        self._titleBarColor = value
        self.titleBar.background = value
        self.closeWindowButton.background = value
        self.minimizeWindowButton.background = value
        self.maximizeWindowButton.background = value

    @property
    def closeButtonHoverColor(self):
        return self._closeButtonHoverColor

    @closeButtonHoverColor.setter
    def closeButtonHoverColor(self, value: tuple):
        self._closeButtonHoverColor = value
        self.closeWindowButton.hoverBackground = value

    @property
    def maximizeButtonHoverColor(self):
        return self._maximizeButtonHoverColor

    @maximizeButtonHoverColor.setter
    def maximizeButtonHoverColor(self, value: tuple):
        self._maximizeButtonHoverColor = value
        self.maximizeeWindowButton.hoverBackground = value

    @property
    def minimizeButtonHoverColor(self):
        return self._minimizeButtonHoverColor

    @minimizeButtonHoverColor.setter
    def minimizeButtonHoverColor(self, value: tuple):
        self._minimizeButtonHoverColor = value
        self.minimizeeWindowButton.hoverBackground = value

    # Quick function for drawing text on to the screen
    def draw_text(self, **kwargs):
        global defaultFont
        font = pygame.font.SysFont(defaultFont, kwargs['fontSize'])
        if kwargs.__contains__('fontName'):
            font = pygame.font.SysFont(kwargs.get("fontName", "Arial"), kwargs.get("fontSize", 16))

        img = font.render(kwargs.get("text", "text"), True, kwargs.get("textColor", (255,255,255)))
        self.screen.blit(img, (kwargs.get("x", 0), kwargs.get("y", 0)))

    # Displaying current FPS in the top left corner
    def display_fps(self, **kwargs):
        fontSize = kwargs.get("fontSize", 20)
        textColor = kwargs.get("textColor", (255,255,255))
        x = kwargs.get("x", 5)
        y = kwargs.get("y", 5)
        self.debug(str(round(self.clock.get_fps())), fontSize=fontSize, textColor=textColor, x=x, y=y)

    # Function for changing size of the window dynamically
    def change_size(self, width, height):
        width = width
        height = height
        self.screen_width = width
        self.screen_height = height

        if not(self.customTitleBar):
            if self.resizable:
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
            else:
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.NOFRAME)

            self.closeWindowButton.x = self.screen_width - self.closeWindowButton.rect.width
            if self.closeWindowImage != None:
                self.closeWindowImage.x = self.closeWindowButton.x+16
            self.maximizeWindowButton.x = self.closeWindowButton.x - self.maximizeWindowButton.rect.width
            if self.maximizeWindowImage != None:
                self.maximizeWindowImage.x = self.maximizeWindowButton.x+16
            
            if self.resizable:
                self.minimizeWindowButton.x = self.maximizeWindowButton.x - self.minimizeWindowButton.rect.width
            else:
                self.minimizeWindowButton.x = self.closeWindowButton.x - self.minimizeWindowButton.rect.width

            if self.minimizeWindowImage != None:
                self.minimizeWindowImage.x = self.minimizeWindowButton.x+16

            
            self.titleBar.width = width
            if self.resizable:
                self.titleBar.width -= (self.closeWindowButton.rect.width+self.maximizeWindowButton.rect.width+self.minimizeWindowButton.rect.width)
            else:
                self.titleBar.width -= (self.closeWindowButton.rect.width+self.minimizeWindowButton.rect.width)

        # Positioning window in the middle of the screen
        if os.name == 'nt': # Windows
            display_size = get_display_size(ignoreTaskBar=True)
            window_pos_x = (display_size[0] - width) // 2
            window_pos_y = (display_size[1] - height) // 2
            ctypes.windll.user32.SetWindowPos(pygame.display.get_wm_info()["window"], 0, window_pos_x, window_pos_y, 0, 0, 0x0001)


    # Setting icon of the window
    def set_icon(self, image):
        self.icon = pygame.image.load(image)
        pygame.display.set_icon(self.icon)

    # Function for displaying text in the top left corner
    def debug(self, text, **kwargs):
        fontSize = kwargs.get("fontSize", 20)
        textColor = kwargs.get("textColor", (255,255,255))
        x = kwargs.get("x", 5)
        y = kwargs.get("y", 5)
        self.font = pygame.font.SysFont('Arial', fontSize)
        self.img = self.font.render(text, True, textColor)
        self.screen.blit(self.img, (x, y))

    # Function for loading tile map from .txt format in 2 dimensional list format -- (numbers only e.g '0')
    def loadTileMap(self, path):
        f = open(path, "r")
        data = f.read()
        f.close()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(list(row))

        return game_map

    # Function for loading tile map from .txt format in 2 dimensional list format -- (text only e.g 'air')
    def loadTileMap2(self, path):
        data_file = open(path)
        game_map = data_file.readlines()
        for i in range(len(game_map)):
            game_map[i] = list(map(str, game_map[i].split()))

        return game_map

    def _move_window_to_mouse_position(self, window_handle, pos):
        x, y = win32gui.GetCursorPos()
        x -= pos[0]
        y -= pos[1]
        if y < -(self.titleBar.height // 2):
            y = -(self.titleBar.height // 2)
        win32gui.SetWindowPos(window_handle, 0, x, y, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)
        pygame.mouse.set_pos(pos)

    # Main loop which handles all the events
    def main_loop(self, callback, onClose=None, drawOnToTitleBar=None):
        global _textBoxList, _allObjects, _changingCursor, _allObjects
                
        while self.run:
            pos = pygame.mouse.get_pos()
            self.screen.fill(self.background)
            self.delta = time.time() - self.previous_time
            self.previous_time = time.time()

            self.scrolling_up = False
            self.scrolling_down = False

            # Changing cursor -=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-#
            if _changingCursor == None:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            else:
                pygame.mouse.set_cursor(_changingCursor)
            _changingCursor = None
            #-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

            # Looping through every clickable object and then setting _hoveringAction
            # variable to True to object with biggest index in the case of overlaping
            z_index_order = []
            for clickedObject in _clickedObjects:
                if clickedObject.z_index != None:
                    clickedObject._hoveringAction = False
                    z_index_order.append(clickedObject.z_index)
            z_index_order.sort()
            for clickedObject in _clickedObjects:
                if clickedObject.z_index != None:
                    if clickedObject.z_index == max(z_index_order):
                        clickedObject._hoveringAction = True
                        z_index_order.clear()
                        _clickedObjects.clear()
                        break
            #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
                    
            for event in pygame.event.get():
                # Closing window event
                for textbox in _textBoxList:
                    textbox._update(event)
                if event.type == pygame.QUIT:
                    if onClose != None:
                        onClose()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.scrolling_down = False
                        self.scrolling_up = True
                    elif event.button == 5:
                        self.scrolling_up = False
                        self.scrolling_down = True

            callback()

            if self.customTitleBar:
                self.titleBar.draw()

                if self.closeWindowButton.draw():
                    sys.exit()

                if self.resizable:
                    if self.maximizeWindowButton.draw():
                        pass
                    if self.maximizeWindowImage != None:
                        self.maximizeWindowImage.draw()
                    
                if self.minimizeWindowButton.draw():
                    pygame.display.iconify()

                if self.closeWindowImage != None:
                    self.closeWindowImage.draw()
                if self.minimizeWindowImage != None:
                    self.minimizeWindowImage.draw()

                if self.showWindowTitle:
                    self.windowTitleLabel.draw()

                if self.titleBar.rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0] == 1 and not(self._dragingWindow):
                        self._pos = pygame.mouse.get_pos()
                        self._dragingWindow = True
                
                if self._dragingWindow:
                    window_handle = win32gui.FindWindow(None, self.title)
                    if window_handle:
                        self._move_window_to_mouse_position(window_handle, self._pos)
                
                if pygame.mouse.get_pressed()[0] == 0 and self._dragingWindow:
                    self._dragingWindow = False

            if drawOnToTitleBar != None:
                if callable(drawOnToTitleBar):
                    drawOnToTitleBar()

            self.clock.tick(self.FPS)
            pygame.display.update()

            
class Button():
    def __init__(self, **kwargs):
        global defaultFont, _allObjects, _windowObject, _clickableObjects
        self._fontName: str = kwargs.get("fontName", defaultFont)
        self._fontName: str = kwargs.get("_fontName", self._fontName)
        self._fontSize: int = kwargs.get("fontSize", 22)
        self._fontSize: int = kwargs.get("_fontSize", self._fontSize)
        self._changeCursor: bool = kwargs.get("changeCursor", True)
        self._changeCursor: bool = kwargs.get("_changeCursor", self._changeCursor)
        self._text: str = kwargs.get("text", "button")
        self._text: str = kwargs.get("_text", self._text)
        self.textColor: tuple = kwargs.get("textColor", (235, 235, 235))
        self.hoverTextColor: tuple = kwargs.get("hoverTextColor", self.textColor)
        self.activeTextColor: tuple = kwargs.get("activeTextColor", self.hoverTextColor)
        self.displayColor: tuple = kwargs.get("displayColor", (235, 235, 235))
        self.background0: tuple = kwargs.get("background", (50, 50, 50))
        self.background: tuple = self.background0
        self.bottomColor0: tuple = kwargs.get("bottomColor", (100,100,100))
        self.bottomColor: tuple = self.bottomColor0
        self.hoverBackground: tuple = kwargs.get("hoverBackground", self.background0)
        self.activeBackground: tuple = kwargs.get("activeBackground", self.hoverBackground)
        self.hoverColorBottom: tuple = kwargs.get("hoverColorBottom", self.bottomColor)
        self.outlineColor: tuple = kwargs.get("outlineColor", (180,180,180))
        self.outlineColor0: tuple = self.outlineColor
        self.hoverOutlineColor: tuple = kwargs.get("hoverOutlineColor", (225,225,225))
        self.activeOutlineColor: tuple = kwargs.get("activeOutlineColor", (255,255,255))
        self._outlineWidth: int = kwargs.get("outlineWidth", 0)
        self._outlineWidth: int = kwargs.get("_outlineWidth", self._outlineWidth)
        self._autoResizing = kwargs.get("autoResizing", True)
        self._autoResizing = kwargs.get("_autoResizing", self._autoResizing)
        self._width: int = kwargs.get("width", 14)
        self._width: int = kwargs.get("_width", self._width)
        self._height: int = kwargs.get("height", 2)
        self._height: int = kwargs.get("_height", self._height)
        self.textPosition: str = kwargs.get("textPosition", "center")
        self.borderRadius: int = kwargs.get("borderRadius", 0)
        self.bordersToHide: list = kwargs.get("bordersToHide", [])
        self.active: bool = kwargs.get("active", True)
        self.clickAnimation: bool = kwargs.get("clickAnimation", False)
        self.name: str = kwargs.get("name", None)
        self.z_index: int = kwargs.get("z_index", None)
        self._hide = kwargs.get("hide", False)
        self._hide = kwargs.get("_hide", self._hide)
        self.disable = kwargs.get("disable", False)

        self.clickedOutside = False
        self._clickedButton = False
        self.clicked = False

        self._hoveringAction = False

        self.dropDownMenu = kwargs.get("dropDownMenu", None)

        self.clickEvent = None
        self.hoverEvent = None

        self._x = kwargs.get("x", 0)
        self._y = kwargs.get("y", 0)
        self._x = kwargs.get("_x", self._x)
        self._y = kwargs.get("_y", self._y)

        self.textOffsetX = kwargs.get("textOffsetX", 0)
        self.textOffsetY = kwargs.get("textOffsetY", 0)

        if self.fontName[-4:] == ".ttf":
            self.font = pygame.font.Font(self.fontName, self._fontSize)
        else:
            self.font = pygame.font.SysFont(self.fontName, self._fontSize)

        self.img = self.font.render(self._text, True, self.displayColor)
        self.imageRect = self.img.get_rect()
        
        self.buttonrect = pygame.Rect(self._x, self._y, (self.imageRect.width+12 + self.width), self.imageRect.height + 12 + self.height)
        if not(self._autoResizing):
            self.buttonrect.width, self.buttonrect.height = self._width, self._height
        
        self.outlinerect = pygame.Rect(self.buttonrect.x - self._outlineWidth, self.buttonrect.y - self._outlineWidth, self.buttonrect.width + (self._outlineWidth*2), self.buttonrect.height + (self._outlineWidth*2))

        if self.buttonrect.height - self.borderRadius*2 < 2:
            self.borderRadius = self.buttonrect.height // 2 - 1

        self.rect = pygame.Rect(self._x-self.outlineWidth, self._y-self.outlineWidth, self.buttonrect.width + (self._outlineWidth*2), self.buttonrect.height + (self._outlineWidth*2))

        _allObjects.append(self)
        _clickableObjects.append(self)

    @property
    def outlineWidth(self):
        return self._outlineWidth
    
    @outlineWidth.setter
    def outlineWidth(self, value):
        self._outlineWidth = value
        self.outlinerect.x = self.buttonrect.x - self._outlineWidth
        self.outlinerect.y = self.buttonrect.y - self._outlineWidth
        self.outlinerect.width, self.outlinerect.height = self.buttonrect.width + (self._outlineWidth*2), self.buttonrect.height + (self._outlineWidth*2)
        self.rect = pygame.Rect(self._x-self.outlineWidth, self._y-self.outlineWidth, self.buttonrect.width + (self._outlineWidth*2), self.buttonrect.height + (self._outlineWidth*2))

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
        self.img = self.font.render(self._text, True, self.displayColor)
        self.imageRect = self.img.get_rect()
        self.buttonrect.x, self.buttonrect.y, self.buttonrect.width, self.buttonrect.height = (self.x, self._y, (self.imageRect.width+12 + self.width),
                                      self.imageRect.height + 12 + self.height)
        if not(self._autoResizing):
            self.buttonrect.width, self.buttonrect.height = self._width, self._height
        self.rect = pygame.Rect(self._x-self.outlineWidth, self._y-self.outlineWidth, self.buttonrect.width + (self._outlineWidth*2), self.buttonrect.height + (self._outlineWidth*2))

    @property
    def fontSize(self):
        return self._fontSize
    
    @fontSize.setter
    def fontSize(self, value):
        self._fontSize = value
        if self.fontName[-4:] == ".ttf":
            self.font = pygame.font.Font(self.fontName, self._fontSize)
        else:
            self.font = pygame.font.SysFont(self.fontName, self._fontSize)
        self.img = self.font.render(self._text, True, self.displayColor)
        self.imageRect = self.img.get_rect()
        self.buttonrect.x, self.buttonrect.y, self.buttonrect.width, self.buttonrect.height = (self._x, self._y, (self.imageRect.width+12 + self.width),
                                      self.imageRect.height + 12 + self.height)
        self.rect = pygame.Rect(self._x-self.outlineWidth, self._y-self.outlineWidth, self.buttonrect.width + (self._outlineWidth*2), self.buttonrect.height + (self._outlineWidth*2))

    @property
    def fontName(self):
        return self._fontName
    
    @fontName.setter
    def fontName(self, value):
        self._fontName = value
        try:
            if self.fontName[-4:] == ".ttf":
                self.font = pygame.font.Font(self.fontName, self._fontSize)
            else:
                self.font = pygame.font.SysFont(self.fontName, self._fontSize)
        except:
            self._fontName = defaultFont
            if self.fontName[-4:] == ".ttf":
                self.font = pygame.font.Font(self.fontName, self._fontSize)
            else:
                self.font = pygame.font.SysFont(self.fontName, self._fontSize)
        self.img = self.font.render(self._text, True, self.displayColor)
        self.imageRect = self.img.get_rect()
        self.rect = pygame.Rect(self._x-self.outlineWidth, self._y-self.outlineWidth, self.buttonrect.width + (self._outlineWidth*2), self.buttonrect.height + (self._outlineWidth*2))

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
        if self._autoResizing:
            self.buttonrect = pygame.Rect(self._x, self._y, (self.imageRect.width+12 + self.width),
                                        self.imageRect.height + 12 + self.height)
        else:
            self.buttonrect.width = self._width
        self.rect.width = self.buttonrect.width + (self._outlineWidth*2)

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value
        if self._autoResizing:
            self.buttonrect = pygame.Rect(self._x, self._y, (self.imageRect.width+12 + self.width),
                                        self.imageRect.height + 12 + self.height)
        else:
            self.buttonrect.height = self._height
        self.rect.height = self.buttonrect.height + (self._outlineWidth*2)

    @property
    def autoResizing(self):
        return self._autoResizing
    
    @autoResizing.setter
    def autoResizing(self, value: bool):
        self._autoResizing = value
        if self._autoResizing:
            self.buttonrect = pygame.Rect(self._x, self._y, (self.imageRect.width+12 + self.width),
                                        self.imageRect.height + 12 + self.height)
        else:
            self.buttonrect.width, self.buttonrect.height = self._width, self._height
        self.rect.width = self.buttonrect.width + (self._outlineWidth*2)
        self.rect.height = self.buttonrect.height + (self._outlineWidth*2)

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self.buttonrect.x, self.buttonrect.y = self._x, self._y
        self.outlinerect.x = self.buttonrect.x - self._outlineWidth
        self.rect.x = self._x - self._outlineWidth

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self.buttonrect.x, self.buttonrect.y = self._x, self._y
        self.outlinerect.y = self.buttonrect.y - self._outlineWidth
        self.rect.y = self._y - self._outlineWidth

    @property
    def hide(self):
        return self._hide
    
    @hide.setter
    def hide(self, value: bool):
        self._hide = value

    @property
    def changeCursor(self):
        return self._changeCursor

    @changeCursor.setter
    def changeCursor(self, value: bool):
        self._changeCursor = value

    def _has_arguments(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters
        argument_names = [param.name for param in parameters.values()]
        if len(argument_names) > 0:
            return True
        else:
            return False

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def mouse_hovering(self):
        pos = pygame.mouse.get_pos()
        if self.buttonrect.collidepoint(pos):
            return True

    # Centering button in the x axis
    def center_x(self, surface=None):
        global _windowObject
        if surface == None:
            surface = _windowObject

        self._x = (surface.screen_width - self.buttonrect.width) // 2
        self.buttonrect.x = (surface.screen_width - self.buttonrect.width) // 2
        self.rect.x = self._x - self._outlineWidth
        

    # Centering button in the y axis
    def center_y(self, surface=None):
        global _windowObject
        if surface == None:
            surface = _windowObject

        self._y = (surface.screen_height // 2) - self.buttonrect.height // 2
        self.buttonrect.y = (surface.screen_height // 2) - self.buttonrect.height // 2
        self.rect.y = (self._y - self._outlineWidth)

    # Centering button in the x and y axis (middle of the window)
    def center(self, surface=None):
        global _windowObject
        if surface == None:
            surface = _windowObject

        self._x = (surface.screen_width - self.buttonrect.width) // 2
        self.buttonrect.x = (surface.screen_width - self.buttonrect.width) // 2
        self._y = ((surface.screen_height // 2) - self.buttonrect.height // 2)
        self.buttonrect.y = ((surface.screen_height // 2) - self.buttonrect.height // 2)
        self.rect.x = self._x - self._outlineWidth
        self.rect.y = (self._y - self._outlineWidth)

    def mouse_click(self):
        pos = pygame.mouse.get_pos()
        if self.buttonrect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

    # Drawing all the stuff to the window and handling events
    def draw(self, surface=None):
        global _windowObject, _changingCursor, _clickedObjects
        if not(self._hide):
            pos = pygame.mouse.get_pos()

            if not(self.rect.collidepoint(pygame.mouse.get_pos())):
                if pygame.mouse.get_pressed()[0] == 1:
                    if self.dropDownMenu != None:
                        if self.dropDownMenu.active:
                            mouseCollided = False
                            for index, item in enumerate(self.dropDownMenu._optionButtons):
                                if self.dropDownMenu._optionButtons[index][0].rect.collidepoint(pygame.mouse.get_pos()):
                                    mouseCollided = True
                                    break
                            if not(mouseCollided):
                                self.dropDownMenu.active = False

            if surface == None:
                surface = _windowObject.screen
            self.img = self.font.render(self._text, True, self.displayColor)
            self.imageRect = self.img.get_rect()
            self.imageRect.topleft = (self._x, self._y)
            
            x = self.buttonrect.x
            y = self.buttonrect.y

            if self.clickAnimation == True and self.clicked:
                x += 1
                y += 1

            if self._outlineWidth > 0:
                if self.borderRadius > 1:
                    if not(self.bordersToHide.__contains__("topleft")):
                        gfxdraw.aacircle(surface, (x + self.borderRadius)-self._outlineWidth, (y + self.borderRadius)-self._outlineWidth, self.borderRadius, self.outlineColor0)
                        gfxdraw.filled_circle(surface, (x + self.borderRadius)-self._outlineWidth, (y + self.borderRadius)-self._outlineWidth, self.borderRadius, self.outlineColor0)
                    if not(self.bordersToHide.__contains__("topright")):
                        gfxdraw.aacircle(surface, (x + self.buttonrect.width - self.borderRadius-1)+self._outlineWidth, (y + self.borderRadius)-self._outlineWidth, self.borderRadius, self.outlineColor0)
                        gfxdraw.filled_circle(surface, (x + self.buttonrect.width - self.borderRadius-1)+self._outlineWidth, (y + self.borderRadius)-self._outlineWidth, self.borderRadius, self.outlineColor0)
                    if not(self.bordersToHide.__contains__("bottomleft")):
                        gfxdraw.aacircle(surface, (x + self.borderRadius)-self._outlineWidth, (y + self.buttonrect.height - self.borderRadius-1)+self._outlineWidth, self.borderRadius, self.outlineColor0)
                        gfxdraw.filled_circle(surface, (x + self.borderRadius)-self._outlineWidth, (y + self.buttonrect.height - self.borderRadius-1)+self._outlineWidth, self.borderRadius, self.outlineColor0)
                    if not(self.bordersToHide.__contains__("bottomright")):
                        gfxdraw.aacircle(surface, (x + self.buttonrect.width - self.borderRadius-2)+self._outlineWidth, (y + self.buttonrect.height - self.borderRadius-1)+self._outlineWidth, self.borderRadius, self.outlineColor0)
                        gfxdraw.filled_circle(surface, (x + self.buttonrect.width - self.borderRadius-2)+self._outlineWidth, (y + self.buttonrect.height - self.borderRadius-1)+self._outlineWidth, self.borderRadius, self.outlineColor0)

                    pygame.draw.rect(surface, self.outlineColor0, ((x + self.borderRadius)-self._outlineWidth, y-self._outlineWidth, (self.buttonrect.width - 2 * self.borderRadius)+self._outlineWidth*2, self.buttonrect.height+self._outlineWidth*2))
                    pygame.draw.rect(surface, self.outlineColor0, ((x)-self._outlineWidth, y + self.borderRadius-self._outlineWidth, self.buttonrect.width+self._outlineWidth*2, (self.buttonrect.height - 2 * self.borderRadius)+self._outlineWidth*2))
                else:
                    pygame.draw.rect(surface, self.outlineColor0, self.outlinerect)

            if self.borderRadius > 1:
                if not(self.bordersToHide.__contains__("topleft")):
                    gfxdraw.aacircle(surface, x + self.borderRadius, y + self.borderRadius, self.borderRadius, self.background0)
                    gfxdraw.filled_circle(surface, x + self.borderRadius, y + self.borderRadius, self.borderRadius, self.background0)
                if not(self.bordersToHide.__contains__("topright")):
                    gfxdraw.aacircle(surface, x + self.buttonrect.width - self.borderRadius-1, y + self.borderRadius, self.borderRadius, self.background0)
                    gfxdraw.filled_circle(surface, x + self.buttonrect.width - self.borderRadius-1, y + self.borderRadius, self.borderRadius, self.background0)
                if not(self.bordersToHide.__contains__("bottomleft")):
                    gfxdraw.aacircle(surface, x + self.borderRadius, y + self.buttonrect.height - self.borderRadius-1, self.borderRadius, self.background0)
                    gfxdraw.filled_circle(surface, x + self.borderRadius, y + self.buttonrect.height - self.borderRadius-1, self.borderRadius, self.background0)
                if not(self.bordersToHide.__contains__("bottomright")):
                    gfxdraw.aacircle(surface, x + self.buttonrect.width - self.borderRadius-2, y + self.buttonrect.height - self.borderRadius-1, self.borderRadius, self.background0)
                    gfxdraw.filled_circle(surface, x + self.buttonrect.width - self.borderRadius-2, y + self.buttonrect.height - self.borderRadius-1, self.borderRadius, self.background0)

            pygame.draw.rect(surface, self.background0, (x + self.borderRadius, y, self.buttonrect.width - 2 * self.borderRadius, self.buttonrect.height))
            pygame.draw.rect(surface, self.background0, (x, y + self.borderRadius, self.buttonrect.width, self.buttonrect.height - 2 * self.borderRadius))

            if self.bordersToHide.__contains__("topleft"):
                pygame.draw.rect(surface, self.background0, (x-self._outlineWidth, y-self._outlineWidth, ((x + self.borderRadius)-x)+(self.outlineWidth*2), self.borderRadius+self._outlineWidth))
                if self._outlineWidth > 0:
                    pygame.draw.rect(surface, self.outlineColor0, (x-self._outlineWidth, y-self._outlineWidth, self._outlineWidth, self.borderRadius+self._outlineWidth))
                    pygame.draw.rect(surface, self.outlineColor0, (x-self._outlineWidth, y-self._outlineWidth, ((x + self.borderRadius)-x)+(self.outlineWidth*2), self._outlineWidth))

            if self.bordersToHide.__contains__("topright"):
                pygame.draw.rect(surface, self.background0, ((x + self.borderRadius+self.buttonrect.width - 2 * self.borderRadius-self._outlineWidth), y-self._outlineWidth, ((x + self.borderRadius)-x)+(self.outlineWidth*2), self.borderRadius+self._outlineWidth))
                if self._outlineWidth > 0:
                    if self._outlineWidth > 0:
                        pygame.draw.rect(surface, self.outlineColor0, (((x + self.borderRadius+self.buttonrect.width - 2 * self.borderRadius-self._outlineWidth)+((x + self.borderRadius)-x)+self.outlineWidth), y-self._outlineWidth, self._outlineWidth, self.borderRadius+(self._outlineWidth*2)))
                        pygame.draw.rect(surface, self.outlineColor0, ((x + self.borderRadius+self.buttonrect.width - 2 * self.borderRadius-self._outlineWidth), y-self._outlineWidth, ((x + self.borderRadius)-x)+(self.outlineWidth*2), self._outlineWidth))

            if self.bordersToHide.__contains__("bottomleft"):
                pygame.draw.rect(surface, self.background0, (x-self._outlineWidth, (y-self._outlineWidth)+self.buttonrect.height-self.borderRadius+self._outlineWidth, (((x + self.borderRadius)-x)+(self._outlineWidth*2)), self.borderRadius+self._outlineWidth))
                if self._outlineWidth > 0:
                    pygame.draw.rect(surface, self.outlineColor0, (x-self._outlineWidth, (y-self._outlineWidth)+self.buttonrect.height-self.borderRadius+self._outlineWidth, self._outlineWidth, self.borderRadius+self._outlineWidth))
                    pygame.draw.rect(surface, self.outlineColor0, (x-self._outlineWidth, (y-self._outlineWidth)+self.buttonrect.height-self.borderRadius+self._outlineWidth+self.borderRadius, ((x + self.borderRadius)-x)+(self.outlineWidth*2), self._outlineWidth))

            if self.bordersToHide.__contains__("bottomright"):
                pygame.draw.rect(surface, self.background0, ((x + self.borderRadius+self.buttonrect.width - 2 * self.borderRadius-self._outlineWidth), (y-self._outlineWidth)+self.buttonrect.height-self.borderRadius, ((x + self.borderRadius)-x)+(self.outlineWidth*2), self.borderRadius+(self._outlineWidth*2)))
                if self._outlineWidth > 0:
                    pygame.draw.rect(surface, self.outlineColor0, (((x + self.borderRadius+self.buttonrect.width - 2 * self.borderRadius-self._outlineWidth)+((x + self.borderRadius)-x)+self.outlineWidth), (y-self._outlineWidth)+self.buttonrect.height-self.borderRadius, self._outlineWidth, self.borderRadius+(self._outlineWidth*2)))
                    pygame.draw.rect(surface, self.outlineColor0, ((x + self.borderRadius+self.buttonrect.width - 2 * self.borderRadius-self._outlineWidth), ((y-self._outlineWidth)+self.buttonrect.height-self.borderRadius)+self.borderRadius+self._outlineWidth, ((x + self.borderRadius)-x)+(self.outlineWidth*2), self._outlineWidth))

            action = False

            if self.dropDownMenu != None:
                self.dropDownMenu.draw()

            if not(self.buttonrect.collidepoint(pos)) and pygame.mouse.get_pressed()[0] == 1:
                if not(self.clickedOutside):
                    self.clickedOutside = True
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clickedOutside = False

            # check mouseover and clicked conditions
            if self.z_index == None:
                self._hoveringAction = True
            if self.active:
                if self.buttonrect.collidepoint(pos) and not(self.disable):
                    if not(_clickedObjects.__contains__(self)):
                        _clickedObjects.append(self)
                    if self._hoveringAction:
                        if self._changeCursor:
                            _changingCursor = pygame.SYSTEM_CURSOR_HAND
                        if self.hoverEvent != None:
                            if self._has_arguments(self.hoverEvent):
                                self.hoverEvent(self)
                            else:
                                self.hoverEvent()
                        if not(self.clicked):
                            self.background0 = self.hoverBackground
                            self.outlineColor0 = self.hoverOutlineColor
                            self.displayColor = self.hoverTextColor
                        else:
                            self.displayColor = self.activeTextColor
                        self.bottomColor0 = self.hoverColorBottom
                        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and self.buttonrect.collidepoint(pos):
                            if not(self.clickedOutside):
                                self.background0 = self.activeBackground
                                self.outlineColor0 = self.activeOutlineColor

                                self.clicked = True
                    else:
                        self.background0 = self.background
                        # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        self.background0 = self.background
                        self.displayColor = self.textColor
                        self.bottomColor0 = self.bottomColor
                        self.outlineColor0 = self.outlineColor
                else:
                    self.background0 = self.background
                    # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.background0 = self.background
                    self.displayColor = self.textColor
                    self.bottomColor0 = self.bottomColor
                    self.outlineColor0 = self.outlineColor

                if not(self.clickedOutside):
                    if pygame.mouse.get_pressed()[0] == 0 and self.buttonrect.collidepoint(pos):
                        if self.clicked and self._hoveringAction:
                            action = True
                            if self.dropDownMenu != None:
                                if not(self.dropDownMenu.active):
                                    self.dropDownMenu.x = self._x
                                    self.dropDownMenu.y = self._y+self.rect.height
                                    self.dropDownMenu.active = True
                                else:
                                    self.dropDownMenu.active = False
                            if self.clickEvent != None:
                                if self._has_arguments(self.clickEvent):
                                    self.clickEvent(self)
                                else:
                                    self.clickEvent()
                        self.clicked = False
                    elif not(self.buttonrect.collidepoint(pos)):
                        self.clicked = False

            textPositions = ["center", "left", "right"]
            if not(textPositions.__contains__(self.textPosition)):
                self.textPosition = "center"
            if self.textPosition == "left":
                surface.blit(self.img, (x + self._outlineWidth + 4 +self.textOffsetX, y + (self.buttonrect.height - self.img.get_height()) // 2 + self.textOffsetY))
            elif self.textPosition == "center":
                surface.blit(self.img, (x + (self.buttonrect.width - self.img.get_width()) // 2 + self.textOffsetX , y + (self.buttonrect.height - self.img.get_height()) // 2 + self.textOffsetY))
            elif self.textPosition == "right":
                pass
            
            return action

class ImageButton():
    def __init__(self, **kwargs):
        global _windowObject, _clickableObjects
        self._x = kwargs.get("x", 0)
        self._x = kwargs.get("_x", self._x)
        self._y = kwargs.get("y", 0)
        self._y = kwargs.get("_y", self._y)
        self._changeCursor = kwargs.get("changeCursor", True)
        self._changeCursor = kwargs.get("_changeCursor", self._changeCursor)
        self.fill = kwargs.get("fill", None)
        self.clickAnimation: bool = kwargs.get("clickAnimation", False)

        self._clicked = False
        self.clickedOutside = False

        self._image0 = kwargs.get("image", "PyniteAssets/no-image2.png")
        self._image0 = kwargs.get("_image", self._image0)
        self._image0_2 = kwargs.get("image2", self._image0)
        self._image0_2 = kwargs.get("_image2", self._image0_2)

        self._image0 = kwargs.get("_image0", self._image0)
        self._image0_2 = kwargs.get("_image0_2", self._image0_2)

        if not(self._image0.__contains__(_filePath)):
            if os.path.exists(f"{_filePath}/" + self._image0):
                self._image0 = f"{_filePath}/" + self._image0
            elif os.path.exists(self._image0):
                pass
            else:
                self._image0 = "PyniteAssets/no-image2.png"
        if not(self._image0_2.__contains__(_filePath)):
            if os.path.exists(f"{_filePath}/" + self._image0_2):
                self._image0_2 = f"{_filePath}/" + self._image0_2
            elif os.path.exists(self._image0_2):
                pass
            else:
                self._image0_2 = "PyniteAssets/no-image2.png"

        self._image = pygame.image.load(self._image0).convert_alpha()
        self._image2 = pygame.image.load(self._image0_2).convert_alpha()
        
        self._scale = kwargs.get("scale", 1)
        self._scale = kwargs.get("_scale", self._scale)
        self.name = kwargs.get("name", None)
        self.z_index = kwargs.get("z_index", None)
        self._hide = kwargs.get("hide", False)
        self._hide = kwargs.get("_hide", self._hide)
        self.disable = kwargs.get("disable", False)
        
        self.clickEvent = None
        self.hoverEvent = None

        self._hoveringAction = False

        self._width = self._image.get_rect().width
        self._height = self._image.get_rect().height
        self._width2 = self._image2.get_rect().width
        self._height2 = self._image2.get_rect().height

        self._image = pygame.transform.scale(self._image, (int(self._width * self._scale), int(self._height * self._scale)))
        self._image2 = pygame.transform.scale(self._image2, (int(self._width2 * self._scale), int(self._height2 * self._scale)))

        self.rect = pygame.Rect(self._x, self._y, self._image.get_rect().width, self._image.get_rect().height)

        self._imageToDraw = self._image

        _allObjects.append(self)
        _clickableObjects.append(self)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = self._y

    @property
    def changeCursor(self):
        return self._changeCursor

    @changeCursor.setter
    def changeCursor(self, value: bool):
        self._changeCursor = value

    @property
    def image(self):
        return self._image0

    @image.setter
    def image(self, value):
        self._image0 = value
        if not(self._image0.__contains__(_filePath)):
            if os.path.exists(f"{_filePath}/" + self._image0):
                self._image0 = f"{_filePath}/" + self._image0
            elif os.path.exists(self._image0):
                pass
            else:
                self._image0 = "PyniteAssets/no-image2.png"
        self._image = pygame.image.load(self._image0).convert_alpha()
        self._width, self._height = self._image.get_rect().width, self._image.get_rect().height
        self._image = pygame.transform.scale(self._image, (int(self._width * self._scale), int(self._height * self._scale)))
        self.rect.width, self.rect.height = self._image.get_width(), self._image.get_height()

    @property
    def image2(self):
        return self._image0_2
    
    @image2.setter
    def image2(self, value):
        self._image0_2 = value
        if not(self._image0_2.__contains__(_filePath)):
            if os.path.exists(f"{_filePath}/" + self._image0_2):
                self._image0_2 = f"{_filePath}/" + self._image0_2
            elif os.path.exists(self._image0_2):
                pass
            else:
                self._image0_2 = "PyniteAssets/no-image2.png"
        self._image2 = pygame.image.load(self._image0_2).convert_alpha()
        self._width2, self._height2 = self._image2.get_rect().width, self._image2.get_rect().height
        self._image2 = pygame.transform.scale(self._image2, (int(self._width2 * self._scale), int(self._height2 * self._scale)))
        
    @property
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, value):
        self._scale = value
        self._image = pygame.transform.scale(pygame.image.load(self._image0).convert_alpha(), (int(self._width * self._scale), int(self._height * self._scale)))
        self._image2 = pygame.transform.scale(pygame.image.load(self._image0_2).convert_alpha(), (int(self._width2 * self._scale), int(self._height2 * self._scale)))
        self.rect.width, self.rect.height = self._image.get_width(), self._image.get_height()
    
    @property
    def hide(self):
        return self._hide
    
    @hide.setter
    def hide(self, value: bool):
        self._hide = value

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def _has_arguments(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters
        argument_names = [param.name for param in parameters.values()]
        if len(argument_names) > 0:
            return True
        else:
            return False

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def mouse_hovering(self):
        if self._image.get_rect(topleft=(self._x, self._y)).collidepoint(pygame.mouse.get_pos()):
            return True
        
    def mouse_click(self):
        if self._image.get_rect(topleft=(self._x, self._y)).collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

    def center(self):
        surface = _windowObject
        self._x = (surface.screen_width - self._width) // 2
        self._y = ((surface.screen_height // 2) - self._height // 2)

    def center_x(self):
        surface = _windowObject
        self._x = (surface.screen_width - self._width) // 2

    def center_y(self):
        surface = _windowObject
        self._y = ((surface.screen_height // 2) - self._height // 2)

    def draw(self, surface=None):
        global _windowObject, _changingCursor, _clickedObjects
        if not(self._hide):
            if surface == None:
                surface = _windowObject.screen

            x = self._x
            y = self._y

            if self.clickAnimation and self._clicked:
                x += 1
                y += 1

            pos = pygame.mouse.get_pos()
            if self.fill != None and self.fill != "None":
                pygame.draw.rect(surface, self.fill, self.rect)
            surface.blit(self._imageToDraw, (x, y))
            
            if not(self.disable):
                if not(self._image.get_rect(topleft=(x, y)).collidepoint(pos)) and pygame.mouse.get_pressed()[0] == 1:
                    self.clickedOutside = True
                elif pygame.mouse.get_pressed()[0] == 0:
                    self.clickedOutside = False

                if self.z_index == None:
                    self._hoveringAction = True

                if self._image.get_rect(topleft=(x, y)).collidepoint(pos):
                    if not(_clickedObjects.__contains__(self)):
                        _clickedObjects.append(self)
                    if self._hoveringAction:
                        if self._changeCursor:
                            _changingCursor = pygame.SYSTEM_CURSOR_HAND
                        if self.hoverEvent != None:
                            if self._has_arguments(self.hoverEvent):
                                self.hoverEvent(self)
                            else:
                                self.hoverEvent()

                        self._imageToDraw = self._image2
                        if pygame.mouse.get_pressed()[0] == 1 and not(self.clickedOutside):
                            self._clicked = True

                        if not(self.clickedOutside):
                            if pygame.mouse.get_pressed()[0] == 0 and self._clicked:
                                self._clicked = False
                                if self.clickEvent != None:
                                    if self._has_arguments(self.clickEvent):
                                        self.clickEvent(self)
                                    else:
                                        self.clickEvent()
                                return True
                    else:
                        self._clicked = False
                        self._imageToDraw = self._image
                else:
                    self._clicked = False
                    self._imageToDraw = self._image
            else:
                self._imageToDraw = self._image


class Image():
    def __init__(self, **kwargs):
        global _windowObject
        self._x = kwargs.get("x", 0)
        self._x = kwargs.get("_x", self._x)
        self._y = kwargs.get("y", 0)
        self._y = kwargs.get("_y", self._y)
        self._scale = kwargs.get("scale", 1)
        self._scale = kwargs.get("_scale", self._scale)
        image = None
        self.image0 = None
        if kwargs.__contains__("image"):
            if not(kwargs["image"].__contains__(_filePath)):
                kwargs["image"] = f"{_filePath}/" + kwargs["image"]
                image = pygame.image.load(kwargs['image']).convert_alpha()
                self.image0 = kwargs['image']
        elif kwargs.__contains__("image0"):
            if not(kwargs["image0"].__contains__(_filePath)):
                kwargs["image0"] = f"{_filePath}/" + kwargs["image0"]
            image = pygame.image.load(kwargs['image0']).convert_alpha()
            self.image0 = kwargs['image0']

        self.fill = kwargs.get("fill", None)
        self.name = kwargs.get("name", None)
        self._hide = kwargs.get("hide", False)
        self._hide = kwargs.get("_hide", self._hide)
        self.z_index = kwargs.get("z_index", None)
        self.clickEvent = None
        self.hoverEvent = None
        self._width = image.get_width()
        self._height = image.get_height()
        self._image = pygame.transform.scale(image, (int( self._width * self.scale), int( self._height * self.scale)))
        self.rect = pygame.Rect(self._x, self._y, self._image.get_width(), self._image.get_height())

        _allObjects.append(self)

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value: int):
        self._x = value
        self.rect.x = self._x

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value: int):
        self._y = value
        self.rect.y = self._y

    @property
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, value):
        self._scale = value
        self._image = pygame.transform.scale(pygame.image.load(self.image0).convert_alpha(), (int(self._width * self._scale), int( self._height * self._scale)))
        self.rect.width, self.rect.height = self._image.get_width(), self._image.get_height()

    @property
    def image(self):
        return self.image0
    
    @image.setter
    def image(self, value):
        self.image0 = value
        image = pygame.image.load(value).convert_alpha()
        self._width = image.get_width()
        self._height = image.get_height()
        self._image = pygame.transform.scale(pygame.image.load(value).convert_alpha(), (int(self._width * self.scale), int(self._height * self.scale)))
        self.rect.width, self.rect.height = self._image.get_width(), self._image.get_height()

    @property
    def hide(self):
        return self._hide
    
    @hide.setter
    def hide(self, value: bool):
        self._hide = value

    def _has_arguments(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters
        argument_names = [param.name for param in parameters.values()]
        if len(argument_names) > 0:
            return True
        else:
            return False

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def mouse_hovering(self):
        if self._image.get_rect(topleft=(self.x, self.y)).collidepoint(pygame.mouse.get_pos()):
            return True
        
    def mouse_click(self):
        if self._image.get_rect(topleft=(self.x, self.y)).collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

    def draw(self, surface=None):
        global _windowObject
        pos = pygame.mouse.get_pos()
        if self._image.get_rect(topleft=(self.x, self.y)).collidepoint(pos):
            if self.hoverEvent != None:
                if self._has_arguments(self.hoverEvent):
                    self.hoverEvent(self)
                else:
                    self.hoverEvent()
            if pygame.mouse.get_pressed()[0] == 1:
                if self.clickEvent != None:
                    if self._has_arguments(self.clickEvent):
                        self.clickEvent(self)
                    else:
                        self.clickEvent()
        if not(self._hide):
            if surface == None:
                surface = _windowObject.screen

            if self.fill != None and self.fill != "None":
                pygame.draw.rect(surface, self.fill, self.rect)

            surface.blit(self._image, (self._x, self._y))

class Rectangle(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        global _allObjects, _windowObject
        pygame.sprite.Sprite.__init__(self)
        self._x: int = kwargs.get("x", 0)
        self._y: int = kwargs.get("y", 0)
        self._x: int = kwargs.get("_x", self._x)
        self._y: int = kwargs.get("_y", self._y)
        self._width: int = kwargs.get("width", 40)
        self._width: int = kwargs.get("_width", self._width)
        self._height: int = kwargs.get("height", 40)
        self._height: int = kwargs.get("_height", self._height)
        self.background: tuple = kwargs.get("background", (255,255,255))
        self.thickness: int = kwargs.get("thickness", 0)
        self.borderRadius: int = kwargs.get("borderRadius", 0)
        self.rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self.name: str = kwargs.get("name", None)
        self.z_index: int = kwargs.get("z_index", None)
        self._hide = kwargs.get("hide", False)
        self._hide = kwargs.get("_hide", self._hide)
        
        self.clickEvent = None
        self.hoverEvent = None

        _allObjects.append(self)

    def mouse_click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

    def mouse_hovering(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = value

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = self._y

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
        self.rect.width = value

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value
        self.rect.height = value

    @property
    def hide(self):
        return self._hide
    
    @hide.setter
    def hide(self, value: bool):
        self._hide = value

    def _has_arguments(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters
        argument_names = [param.name for param in parameters.values()]
        if len(argument_names) > 0:
            return True
        else:
            return False

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def center(self):
        self._x = (_windowObject.screen_width // 2) - self.rect.width // 2
        self._y = ((_windowObject.screen_height // 2) - self.rect.height // 2)
        self.rect.x, self.rect.y = self._x, self._y

    def center_x(self):
        self._x = (_windowObject.screen_width // 2) - self.rect.width // 2
        self.rect.x = self._x

    def center_y(self):
        self._y = ((_windowObject.screen_height // 2) - self.rect.height // 2)
        self.rect.y = self._y

    def draw(self, surface=None):
        global _windowObject
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.hoverEvent != None:
                if self._has_arguments(self.hoverEvent):
                    self.hoverEvent(self)
                else:
                    self.hoverEvent()
            if pygame.mouse.get_pressed()[0] == 1:
                if self.clickEvent != None:
                    if self._has_arguments(self.clickEvent):
                        self.clickEvent(self)
                    else:
                        self.clickEvent()
        if not(self._hide):
            if surface == None:
                surface = _windowObject.screen
            pygame.draw.rect(surface, self.background, self.rect,self.thickness,self.borderRadius)

class Surface():
    def __init__(self, **kwargs):
        global _allObjects, _windowObject
        pygame.sprite.Sprite.__init__(self)
        self._x: int = kwargs.get("x", 0)
        self._y: int = kwargs.get("y", 0)
        self._x: int = kwargs.get("_x", self._x)
        self._y: int = kwargs.get("_y", self._y)
        self._width: int = kwargs.get("width", 40)
        self._width: int = kwargs.get("_width", self._width)
        self._height: int = kwargs.get("height", 40)
        self._height: int = kwargs.get("_height", self._height)
        self.background: tuple = kwargs.get("background", (255,255,255))
        self.name: str = kwargs.get("name", None)
        self.z_index: int = kwargs.get("z_index", None)
        self._hide = kwargs.get("hide", False)
        self._hide = kwargs.get("_hide", self._hide)

        self.surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        self.rect = pygame.Rect(self._x, self._y, self._width, self._height)
        
        self.clickEvent = None
        self.hoverEvent = None

        _allObjects.append(self)

    def mouse_click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

    def mouse_hovering(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = value

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = self._y

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
        self.surface = pygame.Surface((self._width, self._height))
        self.rect.width = self.surface.get_width()

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value
        self.surface = pygame.Surface((self._width, self._height))
        self.rect.height = self.surface.get_height()

    @property
    def hide(self):
        return self._hide
    
    @hide.setter
    def hide(self, value: bool):
        self._hide = value

    def _has_arguments(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters
        argument_names = [param.name for param in parameters.values()]
        if len(argument_names) > 0:
            return True
        else:
            return False

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def center(self):
        self._x = (_windowObject.screen_width // 2) - self.rect.width // 2
        self._y = ((_windowObject.screen_height // 2) - self.rect.height // 2)
        self.rect.x, self.rect.y = self._x, self._y

    def center_x(self):
        self._x = (_windowObject.screen_width // 2) - self.rect.width // 2
        self.rect.x = self._x

    def center_y(self):
        self._y = ((_windowObject.screen_height // 2) - self.rect.height // 2)
        self.rect.y = self._y

    def draw(self, surface=None):
        global _windowObject
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.hoverEvent != None:
                if self._has_arguments(self.hoverEvent):
                    self.hoverEvent(self)
                else:
                    self.hoverEvent()
            if pygame.mouse.get_pressed()[0] == 1:
                if self.clickEvent != None:
                    if self._has_arguments(self.clickEvent):
                        self.clickEvent(self)
                    else:
                        self.clickEvent()
        if not(self._hide):
            if surface == None:
                surface = _windowObject.screen
            self.surface.fill(self.background)
            surface.blit(self.surface, (self._x, self._y))

class Circle(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self._x = kwargs.get("x", 0)
        self._x = kwargs.get("_x", self._x)
        self._y = kwargs.get("y", 0)
        self._y = kwargs.get("_y", self._y)
        self._radius = kwargs.get("radius", 8)
        self._radius = kwargs.get("_radius", self._radius)
        self.background = kwargs.get("background", (255,255,255))
        self.showHitbox = kwargs.get("showHitbox", False)
        self._changeCursor = kwargs.get("changeCursor", False)
        self._changeCursor = kwargs.get("_changeCursor", self._changeCursor)
        self._hide = kwargs.get("hide", False)
        self._hide = kwargs.get("_hide", self._hide)
        self.name = kwargs.get("name", None)
        self.z_index = kwargs.get("z_index", None)

        self.rect = pygame.Rect(self._x, self._y, self._radius * 2, self._radius * 2)

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = value

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = self._y

    @property
    def hide(self):
        return self._hide
    
    @hide.setter
    def hide(self, value: bool):
        self._hide = value

    @property
    def changeCursor(self):
        return self._changeCursor

    @changeCursor.setter
    def changeCursor(self, value: bool):
        self._changeCursor = value
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value: int):
        self._radius = value
        self.rect.width, self.rect.height = self._radius * 2, self._radius * 2

    def mouse_click(self):
        cursor_pos = pygame.mouse.get_pos()
        dx = abs(cursor_pos[0] - self._x-self._radius)
        dy = abs(cursor_pos[1] - self._y-self._radius)
        distance_squared = dx*dx + dy*dy
        if distance_squared <= self.radius*self.radius:
            if pygame.mouse.get_pressed()[0] == 1:
                return True

    def mouse_hovering(self):
        cursor_pos = pygame.mouse.get_pos()
        dx = abs(cursor_pos[0] - self._x-self._radius)
        dy = abs(cursor_pos[1] - self._y-self._radius)
        distance_squared = dx*dx + dy*dy
        if distance_squared <= self.radius*self.radius:
            return True

    def draw(self, surface=None):
        global _windowObject, _changingCursor
        if not(self._hide):
            if self.mouse_hovering:
                if self._changeCursor:
                    _changingCursor = pygame.SYSTEM_CURSOR_HAND
            if surface == None:
                surface = _windowObject.screen
            gfxdraw.aacircle(surface, int(self._x+self.radius), int(self._y+self.radius), self._radius, self.background)
            gfxdraw.filled_circle(surface, int(self._x+self.radius), int(self._y+self.radius), self._radius, self.background)
            if self.showHitbox:
                pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)

# Class for making combinations of key presses (e.g: CTRL + C) (max number of keys: 3)
class KeyBindCombination():
    def __init__(self, **kwargs):
        self.keys = 2
        self.key1 = kwargs['key1']
        self.key2 = kwargs['key2']
        self.key3 = kwargs.get("key3", None)

        self.key1Active = False
        self.key1Active = False
        self.key1Active = False
        
        if self.key3 != None:
            self.keys = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.key1]:
            self.key1Active = True
        else:
            self.key1Active = False

        if keys[self.key2]:
            self.key2Active = True
        else:
            self.key2Active = False
            
        if self.key3 != None:
            if keys[self.key3]:
                self.key3Active = True
            else:
                self.key3Active = False

        if self.keys == 2 and self.key1Active and self.key2Active:
            return True
        elif self.keys == 3 and self.key1Active and self.key2Active and self.key3Active:
            return True

# Class for making object which contains specific variables such as health, gravity, jump etc...
# can be represented only as an image which has it's own hitbox
class Object(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.scale = kwargs.get("scale", 1)
        self.image = kwargs.get("image", None)
        self.width = kwargs.get("width", 40)
        self.height = kwargs.get("height", 40)
        self.img_width = None
        self.img_height = None
        self.move_up = False
        self.move_right = False
        self.move_down = False
        self.move_left = False
        self.showHitbox = kwargs.get("showHitbox", False)
        self.speed = kwargs.get("speed", 4)
        self.gravity = 0.75
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.direction = 1
        self.hitboxX = kwargs.get("hitboxX", 0)
        self.hitboxY = kwargs.get("hitboxY", 0)
        self.color = kwargs.get("color", (255,255,255))
        self.jumpHeight = kwargs.get("jumpHeight", -11)
        self.jumpDirection = None
        self.health = kwargs.get("health", None)
        self._hide = kwargs.get("hide", False)
        self._hide = kwargs.get("_hide", self._hide)

        self.rect = None
        self.hitbox = None

        self.vertical_flip = False
        self.horizontal_flip = False
        img = None
        if self.image != None:
            img = pygame.image.load(self.image).convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.img_width = self.image.get_width()
            self.img_height = self.image.get_height()

        else:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            self.hitbox = pygame.Rect(self.x - 1 + (self.hitboxX), self.y - 1 + (self.hitboxY),
                                    (self.width * self.scale) + 2 + (self.hitboxX * -2),
                                    (self.height * self.scale) + 2 + (self.hitboxY * -2))

    @property
    def hide(self):
        return self._hide
    
    @hide.setter
    def hide(self, value: bool):
        self._hide = value

    def collision(self, firstRect, secondRect):
        self.colliding = False
        self.firsRect = firstRect
        self.secondRect = secondRect
        if self.firsRect.colliderect(self.secondRect):
            self.colliding = True

        return self.colliding

    def move(self, **kwargs):
        global _windowObject
        dx = 0
        dy = 0
        screen_size = 0
        screen_size = (_windowObject.screen_width, _windowObject.screen_height)
        if self.move_left:
            dx = -self.speed
            self.direction = -1
            self.flip = True
        if self.move_right:
            dx = self.speed
            self.direction = 1
            self.flip = False
        
        # jumping
        if self.jump == True and self.in_air == False:
            self.vel_y = self.jumpHeight
            self.jump = False
            self.in_air = True

        # Applying gravity
        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        for tile in collision_group:
            if tile.rect.colliderect(self.hitbox.x + dx, self.hitbox.y, self.hitbox.width, self.hitbox.height):
                if dx < 0:
                    dx = dx * - 1
                    self.move_left = False
                    self.move_right = True
                elif dx > 0:
                    dx = dx * -1
                    self.move_right = False
                    self.move_left = True
            if tile.rect.colliderect(self.hitbox.x, self.hitbox.y + dy + 1, self.hitbox.width, self.hitbox.height):
                if self.vel_y < 0:
                    if (tile.rect.x != 360 and tile.rect.y != -48) and (tile.rect.x != 456 and tile.rect.y != -24):
                        self.vel_y = 0
                        dy = tile.rect.bottom - self.hitbox.top

                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = 0
                    self.move_left = False
                    self.move_right = False

        if self.hitbox.x + dx < 0:
            if self.vel_y < 10:
                self.move_right = not(self.move_right)
                self.move_left = not(self.move_left)
            else:
                dx = 0

        if self.hitbox.right + dx > screen_size[0]:
            if self.vel_y < 10:
                self.move_right = False
                self.move_left = True
            else:
                dx = 0

        # Collision with the upper part of the window
        if self.hitbox.y + dy < 0:
            dy = 0

        # Collision with bottom of the window
        if self.hitbox.bottom + dy > screen_size[1]:
            dy = 0
            self.vel_y = 0
            self.in_air = False
            self.move_left = False
            self.move_right = False
            self.jumpHeight = -11

        if self.image != None:
            self.x += dx
            self.y += dy
        else:
            self.rect.x += dx
            self.rect.y += dy

    def draw(self, surface=None):
        global _windowObject
        if not(self._hide):
            if surface == None:
                surface = _windowObject.screen
            if self.image != None:
                surface.blit(pygame.transform.flip(self.image, self.horizontal_flip, self.vertical_flip), self.rect)
            else:
                pygame.draw.rect(surface, self.color, self.rect)
            self.hitbox = pygame.Rect(self.rect.x - 1 + (self.hitboxX), self.rect.y - 1 + (self.hitboxY),
                                    (self.width * self.scale) + 2 + (self.hitboxX * -2),
                                    (self.height * self.scale) + 2 + (self.hitboxY * -2))
            if self.showHitbox:
                pygame.draw.rect(surface, (255,0,0), self.hitbox, 2)


particles = []

class Particles():
    def __init__(self, **kwargs):
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.color = kwargs.get("color", (255,255,255))
        self.minSize = kwargs.get("minSize", 3)
        self.maxSize = kwargs.get("maxSize", 6)
        self.speed = kwargs.get("speed", 4)
        self._hide = kwargs.get("hide", False)
        self._hide = kwargs.get("_hide", self._hide)

        particles.append([[self.x, self.y], [random.randint(0, 20) / 10 - 1, self.speed],
                          random.randint(self.minSize, self.maxSize)])

    @property
    def hide(self):
        return self._hide
    
    @hide.setter
    def hide(self, value: bool):
        self._hide = value

    def draw(self, surface=None):
        global _windowObject
        if not(self._hide):
            if surface == None:
                surface = _windowObject.screen
            for particle in particles:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]
                particle[2] -= 0.1
                pygame.draw.circle(surface, (self.color), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
                if particle[2] <= 0:
                    particles.remove(particle)


# Class with the same behavior and functions like Object class
# object is represented as an image that's loaded from spritesheet and can be animated unlike normal Object class
class SpriteSheet(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = pygame.image.load(kwargs['image']).convert_alpha()
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.width = kwargs['width']
        self.height = kwargs['height']
        self.scale = kwargs.get("scale", 1)
        self.animation_list = []
        self.animation_speed0 = 0
        self.animation_speed = 0
        self.animation_steps = self.sheet.get_width() // self.width
        self.animation_frame = 1
        self.health = kwargs.get("health", 100)
        self.move_up = False
        self.move_right = False
        self.move_down = False
        self.move_left = False
        self.showHitbox = kwargs.get("showHitbox", False)
        self.speed = kwargs.get("speed", 4)
        self.gravity = 0.75
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.direction = 1
        self.idle = True
        self.current_frame = 0
        self.hitboxX = kwargs.get("hitboxX", 0)
        self.hitboxY = kwargs.get("hitboxY", 0)
        self._hide = kwargs.get("hide", False)
        self._hide = kwargs.get("_hide", self._hide)

        self.rect = self.sheet.get_rect()
        self.hitbox = pygame.Rect(self.x - 1 + (self.hitboxX), self.y - 1 + (self.hitboxY),
                                  (self.width * self.scale) + 2 + (self.hitboxX * -2),
                                  (self.height * self.scale) + 2 + (self.hitboxY * -2))
    
    @property
    def hide(self):
        return self._hide
    
    @hide.setter
    def hide(self, value: bool):
        self._hide = value

    def get_image(self, frame, color):
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * self.width), 0, self.width, self.height))
        image = pygame.transform.scale(image, (self.width * self.scale, self.height * self.scale))
        image.set_colorkey(color)
        self.rect = image.get_rect()

        return image

    # Reseting animation frame
    def reset_frame(self):
        self.current_frame = 0

    # Moving object
    def move(self, **kwargs):
        global _windowObject
        dx = 0
        dy = 0
        screen_size = 0
        screen_size = (_windowObject.screen_width, _windowObject.screen_height)
        if self.move_left:
            dx = -self.speed
            self.direction = -1
            self.flip = True
        if self.move_right:
            dx = self.speed
            self.direction = 1
            self.flip = False

        # Jumping
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # Applying gravity
        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        for tile in collision_group:
            if tile.rect.colliderect(self.hitbox.x + dx, self.hitbox.y, self.hitbox.width, self.hitbox.height):
                dx = 0
            if tile.rect.colliderect(self.hitbox.x, self.hitbox.y + dy + 1, self.hitbox.width, self.hitbox.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile.rect.bottom - self.hitbox.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = 0

        if self.hitbox.x + dx < 0:
            dx = 0
        if self.hitbox.right + dx > screen_size[0]:
            dx = 0
        if self.hitbox.y + dy < 0:
            dy = 0
        if self.hitbox.bottom + dy > screen_size[1]:
            dy = 0

        self.x += dx
        self.y += dy

    def collision(self, firstRect, secondRect):
        self.colliding = False
        self.firsRect = firstRect
        self.secondRect = secondRect
        if self.firsRect.colliderect(self.secondRect):
            self.colliding = True

        return self.colliding

    def load_image(self):
        for i in range(self.animation_steps):
            self.animation_list.append(self.get_image(i, (255,255,255)))

    # Function for animating image
    def animate(self, **kwargs):
        self.animation_speed0 = kwargs['speed']
        self.startFrame0 = kwargs['startFrame']
        self.startFrame = kwargs['startFrame']
        self.endFrame = kwargs['endFrame']
        if self.animation_speed > 0:
            self.animation_speed -= 1
        elif self.animation_speed <= 0 and self.startFrame0 + self.current_frame < self.endFrame:
            self.current_frame += 1
            self.animation_speed = self.animation_speed0
            self.animation_frame = self.startFrame0 + self.current_frame
        elif self.animation_speed <= 0 and self.startFrame0 + self.current_frame == self.endFrame:
            self.current_frame = 0
            self.animation_frame = self.startFrame0
            self.animation_speed = self.animation_speed0

    def draw(self, surface=None):
        global _windowObject
        if not(self._hide):
            if surface == None:
                surface = _windowObject.screen
            #surface.blit(self.animation_list[self.animation_frame - 1], (self.x, self.y))
            surface.blit(pygame.transform.flip(self.animation_list[self.animation_frame - 1], self.flip, False), (self.x, self.y))
            self.hitbox = pygame.Rect(self.x - 1 + (self.hitboxX), self.y - 1 + (self.hitboxY),
                                    (self.width * self.scale) + 2 + (self.hitboxX * -2),
                                    (self.height * self.scale) + 2 + (self.hitboxY * -2))
            if self.showHitbox:
                pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 1)

class Timer():
    def __init__(self, time, **kwargs):
        self.run = False
        self._time = time * _windowObject.FPS
        self.tick = 0
        self.loops = kwargs.get("loops", None)
        self._iterations = None if self.loops == None else 0

    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, value):
        self._time = value * _windowObject.FPS

    def loop(self):
        done = False
        if self.run:
            if self.tick < self._time:
                self.tick += 1
            else:
                if self._iterations != None:
                    self._iterations +=1
                    if self._iterations <= self.loops:
                        done = True
                elif self._iterations == None:
                    done = True
                else:
                    self.run = False
                self.tick = 0

        return done

    def restart(self):
        if self._iterations != None:
            self._iterations = 0
        self.tick = 0
        self.run = True

    def start(self):
        self.run = True
    
    def stop(self):
        self.run = False

# -=-=-= UNFINISHED -=-=-=#
class CircleProgressBar():
    def __init__(self, **kwargs):
        self.center = (0,0)
        self.thickness = 2
        self.radius = 25
        self.color = (255,255,255)
        self.valueSize = 22
        self.valueColor = (255,255,255)
        self.showValue = True
        self.value = 0
        self.background = (0,0,0)
        self.showBackground = False
        if kwargs.__contains__('center'):
            self.center = kwargs['center']
        if kwargs.__contains__('thickness'):
            self.thickness = kwargs['thickness']
        if kwargs.__contains__('color'):
            self.color = kwargs['color']
        if kwargs.__contains__('radius'):
            self.radius = kwargs['radius']
        if kwargs.__contains__('valueSize'):
            self.valueSize = kwargs['valueSize']
        if kwargs.__contains__('valueColor'):
            self.valueColor = kwargs['valueColor']
        if kwargs.__contains__('value'):
            self.value = kwargs['value']
        if kwargs.__contains__('background'):
            self.background = kwargs['background']
        if kwargs.__contains__('showBackground'):
            self.showBackground = kwargs['showBackground']
        if kwargs.__contains__('showValue'):
            self.showValue = kwargs['showValue']

    def draw(self, surface=None):
        global _windowObject
        if surface == None:
            surface = _windowObject.screen
        if self.showBackground:
            for i in range(0, 360):
                x1 = self.center[0] + self.radius * math.cos(math.radians(i - 90))
                y1 = self.center[1] + self.radius * math.sin(math.radians(i - 90))
                gfxdraw.aacircle(surface, int(x1), int(y1), self.thickness, self.background)
                gfxdraw.filled_circle(surface, int(x1), int(y1), self.thickness, self.background)
        if self.value > 100:
            self.value = 100
        if self.showValue:
            font = pygame.font.SysFont('Arial', self.valueSize)
            img = font.render(str(self.value), True, self.valueColor)
            surface.blit(img, (self.center[0] - (img.get_width() // 2) - 1, self.center[1] - (img.get_height() // 2)))
        for i in range(0, int(self.value * 3.6)):
            x = self.center[0] + self.radius * math.cos(math.radians(i - 90))
            y = self.center[1] + self.radius * math.sin(math.radians(i - 90))
            gfxdraw.aacircle(surface, int(x), int(y), self.thickness, self.color)
            gfxdraw.filled_circle(surface, int(x), int(y), self.thickness, self.color)

class Switch():
    def __init__(self, **kwargs):
        self._x = kwargs.get("x", 0)
        self._x = kwargs.get("_x", self._x)
        self._y = kwargs.get("y", 0)
        self._y = kwargs.get("_y", self._y)
        self._width = kwargs.get("width", 52)
        self._width = kwargs.get("_width", self._width)
        self._height = kwargs.get("height", 22)
        self._height = kwargs.get("_height", self._height)
        self._ballColor = kwargs.get("ballColor", (255,255,255))
        self._ballColor = kwargs.get("_ballColor", self._ballColor)
        self.ballColor0 = self._ballColor
        self.background = kwargs.get("background", (60,60,60))
        self.background0 = self.background
        self.activeBackground = kwargs.get("activeBackground", (75,10,155))
        self.activeBallColor = kwargs.get("activeBallColor", (255,255,255))
        self.active = kwargs.get("active", False)
        self.animation = kwargs.get("animation", True)
        self.disable = kwargs.get("disable", False)
        self.clicked = False
        self.tick = 100
        self._changeCursor = kwargs.get("changeCursor", True)
        self._changeCursor = kwargs.get("_changeCursor", self._changeCursor)
        self.name = kwargs.get("name", None)
        self.z_index = kwargs.get("z_index", None)
        self._hide = kwargs.get("hide", False)
        self._hide = kwargs.get("_hide", self._hide)
        self.clickEvent = None
        self.hoverEvent = None

        self.rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self.ballrect = pygame.Rect(self._x + 3, self._y + 2, self._height - 5, self._height - 5)

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value: int):
        self._x = value
        self.rect.x = value
        if self.active:
            self.ballrect.x = (self._x + self._width) - self.ballrect.width -2
        else:
            self.ballrect.x = self._x + 3

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value: int):
        self._y = value
        self.rect.y = self._y
        self.ballrect.y = self._y + 2

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value: int):
        self._width = value
        self.rect.width = value
        if not(self.active):
            self.ballrect.x = self._x + 3
        else:
            self.ballrect.x = self._x + self.rect.width - (self.ballrect.width*2 - 3)

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value: int):
        self._height = value
        self.rect.height = value
        self.ballrect.height = self._height - 5
        self.ballrect.y = self._y + 3
        
    @property
    def changeCursor(self):
        return self._changeCursor
    
    @changeCursor.setter
    def changeCursor(self, value: bool):
        self._changeCursor = value

    @property
    def ballColor(self):
        return self._ballColor
    
    @ballColor.setter
    def ballColor(self, value: tuple):
        self._ballColor = value
        self.ballColor0 = value

    @property
    def hide(self):
        return self._hide
    
    @hide.setter
    def hide(self, value: bool):
        self._hide = value

    def _has_arguments(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters
        argument_names = [param.name for param in parameters.values()]
        if len(argument_names) > 0:
            return True
        else:
            return False

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def mouse_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                return True
        
    def mouse_hovering(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True

    def draw(self, surface=None):
        global _windowObject, _changingCursor
        if not(self._hide):
            if self.active:
                self.active = True
                self.background0 = self.activeBackground
                self.ballColor0 = self.activeBallColor
            else:
                self.ballColor = self._ballColor
                self.background0 = self.background
            if surface == None:
                surface = _windowObject.screen
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos) or self.ballrect.collidepoint(pos) and not(self.disable):
                if self._changeCursor:
                    _changingCursor = pygame.SYSTEM_CURSOR_HAND
                if self.hoverEvent != None:
                    if self._has_arguments(self.hoverEvent):
                        self.hoverEvent(self)
                    else:
                        self.hoverEvent()
                if pygame.mouse.get_pressed()[0] == 1:
                    if self.clickEvent != None:
                        if self._has_arguments(self.clickEvent):
                            self.clickEvent(self)
                        else:
                            self.clickEvent()
                    self.tick = 100
                    self.clicked = True
            if self.animation:
                if self.active and self.ballrect.x + self.ballrect.width < self._x + self._width - 3:
                    self.ballrect.x += 4
                    if self.ballrect.x + self.ballrect.width > self._x + self._width - 3:
                        self.ballrect.x = (self._x + self._width) - self.ballrect.width -3
                elif not(self.active) and self.ballrect.x > self.x+3:
                    self.ballrect.x -= 4
                    if self.ballrect.x < self._x + 3:
                        self.ballrect.x = self._x + 3
            else:
                if self.active:
                    self.ballrect.x = (self._x + self._width) - self.ballrect.width -2
                else:
                    self.ballrect.x = self._x + 3

            if pygame.mouse.get_pressed()[0] == 0 and not(self.disable):
                if self.rect.collidepoint(pos):
                    if self.clicked:
                        self.clicked = False
                        if self.active:
                            self.active = False
                            self.background0 = self.background
                            self.ballColor0 = self._ballColor
                        else:
                            self.active = True
                            self.background0 = self.activeBackground
                            self.ballColor0 = self.activeBallColor
                else:
                    self.clicked = False

            pygame.draw.rect(surface, self.background0, self.rect, 0, 10)


            gfxdraw.aacircle(surface, self.ballrect.x + (self.ballrect.height // 2), self.ballrect.y + (self.ballrect.height // 2), self.ballrect.height // 2, self.ballColor0)
            gfxdraw.filled_circle(surface, self.ballrect.x + (self.ballrect.height // 2), self.ballrect.y + (self.ballrect.height // 2), self.ballrect.height // 2, self.ballColor0)

# Class for making tile when working with tile maps
class Tile(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.kwargs = kwargs
        self.sign = kwargs.get("sign", None)
        self.group = kwargs.get("group", None)
        self.collision = kwargs.get("collision", False)
        self.image = self.kwargs['image']
        self.name = kwargs.get("name", None)
        self.img = pygame.image.load(kwargs['image']).convert()
        self.rect = self.img.get_rect()
        self.tileSize = kwargs["tileSize"]

        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)

        self.rect.center = (self.x + self.tileSize - self.tileSize // 2, self.y + self.tileSize - self.tileSize // 2)

# Class for creating world that's made out of tiles
class World(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.objects_list = []
        self.game_map = kwargs['map']
        self.TILE_SIZE = kwargs['tileSize']
        self.rects = kwargs.get("rects", [])
        
        self.load_map()

    # Loading an entire map
    def load_map(self):
        y = 0
        for row in self.game_map:
            x = 0
            for tile in row:
                for i in range(len(self.rects)):
                    if tile == self.rects[i].sign:
                        block = Tile(**self.rects[i].__dict__)
                        block.rect.x = x * self.TILE_SIZE
                        block.rect.y = -6048 + (y*self.TILE_SIZE)
                        tile_group.add(block)
                        if self.rects[i].group != None:
                            self.rects[i].group.add(block)
                        if block.collision:
                            collision_group.add(block)
                x += 1
            y += 1

    # Drawing all of the tiles
    def draw(self, surface=None):
        global _windowObject
        if surface == None:
            surface = _windowObject.screen
        for tile in tile_group:
            surface.blit(tile.img, tile.rect)

# Class for creating label (text surface)
class Label():
    def __init__(self, **kwargs):
        global defaultFont
        self._x: int = kwargs.get("x", 0)
        self._x: int = kwargs.get("_x", self._x)
        self._y: int = kwargs.get("y", 0)
        self._y: int = kwargs.get("_y", self._y)
        self._textColor: tuple = kwargs.get("textColor", (255,255,255))
        self._textColor: tuple = kwargs.get("_textColor", self._textColor)
        self._fontName: str = kwargs.get("fontName", defaultFont)
        self._fontName: str = kwargs.get("_fontName", self._fontName)
        self._fontSize: int = kwargs.get("fontSize", 22)
        self._fontSize: int = kwargs.get("_fontSize", self._fontSize)
        self._text: str = kwargs.get("text", "text")
        self._text: str = kwargs.get("_text", self.text)
        self.background: tuple = kwargs.get("background", "transparent")
        self.backgroundWidth: int = kwargs.get("backgroundWidth", 0)
        self.backgroundHeight: int = kwargs.get("backgroundHeight", 0)
        self._charSpacing = kwargs.get("charSpacing", 0)
        self._charSpacing = kwargs.get("_charSpacing", self._charSpacing)
        self._charColor = kwargs.get("charColor", [])
        self._charColor = kwargs.get("_charColor", self._charColor)
        self._charsToDraw = []
        self.charColor = self._charColor
        self.charSpacing = self._charSpacing
        self.name: str = kwargs.get("name", None)
        self.z_index: int = kwargs.get("z_index", None)
        self._hide: bool = kwargs.get("hide", False)
        self._hide: bool = kwargs.get("_hide", self._hide)
        self.clickEvent = None
        self.hoverEvent = None

        if self.fontName[-4:] == ".ttf":
            self.font = pygame.font.Font(self.fontName, self._fontSize)
        else:
            self.font = pygame.font.SysFont(self.fontName, self._fontSize)
        self.img = self.font.render(self._text, True, self._textColor)
        self._tempCharsText = self.img
        self.backgroundRect = pygame.Rect(self._x - (self.backgroundWidth // 2), self._y - (self.backgroundHeight // 2), self.img.get_width() + self.backgroundWidth, self.img.get_height() + self.backgroundHeight)

        self.rect = pygame.Rect(self._x - (self.backgroundWidth // 2), self._y - (self.backgroundHeight // 2), self.img.get_width() + self.backgroundWidth, self.img.get_height() + self.backgroundHeight)

        _allObjects.append(self)
    
    @property
    def charColor(self):
        return self._charColor
    
    @charColor.setter
    def charColor(self, value: list):
        self._charsToDraw.clear()
        self._charColor = value
        font = None
        if self.fontName[-4:] == ".ttf":
            font = pygame.font.Font(self.fontName, self._fontSize)
        else:
            font = pygame.font.SysFont(self.fontName, self._fontSize)
        if len(self._charColor) == 0:
            self.img = font.render(self._text, True, self._textColor)
        else:
            for i, char in enumerate(self._text):
                char_surface = font.render(char, True, self._textColor)
                self._charsToDraw.append(char_surface)
            for index, item in enumerate(self._charsToDraw):
                for i, key in enumerate(self._charColor):
                    char_index = self._charColor[i][0]
                    char_surface = font.render(self._text[char_index], True, self._charColor[i][1])
                    self._charsToDraw[char_index] = char_surface

    @property
    def charSpacing(self):
        return self._charSpacing

    @charSpacing.setter
    def charSpacing(self, value: int):
        self._charSpacing = value
        if self._charColor == [] and self._charSpacing != 0:
            self.charColor = [(index, (self._textColor)) for index, item in enumerate(self._text)]

    def _has_arguments(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters
        argument_names = [param.name for param in parameters.values()]
        if len(argument_names) > 0:
            return True
        else:
            return False

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    # Updating text of label
    def update_text(self, **kwargs):
        self._text = kwargs.get("text", self._text)

        #self.font = pygame.font.SysFont(self.fontName, self.fontSize)

    def mouse_click(self):
        pos = pygame.mouse.get_pos()
        if self.backgroundRect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

    def mouse_hovering(self):
        pos = pygame.mouse.get_pos()
        if self.backgroundRect.collidepoint(pos):
            return True

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self.backgroundRect.x = value
        self.rect.x = self._x - (self.backgroundWidth // 2)

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self.backgroundRect.y = self._y
        self.rect.y = self._y - (self.backgroundHeight // 2)

    @property
    def fontSize(self):
        return self._fontSize
    
    @fontSize.setter
    def fontSize(self, value):
        self._fontSize = value
        if self.fontName[-4:] == ".ttf":
            self.font = pygame.font.Font(self.fontName, self._fontSize)
        else:
            self.font = pygame.font.SysFont(self.fontName, self._fontSize)
        self.img = self.font.render(self._text, True, self._textColor)
        self.backgroundRect.width, self.backgroundRect.height = self.img.get_width() + self.backgroundWidth, self.img.get_height() + self.backgroundHeight
        self.rect.width, self.rect.height = self.img.get_width() + self.backgroundWidth, self.img.get_height() + self.backgroundHeight

    @property
    def fontName(self):
        return self._fontName
    
    @fontName.setter
    def fontName(self, value):
        self._fontName = value
        try:
            if self.fontName[-4:] == ".ttf":
                self.font = pygame.font.Font(self.fontName, self._fontSize)
            else:
                self.font = pygame.font.SysFont(self.fontName, self._fontSize)
        except:
            self._fontName = defaultFont
            if self.fontName[-4:] == ".ttf":
                self.font = pygame.font.Font(self.fontName, self._fontSize)
            else:
                self.font = pygame.font.SysFont(self.fontName, self._fontSize)
        self.img = self.font.render(self._text, True, self._textColor)
        self.backgroundRect = pygame.Rect(self._x - (self.backgroundWidth // 2), self._y - (self.backgroundHeight // 2), self.img.get_width() + self.backgroundWidth, self.img.get_height() + self.backgroundHeight)
        self.rect.width, self.rect.height = self.img.get_width() + self.backgroundWidth, self.img.get_height() + self.backgroundHeight

    @property
    def textColor(self):
        return self._textColor
    
    @textColor.setter
    def textColor(self, value):
        self._textColor = value
        self.img = self.font.render(self._text, True, self._textColor)

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
        self.img = self.font.render(self._text, True, self._textColor)
        self.backgroundRect.x, self.backgroundRect.y, self.backgroundRect.width, self.backgroundRect.height = self.x - (self.backgroundWidth // 2), self._y - (self.backgroundHeight // 2), self.img.get_width() + self.backgroundWidth, self.img.get_height() + self.backgroundHeight
        self.rect = pygame.Rect(self._x - (self.backgroundWidth // 2), self._y - (self.backgroundHeight // 2), self.img.get_width() + self.backgroundWidth, self.img.get_height() + self.backgroundHeight)
        self.charColor = self._charColor

    @property
    def hide(self):
        return self._hide
    
    @hide.setter
    def hide(self, value: bool):
        self._hide = value
    
    def draw(self, surface=None):
        global _windowObject
        pos = pygame.mouse.get_pos()
        if self.backgroundRect.collidepoint(pos):
            if self.hoverEvent != None:
                if self._has_arguments(self.hoverEvent):
                    self.hoverEvent(self)
                else:
                    self.hoverEvent()
            if pygame.mouse.get_pressed()[0] == 1:
                if self.clickEvent != None:
                    if self._has_arguments(self.clickEvent):
                        self.clickEvent(self)
                    else:
                        self.clickEvent()
        if not(self._hide):
            if surface == None:
                surface = _windowObject.screen
            if self.background != "transparent":
                self.backgroundRect.x, self.backgroundRect.y = self.x - (self.backgroundWidth // 2), self._y - (self.backgroundHeight // 2)
                pygame.draw.rect(surface, self.background, self.backgroundRect)
            if self._charColor == [] and self._charSpacing == 0:
                surface.blit(self.img, (self._x, self._y))
            else:
                x = self._x
                for index, item in enumerate(self._charsToDraw):
                    surface.blit(self._charsToDraw[index], (x, self._y))
                    x += (self.font.size(self._text[index])[0])+self._charSpacing

class DropDownMenu():
    def __init__(self, **kwargs):
        global _windowObject
        self._x = kwargs.get("x", 0)
        self._x = kwargs.get("_x", self._x)
        self._y = kwargs.get("y", 0)
        self._y = kwargs.get("_y", self._y)
        self._width = kwargs.get("width", 0)
        self._width = kwargs.get("_width", self._width)
        self._height = kwargs.get("height", 0)
        self._height = kwargs.get("_height", self._height)
        self._background = kwargs.get("background", (50,50,50))
        self._background = kwargs.get("_background", self._background)
        self._outlineWidth = kwargs.get("outlineWidth", 0)
        self._outlineWidth = kwargs.get("_outlineWidth", self._outlineWidth)
        self._hoverBackground = kwargs.get("hoverBackground", (80,80,80))
        self._hoverBackground = kwargs.get("_hoverBackground", self._hoverBackground)
        self._outlineColor = kwargs.get("outlineColor", self._background)
        self._outlineColor = kwargs.get("_outlineColor", self._outlineColor)
        self._activeBackground = kwargs.get("activeBackground", self._hoverBackground)
        self._activeBackground = kwargs.get("_activeBackground", self._activeBackground)
        self._hoverOutlineColor = kwargs.get("hoverOutlineColor", self._hoverBackground)
        self._hoverOutlineColor = kwargs.get("_hoverOutlineColor", self._hoverOutlineColor)
        self._activeOutlineColor = kwargs.get("activeOutlineColor", self._hoverOutlineColor)
        self._activeOutlineColor = kwargs.get("_activeOutlineColor", self._activeOutlineColor)
        self._borderRadius = kwargs.get("borderRadius", 0)
        self._borderRadius = kwargs.get("_borderRadius", self._borderRadius)
        self._changeCursor = kwargs.get("changeCursor", True)
        self._changeCursor = kwargs.get("_changeCursor", self._changeCursor)
        self._fontName = kwargs.get("fontName", defaultFont)
        self._fontName = kwargs.get("_fontName", self._fontName)
        self._fontSize = kwargs.get("fontSize", 14)
        self._fontSize = kwargs.get("_fontSize", self._fontSize)
        self._textColor = kwargs.get("textColor", (255,255,255))
        self._textColor = kwargs.get("_textColor", self._textColor)
        self._hoverTextColor= kwargs.get("hoverTextColor", self._textColor)
        self._hoverTextColor = kwargs.get("_hoverTextColor", self._hoverTextColor)
        self._activeTextColor= kwargs.get("activeTextColor", self._hoverTextColor)
        self._activeTextColor = kwargs.get("_activeTextColor", self._activeTextColor)
        self.textPosition = kwargs.get("textPosition", "center")
        self._offsetY = kwargs.get("offsetY", 0)
        self._offsetY = kwargs.get("_offsetY", self._offsetY)
        self._offsetX = kwargs.get("offsetX", 0)
        self._offsetX = kwargs.get("_offsetX", self._offsetX)
        self.textOffsetX = kwargs.get("textOffsetX", 0)
        self.textOffsetY = kwargs.get("textOffsetY", 0)

        self.name = kwargs.get("name", None)
        self._hide = kwargs.get("hide", False)
        self._hide = kwargs.get("_hide", self._hide)
        self.z_index = kwargs.get("z_index", None)

        self._active = False

        self._text = kwargs.get("text", "Drop down")
        self._text = kwargs.get("_text", self._text)
        self._option1 = kwargs.get("option1", "option 1")
        self._option1 = kwargs.get("_option1", self._option1)

        optionsCount = 0
        self._optionButtons = []

        y = self._y
        if self.borderRadius > 0:
            y += 4
        for index, item in enumerate(kwargs):
            if item == f"option{index+1}":
                optionsCount += 1
                buttonText = kwargs[item]
                if isinstance(kwargs.get(f"option{index+1}"), list):
                    buttonText = kwargs[item][0]

                button = Button(text=buttonText, x=self._x, y=y, width=self._width, height=self._height,
                             background=self._background, hoverBackground=self._hoverBackground, activeBackground=self._activeBackground,
                             outlineWidth=self._outlineWidth, outlineColor=self._outlineColor, hoverOutlineColor=self._hoverOutlineColor,
                             activeOutlineColor=self._activeOutlineColor, textColor=self._textColor, hoverTextColor=self._hoverTextColor,
                             fontSize=self._fontSize, fontName=self._fontName, changeCursor=self._changeCursor, autoResizing=False, textPosition=self.textPosition,
                             textOffsetX=self.textOffsetX, textOffsetY=self.textOffsetY)
                y += button.rect.height+self._outlineWidth
                if isinstance(kwargs.get(f"option{index+1}"), list) and len(kwargs[item]) > 1:
                    self._optionButtons.append([button, kwargs[item][1]])
                else:
                    self._optionButtons.append([button, None])

    @property
    def active(self):
        return self._active
    
    @active.setter
    def active(self, value: bool):
        self._active = value
        y = self._y+self._outlineWidth+self._offsetY
        x = self._x+self._outlineWidth+self._offsetX
        if self.borderRadius > 0:
            y += 4
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].y = y
            self._optionButtons[index][0].x = x
            y += self._optionButtons[index][0].rect.height

    @property
    def borderRadius(self):
        return self._borderRadius
    
    @borderRadius.setter
    def borderRadius(self, value: int):
        self._borderRadius = value

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, value: tuple):
        self._background = value
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].background = value

    @property
    def hoverBackground(self):
        return self._hoverBackground

    @hoverBackground.setter
    def hoverBackground(self, value: tuple):
        self._hoverBackground = value
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].hoverBackground = value

    @property
    def activeBackground(self):
        return self._activeBackground

    @activeBackground.setter
    def activeBackground(self, value: tuple):
        self._activeBackground = value
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].activeBackground = value

    @property
    def outlineWidth(self):
        return self._outlineWidth

    @outlineWidth.setter
    def outlineWidth(self, value: int):
        self._outlineWidth = value
        y = self._y+self._outlineWidth+self._offsetY
        if self.borderRadius > 0:
            y += 4
        self.x = self.x+self._offsetX
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].outlineWidth = value
            self._optionButtons[index][0].y = y
            y += self._optionButtons[index][0].rect.height

    @property
    def outlineColor(self):
        return self._outlineColor

    @outlineColor.setter
    def outlineColor(self, value: tuple):
        self._outlineColor = value
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].outlineColor = value

    @property
    def hoverOutlineColor(self):
        return self._hoverOutlineColor

    @hoverOutlineColor.setter
    def hoverOutlineColor(self, value: tuple):
        self._hoverOutlineColor = value
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].hoverOutlineColor = value

    @property
    def activeOutlineColor(self):
        return self._activeOutlineColor

    @activeOutlineColor.setter
    def activeOutlineColor(self, value: tuple):
        self._activeOutlineColor = value
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].activeOutlineColor = value

    @property
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, value: tuple):
        self._textColor = value
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].textColor = value

    @property
    def hoverTextColor(self):
        return self._hoverTextColor

    @hoverTextColor.setter
    def hoverTextColor(self, value: tuple):
        self._hoverTextColor = value
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].hoverTextColor = value

    @property
    def activeTextColor(self):
        return self._activeTextColor

    @activeTextColor.setter
    def activeTextColor(self, value: tuple):
        self._activeTextColor = value
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].activeTextColor = value

    @property
    def fontSize(self):
        return self._fontSize

    @fontSize.setter
    def fontSize(self, value: tuple):
        self._fontSize = value
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].fontSize = value

    @property
    def fontName(self):
        return self._fontName

    @fontName.setter
    def fontName(self, value: tuple):
        self._fontName = value
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].fontName = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: tuple):
        self._x = value+self._outlineWidth+self._offsetX
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: tuple):
        self._y = value
        y = self._y+self._outlineWidth+self._offsetY
        if self.borderRadius > 0:
            y += 4
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].y = y
            y += self._optionButtons[index][0].rect.height

    @property
    def changeCursor(self):
        return self._changeCursor

    @changeCursor.setter
    def changeCursor(self, value: tuple):
        self._changeCursor = value
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].changeCursor = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: tuple):
        self._width = value
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: tuple):
        self._height = value
        y = self._y+self._outlineWidth+self._offsetY
        if self.borderRadius > 0:
            y += 4
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].height = value
            self._optionButtons[index][0].y = y
            y += self._optionButtons[index][0].rect.height

    @property
    def offsetY(self):
        return self._offsetY
    
    @offsetY.setter
    def offsetY(self, value: int):
        self._offsetY = value
        y = value+self._outlineWidth+self._offsetY
        if self.borderRadius > 0:
            y += 4
        
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].y = y
            y += self._optionButtons[index][0].rect.height

    @property
    def offsetX(self):
        return self._offsetX
    
    @offsetX.setter
    def offsetX(self, value: int):
        self._offsetX = value
        x = value+self._outlineWidth+self._offsetX
        for index, item in enumerate(self._optionButtons):
            self._optionButtons[index][0].x = x
            x += self._optionButtons[index][0].rect.width

    def draw(self, surface=None):
        if surface == None:
            surface = _windowObject.screen

        if not(self._hide) and self.active:

            if self.borderRadius > 0:
                x = (self.x-4)+self.offsetX
                y = (self.y-4)+self.offsetY
                width = self.width + 8
                height = 0
                for index, item in enumerate(self._optionButtons):
                    height += self._optionButtons[index][0].rect.height
                height += 16

                gfxdraw.aacircle(surface, x + self.borderRadius, y + self.borderRadius, self.borderRadius, self.background)
                gfxdraw.filled_circle(surface, x + self.borderRadius, y + self.borderRadius, self.borderRadius, self.background)
                gfxdraw.aacircle(surface, x + width - self.borderRadius, y + self.borderRadius, self.borderRadius, self.background)
                gfxdraw.filled_circle(surface, x + width - self.borderRadius, y + self.borderRadius, self.borderRadius, self.background)
                gfxdraw.aacircle(surface, x + self.borderRadius, y + height - self.borderRadius-1, self.borderRadius, self.background)
                gfxdraw.filled_circle(surface, x + self.borderRadius, y + height - self.borderRadius-1, self.borderRadius, self.background)
                gfxdraw.aacircle(surface, x + width - self.borderRadius, y + height - self.borderRadius-1, self.borderRadius, self.background)
                gfxdraw.filled_circle(surface, x + width - self.borderRadius, y + height - self.borderRadius-1, self.borderRadius, self.background)

                pygame.draw.rect(surface, self.background, (x + self.borderRadius, y, (width+2) - 2 * self.borderRadius, height))
                pygame.draw.rect(surface, self.background, (x, y + self.borderRadius, (width+2), height - 2 * self.borderRadius))

            for index, item in enumerate(self._optionButtons):
                if self._optionButtons[index][0].draw():
                    if self._optionButtons[index][1] != None and callable(self._optionButtons[index][1]):
                        self._optionButtons[index][1]()
                        self.active = False
        

# Detecting key press event (just one press of the key)
class GetKeyPress():
    def __init__(self):
        self.tick = 0
        self.clicked = False

    def GetPressed(self, key):
        keys = pygame.key.get_pressed()
        if keys[key]:
            if not(self.clicked):
                self.clicked = True
                return True
        else:
            self.clicked = False

# Detecting holding key event
def GetHoldingKey(key):
    keys = pygame.key.get_pressed()
    if keys[key]:
        return True

# Detecting mouse click event (just one click)
def MouseButtonDown(button):
    if pygame.mouse.get_pressed()[button] == 1:
        return True

# Function for generating rundom numbers (currently integers only)
def Random(firstNumber, secondNumber, exceptionNumbers=None):
    number = None
    while number == None:
        tempNum = random.randint(firstNumber, secondNumber)
        if exceptionNumbers:
            if exceptionNumbers.__contains__(tempNum):
                continue
            else:
                number = tempNum
        else:
            number=tempNum

    return number

# Printing all of the fonts
def PrintFonts():
    fonts = pygame.font.get_fonts()
    fonts_list = [defaultFont]
    for font in fonts:
        fonts_list.append(font)
    print(fonts_list)

# Function for moving object to the specified point in the window
def MoveToPoint(obj, point, speed):
    dx = point[0] - obj.x
    dy = point[1] - obj.y
    distance = math.hypot(dx, dy)
    if distance != 0:
        if distance < speed:
            obj.x = point[0]
            obj.y = point[1]
        else:
            t = speed / distance
            t = min(t, 1.0)
            obj.x += dx * t
            obj.y += dy * t

    if obj.x == point[0] and obj.y == point[1]:
        return True

# Function for reading .txt files
def ReadTxtFile(file, **kwargs):
    listFormat = kwargs.get("list", False)
    ignoreBlankLines = kwargs.get("ignoreBlankLines", False)
    file_content = None

    if os.path.exists(file):
        with open(file, 'r') as f:
            if not(listFormat):
                file_content = f.read()
            else:
                lines = f.readlines()
                file_content = []
                for line in lines:
                    if ignoreBlankLines and line.strip() == "":
                        pass
                    else:
                        file_content.append(line.strip()) 

        return file_content
    
    else:
        pass

# Function for writing text to .txt file
def WriteToTxtFile(file, text, line=-1, overwrite=True, addLineBelow=False):
    with open(file, 'r') as f:
        lines = f.readlines()

    if line == 0:
        line = len(lines)+2
    elif line <= 0:
        line = len(lines)+2 + abs(line)

    if line <= len(lines):
        if overwrite:
            lines[line - 1] = text + '\n'
        else:
            lines[line - 1] = lines[line - 1].rstrip('\n') + text + '\n'
        if addLineBelow:
            lines.insert(line, "\n")
    else:
        lines.extend(['\n'] * (line - len(lines)-1))
        lines.append(text + '\n')

    with open(file, 'w') as f:
        f.writelines(lines)

# Accessing text from .txt file
def GetLineFromTxtFile(file, line):
    if os.path.exists(file):
        line_number = line
        if line != -1:
            line_number = line+1
        else:
            line_number = len(linecache_getlines(file))

        line = linecache_getline(file, line_number)

        if line:
            return line.strip()
    else:
        pass

# Moving folder to specified directory (name of the moving folder can be changed)
def MoveFolder(folder_path, target_dir):
    try:
        os.makedirs(target_dir, exist_ok=True)

        for item in os.listdir(folder_path):
            source_item = os.path.join(folder_path, item)
            destination_item = os.path.join(target_dir, item)

            if os.path.isdir(source_item):
                MoveFolder(source_item, destination_item)
            else:
                os.rename(source_item, destination_item)

        os.rmdir(folder_path)
    except:
        pass

# Moving file to specified directory (name of the moving file can be changed)
def MoveFile(file_path, target_dir):
    try:
        os.rename(file_path, target_dir)
    except:
        pass

# Deleting folder with all it's files
def DeleteFolder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                DeleteFolder(file_path)
        
        os.rmdir(folder_path)
    else:
        pass

def OwerwriteFile(src_file, dest_file):
    with open(src_file, 'r') as src:
        content = src.read()

    with open(dest_file, 'w') as dest:
        dest.write(content)

    # Delete the original file if needed
    os.remove(src_file)

# Function for reading JSON file
def ReadJSONFile(json_file: str, keyName=None, elementIndex=0, elementName=None):
    if os.path.exists(json_file):
        if json_file[-5:] == ".json":
            with open(json_file, 'r') as jfile:
                data = json.load(jfile)
                if keyName != None and elementName != None:
                    return data[keyName][elementIndex][elementName]
                else:
                    return data

# Creating file
def CreateFile(file, overwrite: bool=False):
    if not(overwrite):
        if not(os.path.exists(file)):
            with open(file, 'w') as f:
                pass
    else:
        with open(file, 'w') as f:
            pass

def CopyFile(source_file, destination_file):
    if os.path.exists(source_file):
        shutil.copy(source_file, destination_file)
    else:
        print(f"Pynite: Pynite.CopyFile() ERROR: -> path: {source_file} does not exists")

def CopyFolder(src, dest):
    shutil.copytree(src, dest)

def get_display_size(**kwargs) -> tuple:
    ignoreTaskBar = kwargs.get("ignoreTaskBar", False)
    display_size = None

    platfromOS = platform.system()

    # Windows
    if platfromOS == "Windows":
        if ignoreTaskBar:
            display_size = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(17))
        else:
            display_size = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))

    # Linux
    elif platfromOS == "Linux":
        output = subprocess.check_output(['xdpyinfo']).decode('utf-8')
        for line in output.split('\n'):
            if 'dimensions:' in line:
                size_str = line.split(' ')[-1]
                width, height = map(int, size_str.split('x'))
                display_size = (width, height)
    
    # Unsupported platform
    else:
        display_size = (0, 0)


    return display_size

# Class for music player (multiple songs can be played) (.mp3 and .wav only)
class Music():
    def __init__(self):
        self.musicsList = []
        self._allMusics = []
        self.cahnnelsList = []
        self.currentMusic = None
        self.lengthList = []

    def play(self, music, volume=1):
        volume = volume * 0.01
        if not(self.musicsList.__contains__(music)):
            self.musicsList.append(pygame.mixer.Sound(music))
            self._allMusics.append(music)
            index = len(self.musicsList)-1
            self.cahnnelsList.append(pygame.mixer.Channel(len(self.cahnnelsList)+1))
            self.cahnnelsList[len(self.cahnnelsList)-1].play(self.musicsList[index])
            self.cahnnelsList[len(self.cahnnelsList)-1].set_volume(volume)
            self.currentMusic = music

    # Checking if music is playing
    def is_playing(self, music):
        if self._allMusics.__contains__(music):
            index = self._allMusics.index(music)
            if self.cahnnelsList[index].get_busy():
                return True
            else:
                return False

    # Getting length of song
    def lenght(self, music):
        if music[-4:] == ".mp3":
            audio = MP3(music)
            song_length = audio.info.length
            return song_length
        else:
            return None
    
    def unpause(self, music):
        if self._allMusics.__contains__(music):
            index = self._allMusics.index(music)
            self.cahnnelsList[index].unpause()

    def pause(self, music):
        if self._allMusics.__contains__(music):
            index = self._allMusics.index(music)
            self.cahnnelsList[index].pause()

    def stop(self, music):
        if self._allMusics.__contains__(music):
            index = self._allMusics.index(music)
            self.cahnnelsList[index].stop()
            self.cahnnelsList.pop(index)
            self.musicsList.pop(index)
    
    # Reseting all the songs that have been added to the music player
    def reset(self):
        for channel in self.cahnnelsList:
            channel.stop()
        self.currentMusic = None
        self._allMusics = []
        self.musicsList = []
        self.cahnnelsList = []

class TextBox2(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        global defaultFont, _textBoxList, _windowObject, _allObjects
        pygame.sprite.Sprite.__init__(self)
        self.maxCharacters = abs(kwargs.get("maxCharacters", 999999))
        self.numbersOnly = kwargs.get("numbersOnly", False)
        self.lettersOnly = kwargs.get("lettersOnly", False)
        self.exceptionChars = kwargs.get("exceptionChars", [])
        self._x = kwargs.get("x", 0)
        self._y = kwargs.get("y", 0)
        self._x = kwargs.get("_x", self._x)
        self._y = kwargs.get("_y", self._y)
        self._width = kwargs.get("width", 0)
        self._width = kwargs.get("_width", self._width)
        self._height = kwargs.get("height", 0)
        self._height = kwargs.get("_height", self._height)
        self.FPS = _windowObject.FPS
        self._text = kwargs.get("text", "Text")
        self._text = kwargs.get("_text", self._text)
        self._textColor = kwargs.get("textColor", (220,220,220))
        self._textColor = kwargs.get("_textColor", self._textColor)
        self.textColor0 = self._textColor
        self.placeholderColor = kwargs.get("placeholderColor", (160,160,160))
        self._outlineColor = kwargs.get("outlineColor", (130,130,130))
        self._outlineColor = kwargs.get("_outlineColor", self._outlineColor)
        self.outlineColor0 = self._outlineColor
        self.hoverOutlineColor = kwargs.get("hoverOutlineColor", (130,130,130))
        self.activeOutlineColor = kwargs.get("activeOutlineColor", (225,225,225))
        self.outlineWidth = kwargs.get("outlineWidth", 0)
        self.highlightColor = kwargs.get("highlightColor", (0,100,255))
        self.textPosition = kwargs.get("textPosition", "left")
        self._background = kwargs.get("background", (60,60,60))
        self._background = kwargs.get("_background", self._background)
        self.background0 = self._background
        self.activeBackground = kwargs.get("activeBackground", (90,90,90))
        self.bold = kwargs.get("bold", False)
        self.borderRadius = kwargs.get("borderRadius", 0)
        self._placeholderText = kwargs.get("placeholderText", "Text")
        self._placeholderText = kwargs.get("_placeholderText", self._placeholderText)
        self._changeCursor = kwargs.get("changeCursor", True)
        self._changeCursor = kwargs.get("_changeCursor", self._changeCursor)
        self._fontSize = kwargs.get("fontSize", 26)
        self._fontSize = kwargs.get("_fontSize", self._fontSize)
        self._fontName = kwargs.get("fontName", defaultFont)
        self._fontName = kwargs.get("_fontName", self._fontName)
        self.cursorColor = kwargs.get("cursorColor", (175,175,175))
        self.showOutline = kwargs.get("showOutline", False)
        self.name = kwargs.get("name", None)
        self.disable = kwargs.get("disable", False)
        self.z_index = kwargs.get("z_index", None)
        self.acceptedFormat = kwargs.get("acceptedFormat", None)
        self._hide = kwargs.get("hide", False)
        self._hide = kwargs.get("_hide", self._hide)
        self.clickEvent = None
        self.hoverEvent = None

        if self._text == "":
            self._text = self._placeholderText
        
        self.active = False
        self.clicked = False
        self.clickedOutside = False
        self.showCursor = True
        self.currentLetter = len(self._text)
        self.textPosX = 2
        self.highlightedLetter = 0
        self.highlightedFirstLetter = 0
        self.highlightedLettersRight = 0
        self.highlightedLettersLeft = 0
        self.highlighted = False
        self.holdingShift = False
        self.holdingBackspace = False
        self.holdingArrow = False
        self.holdingLeftArrow = False
        self.holdingRightArrow = False

        self.mouseTimesClicked = 0
        self.mouseClickedTick = 0
        self.mouseClicked = False

        self.mouseClickPosition = 0
        self.mouseHighlightedDirection = None

        self.ctrlA = KeyBindCombination(key1=pygame.K_LCTRL, key2=pygame.K_a)
        self.ctrlV = KeyBindCombination(key1=pygame.K_LCTRL, key2=pygame.K_v)
        self.ctrlC = KeyBindCombination(key1=pygame.K_LCTRL, key2=pygame.K_c)
        self.ctrlX = KeyBindCombination(key1=pygame.K_LCTRL, key2=pygame.K_x)

        self.cursorTimer = Timer(time=0.50)
        self.cursorTimer.start()

        self.arrowHoldingTick = 0
        self.backspaceHoldingTick = 0

        self.backspaceTimer = Timer(time=0.025)
        self.arrowTimer = Timer(time=0.040)

        self.clock = pygame.time.Clock()
        if self._fontName[-4:] == ".ttf":
            self.font = pygame.font.Font(self._fontName, self._fontSize)
        else:
            self.font = pygame.font.SysFont(self._fontName, self._fontSize, bold=self.bold)
        self.text_surface = self.font.render(self._text, True, (self.textColor0))

        self.textSurface = pygame.Surface((self._width - 4, self.text_surface.get_height()), pygame.SRCALPHA)
        self.cursorIBEAM = pygame.Surface((2, self.textSurface.get_height()))
        self.rect = pygame.Rect(self._x, self._y, self._width, self._height+self.text_surface.get_height())

        self.cursorIBEAMX = self.font.size(self._text)[0]

        _textBoxList.append(self)
        _allObjects.append(self)
    
    def clear_text(self):
        self._text = ""
        self.currentLetter = 0
        self.textPosX = 2

    def mouse_click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

    def mouse_hovering(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = value

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = self._y

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
        self.currentLetter = 0

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, value: tuple):
        self._background = value
        self.background0 = value

    @property
    def textColor(self):
        return self._textColor
    
    @textColor.setter
    def textColor(self, value):
        self._textColor = value
        self.textColor0 = value
        self.text_surface = self.font.render(self._text, True, self._textColor)

    @property
    def outlineColor(self):
        return self._outlineColor
    
    @outlineColor.setter
    def outlineColor(self, value: tuple):
        self._outlineColor = value
        self.outlineColor0 = value

    @property
    def fontSize(self):
        return self._fontSize
    
    @fontSize.setter
    def fontSize(self, value: int):
        self._fontSize = value
        if self._fontName[-4:] == ".ttf":
            self.font = pygame.font.Font(self._fontName, self._fontSize)
        else:
            self.font = pygame.font.SysFont(self._fontName, self._fontSize, bold=self.bold)
        self.text_surface = self.font.render(self._text, True, (self.textColor0))
        self.textSurface = pygame.Surface((self._width - 4, self.text_surface.get_height()), pygame.SRCALPHA)
        self.cursorIBEAM = pygame.Surface((2, self.textSurface.get_height()))
        self.rect.width, self.rect.height = self._width, self._height + self.text_surface.get_height()

    @property
    def fontName(self):
        return self._fontName
    
    @fontName.setter
    def fontName(self, value: str):
        self._fontName = value
        if self._fontName[-4:] == ".ttf":
            self.font = pygame.font.Font(self._fontName, self._fontSize)
        else:
            self.font = pygame.font.SysFont(self._fontName, self._fontSize, bold=self.bold)
        self.text_surface = self.font.render(self._text, True, (self.textColor0))
        self.textSurface = pygame.Surface((self._width - 4, self.text_surface.get_height()), pygame.SRCALPHA)
        self.cursorIBEAM = pygame.Surface((2, self.textSurface.get_height()))
        self.rect.width, self.rect.height = self._width, self._height + self.text_surface.get_height()

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value: int):
        self._width = value
        self.rect.width = self._width

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value: int):
        self._height = value
        self.rect.height = self._height+self.text_surface.get_height()

    @property
    def changeCursor(self):
        return self._changeCursor

    @changeCursor.setter
    def changeCursor(self, value: bool):
        self._changeCursor = value

    @property
    def placeholderText(self):
        return self._placeholderText
    
    @placeholderText.setter
    def placeholderText(self, value):
        self._placeholderText = value
        self._text = value

    @property
    def hide(self):
        return self._hide
    
    @hide.setter
    def hide(self, value: bool):
        self._hide = value

    def _has_arguments(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters
        argument_names = [param.name for param in parameters.values()]
        if len(argument_names) > 0:
            return True
        else:
            return False

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def get_enter_press(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] and self.active:
            self.active = False
            self.background0 = self._background
            self.outlineColor0 = self._outlineColor
            return True

    def __delete_text(self):
        # Deleting text that's highlighted to the right
        if (self.highlightedLettersRight > 0 and (self.highlightedFirstLetter > 0 and self.highlightedLettersRight < len(self._text)) and self.currentLetter > 0) or (self.highlightedFirstLetter == 0 and self.highlightedLettersRight > 0 and self.highlighted) and self.highlighted:
            self._text = self._text[:self.highlightedFirstLetter] + self._text[self.highlightedLetter+1:]
            self.currentLetter -= self.highlightedLettersRight
            self.highlightedLettersRight = 0
            self.highlighted = False
            self.highlightedLetter = 0
            self.highlightedFirstLetter = 0

        # # Deleting text that's highlighted to the left
        elif self.highlightedLettersLeft > 0 and self.highlightedLettersLeft < len(self._text) and self.currentLetter >= 0 and self.highlighted:
            self._text = self._text[:self.highlightedLetter] + self._text[self.highlightedFirstLetter+1:]
            self.highlightedLettersLeft = 0
            self.highlighted = False
            self.highlightedLetter = 0
            self.highlightedFirstLetter = 0

        elif (self.highlightedFirstLetter == 0 and self.highlightedLetter == len(self._text)) or (self.highlightedFirstLetter+1 == len(self._text) and self.currentLetter == 0) or (self.highlightedFirstLetter == 0 and self.highlightedLetter+1 == len(self._text) and self.highlighted):
            self._text = ""
            self.currentLetter = 0
            self.highlightedLettersRight = 0
            self.highlightedLettersLeft = 0
            self.highlighted = False
            self.highlightedLetter = 0
            self.highlightedFirstLetter = 0
            self.textPosX = 2

    def _update(self, event):
        if not(self._hide):
            # Text input event
            if event.type == pygame.TEXTINPUT and self.active and len(self._text) < self.maxCharacters:
                char = event.text
                if (char.isdigit() or self.exceptionChars.__contains__(char)) and self.numbersOnly and not(self.lettersOnly):
                    self.__delete_text()
                    self._text = self._text[:self.currentLetter] + char + self._text[self.currentLetter:]
                    self.currentLetter += 1
                    self.cursorTimer.tick = 0
                    self.showCursor = True
                elif char.isdigit() and self.lettersOnly and not(self.numbersOnly):
                    pass
                elif (not(char.isdigit() or self.exceptionChars.__contains__(char)) and self.lettersOnly) and not(self.numbersOnly):
                    self.__delete_text()
                    self._text = self._text[:self.currentLetter] + char + self._text[self.currentLetter:]
                    self.currentLetter += 1         
                    self.cursorTimer.tick = 0
                    self.showCursor = True
                else:
                    if not(self.lettersOnly) and not(self.numbersOnly):
                        self.__delete_text()
                        self._text = self._text[:self.currentLetter] + char + self._text[self.currentLetter:]
                        self.currentLetter += 1
                        self.cursorTimer.tick = 0
                        self.showCursor = True

                # Moving whole text to the left when it's too long to fit in the box
                if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosX) + 6 > (self._width - 3):
                    self.textPosX -= ((self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosX) + 6) - (self._width - 3))
                    if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosX) == (self._width - 9):
                        self.textPosX += 4

            # Deleting text by clicking BACKSPACE
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE and self._text != "":
                    self.holdingBackspace = True
                    
                    self.cursorTimer.tick = 0

                    # Deleting one character per click from text when nothing is highlighted
                    if not(self.highlighted) and self.currentLetter > 0:
                        self.currentLetter -= 1
                        self._text = self._text[:self.currentLetter] + self._text[self.currentLetter+1:]
                    else:
                        self.__delete_text()

                    # Moving whole text to the right when it's too long to fit in the box
                    if self.textPosX < 2:
                        widthDiff = self.font.size(self._text[0:self.currentLetter])[0]
                        self.textPosX = (self._width - 3) - widthDiff - 2
                        if self.textPosX > 2:
                            self.textPosX = 2      

                if event.key == pygame.K_RIGHT and self.currentLetter < len(self._text):
                    self.holdingRightArrow = True
                    self.holdingLeftArrow = False
                    self.currentLetter += 1
                    if self.holdingShift:
                        if self.highlightedFirstLetter == 0 and self.highlightedLettersRight == 0  and self.highlightedLettersLeft == 0:
                            self.highlightedFirstLetter = self.currentLetter-1
                        if self.highlightedLettersLeft <= 0:
                            self.highlightedLetter = self.currentLetter-1
                            self.highlightedLettersRight += 1
                        else:
                            self.highlightedLettersLeft -= 1
                            self.highlightedLetter += 1
                            if self.highlightedLettersLeft <= 0:
                                self.highlightedLetter = 0
                                self.highlightedFirstLetter = 0

                    # Moving whole text to the left when it's too long to fit in the box
                    if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosX) + 6 > self._width - 3:
                        self.textPosX -= (self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosX) + 6) - (self._width - 3)
                        if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosX) == (self._width - 9):
                            self.textPosX += 4

                if event.key == pygame.K_LEFT and self.currentLetter > 0:
                    self.holdingLeftArrow = True
                    self.holdingRightArrow = False
                    self.currentLetter -= 1
                    if self.holdingShift:
                        if self.highlightedFirstLetter == 0 and self.highlightedLettersLeft == 0 and self.highlightedLettersRight == 0:
                            self.highlightedFirstLetter = self.currentLetter
                        if self.highlightedLettersRight <= 0:
                            self.highlightedLetter = self.currentLetter
                            self.highlightedLettersLeft += 1
                        else:
                            self.highlightedLettersRight -= 1
                            self.highlightedLetter -= 1
                            if self.highlightedLettersRight <= 0:
                                self.highlightedLetter = 0
                                self.highlightedFirstLetter = 0

                    # Moving whole text to the right when it's too long to fit in to the box
                    if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosX) + 6 < 4:
                        self.textPosX += abs((self.font.size(self._text[0:self.currentLetter])[0]) + self.textPosX)
                    
        
                # Highlighting whole text by pressing L_CTRL + a
                if self.ctrlA.update():
                    # Unhighlighting
                    if self.highlightedFirstLetter == 0 and self.highlightedLetter == len(self._text):
                        self.highlighted = False
                        self.highlightedLetter = 0
                        self.highlightedLettersRight = 0
                        self.highlightedLettersLeft = 0
                    elif self.highlightedFirstLetter+1 == len(self._text) and self.highlightedLetter == 0:
                        self.highlighted = False
                        self.highlightedFirstLetter = 0
                        self.highlightedLettersRight = 0
                        self.highlightedLettersLeft = 0
                    # Highlighting
                    else:
                        self.highlightedFirstLetter = 0
                        self.highlightedLetter = len(self._text)
                        self.highlightedLettersRight = len(self._text)
                        self.highlighted = True

                # Pasting text to the text box from a clipboard
                if self.ctrlV.update():
                    pastedText = pyperclip.paste()
                    self._text = self._text[:self.currentLetter] + pastedText + self._text[self.currentLetter:]
                    self.currentLetter += len(pastedText)

                    # Moving whole text to the left when it's too long to fit in the box
                    if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosX) + 6 > (self._width - 3):
                        self.textPosX -= ((self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosX) + 6) - (self._width - 3))
                        if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosX) == (self._width - 9):
                            self.textPosX += 4

                # Copying highlighted text to the clipboard
                if self.ctrlC.update():
                    if self.highlightedLettersRight > 0 and (self.highlightedFirstLetter > 0 and self.highlightedLettersRight < len(self._text)):
                        pyperclip.copy(self._text[self.highlightedFirstLetter:self.highlightedLetter+1])
                    elif self.highlightedLettersLeft > 0:
                        pyperclip.copy(self._text[self.highlightedLetter:self.highlightedFirstLetter+1])
                    elif self.highlightedLettersRight == len(self._text) and self.highlightedFirstLetter == 0:
                        pyperclip.copy(self._text)

                # Cutting highlighted text
                if self.ctrlX.update():
                    if self.highlightedLettersRight > 0 and (self.highlightedFirstLetter > 0 and self.highlightedLettersRight < len(self._text)):
                        pyperclip.copy(self._text[self.highlightedFirstLetter:self.highlightedLetter+1])
                        self._text = self._text[:self.highlightedFirstLetter] + self._text[self.highlightedLetter+1:]
                        self.currentLetter -= self.highlightedLettersRight
                        self.highlightedLettersRight = 0
                        self.highlighted = False
                        self.highlightedLetter = 0
                        self.highlightedFirstLetter = 0

                    # Deleting text that's highlighted to the left
                    elif self.highlightedLettersLeft > 0:
                        pyperclip.copy(self._text[self.highlightedLetter:self.highlightedFirstLetter+1])
                        self._text = self._text[:self.highlightedLetter] + self._text[self.highlightedFirstLetter+1:]
                        self.highlightedLettersLeft = 0
                        self.highlighted = False
                        self.highlightedLetter = 0
                        self.highlightedFirstLetter = 0    

                    # Deleting whole text when whole text is highlighted
                    elif self.highlightedLettersRight == len(self._text) and self.highlightedFirstLetter == 0:
                        pyperclip.copy(self._text)
                        self._text = ""
                        self.currentLetter = 0
                        self.highlightedLettersRight = 0
                        self.highlighted = False
                        self.highlightedLetter = 0
                        self.highlightedFirstLetter = 0
                        self.textPosX = 2

                if event.key == pygame.K_LSHIFT:
                    self.holdingShift = True

            if event.type == pygame.KEYUP and self.active:
                if event.key == pygame.K_LSHIFT:
                    self.holdingShift = False
                if event.key == pygame.K_BACKSPACE:
                    self.holdingBackspace = False
                    self.backspaceTimer.stop()
                    self.backspaceHoldingTick = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.holdingArrow = False
                    self.arrowTimer.stop()
                    self.holdingLeftArrow = False
                    self.holdingRightArrow = False
                    self.arrowHoldingTick = 0

    def __tripleClick(self, pos):
        pass

    # Method for positioning cursor in the correct position based on which character user clicked on
    def __setCursorPosition(self, pos):
        self.cursorTimer.tick = 0
        self.showCursor = True
        if self._text != "":
            clickedPos = (pos[0] - self._x) + abs(self.textPosX) - 6
            charLengthList = []

            for i in range(len(self._text)):
                charLengthList.append((self.font.size(self._text[0:i])[0]))

            closest_number = min(charLengthList, key=lambda x: abs(x - clickedPos))
            self.currentLetter = charLengthList.index(closest_number)
            if clickedPos > self.font.size(self._text[0:len(self._text)-1])[0] + (self.font.size(self._text[-1])[0] // 2):
                self.currentLetter = len(self._text)

    def _highlightingByMousePosition(self, pos):
        pass

    def draw(self, surface=None):
        global _windowObject, _changingCursor
        if not(self._hide):
            if not(self.active):
                self.background0 = self.background
            if surface == None:
                surface = _windowObject.screen
            keys = pygame.key.get_pressed()
            if self.active:
                if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] and self.arrowHoldingTick < 30:
                    self.arrowHoldingTick += 1
                    self.cursorTimer.tick = 0
                    self.showCursor = True
                    if self.arrowHoldingTick == 30:
                        self.arrowTimer.restart()
                        self.holdingArrow = True
                if keys[pygame.K_BACKSPACE] and self.backspaceHoldingTick < 30:
                    self.backspaceHoldingTick += 1
                    self.cursorTimer.tick = 0
                    self.showCursor = True
                    if self.backspaceHoldingTick == 30:
                        self.backspaceTimer.restart()
                        self.holdingBackspace = True
            else:
                self.highlighted = False
                self.highlightedFirstLetter = 0
                self.highlightedLettersLeft = 0
                self.highlightedLettersRight = 0


            # Drawing outline of TextBox
            # Setting text box state (active or not active)
            # TO oepwlewekwec2wpvemwpewmpevwmpvewmpvemwpqvlwmepoevmwpw4mbope wmpoebwmpoewm
            pos = pygame.mouse.get_pos()

            if self._text == "" and not(self.active):
                self._text = self._placeholderText

            if self.mouseClickPosition:
                self._highlightingByMousePosition(pos)
                
            if self.rect.collidepoint(pos):
                if self._changeCursor:
                    _changingCursor = pygame.SYSTEM_CURSOR_IBEAM
                if self.hoverEvent != None:
                    if self._has_arguments(self.hoverEvent):
                        self.hoverEvent(self)
                    else:
                        self.hoverEvent()

            self.__tripleClick(pos)
            if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.active:
                self.__setCursorPosition(pos)
            
            if not(self.disable):
                if pygame.mouse.get_pressed()[0] == 1 and self.rect.collidepoint(pos):
                    if not(self.clicked) and not(self.clickedOutside):
                        self.active = True
                        self.clicked = True
                        self.background0 = self.activeBackground
                        self.outlineColor0 = self.activeOutlineColor
                        
                        if self._text == self._placeholderText:
                            self._text = ""
                            self.currentLetter = 0

                        if self.clickEvent != None:
                            if self._has_arguments(self.clickEvent):
                                self.clickEvent(self)
                            else:
                                self.clickEvent()

                        self.__setCursorPosition(pos)

                        self.mouseClickPosition = pos

                elif pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                    self.clicked = False

                elif pygame.mouse.get_pressed()[0] == 0 and self.clickedOutside:
                    self.clickedOutside = False

                elif pygame.mouse.get_pressed()[0] == 1 and self.active:
                    if not(self.rect.collidepoint(pos)) and not(self.clicked):
                        self.active = False
                        self.background0 = self._background
                        self.outlineColor0 = self._outlineColor

                elif pygame.mouse.get_pressed()[0] == 1 and not(self.clicked):
                    if not(self.active) and not(self.rect.collidepoint(pos)):
                        self.clickedOutside = True

            if self.outlineWidth > 0:
                if self.borderRadius > 1:
                    gfxdraw.aacircle(surface, (self.rect.x + self.borderRadius)-self.outlineWidth, (self.rect.y + self.borderRadius)-self.outlineWidth, self.borderRadius, self.outlineColor0)
                    gfxdraw.filled_circle(surface, (self.rect.x + self.borderRadius)-self.outlineWidth, (self.rect.y + self.borderRadius)-self.outlineWidth, self.borderRadius, self.outlineColor0)
                    gfxdraw.aacircle(surface, (self.rect.x + self.rect.width - self.borderRadius-1)+self.outlineWidth, (self.rect.y + self.borderRadius)-self.outlineWidth, self.borderRadius, self.outlineColor0)
                    gfxdraw.filled_circle(surface, (self.rect.x + self.rect.width - self.borderRadius-1)+self.outlineWidth, (self.rect.y + self.borderRadius)-self.outlineWidth, self.borderRadius, self.outlineColor0)
                    gfxdraw.aacircle(surface, (self.rect.x + self.borderRadius)-self.outlineWidth, (self.rect.y + self.rect.height - self.borderRadius-1)+self.outlineWidth, self.borderRadius, self.outlineColor0)
                    gfxdraw.filled_circle(surface, (self.rect.x + self.borderRadius)-self.outlineWidth, (self.rect.y + self.rect.height - self.borderRadius-1)+self.outlineWidth, self.borderRadius, self.outlineColor0)
                    gfxdraw.aacircle(surface, (self.rect.x + self.rect.width - self.borderRadius-2)+self.outlineWidth, (self.rect.y + self.rect.height - self.borderRadius-1)+self.outlineWidth, self.borderRadius, self.outlineColor0)
                    gfxdraw.filled_circle(surface, (self.rect.x + self.rect.width - self.borderRadius-2)+self.outlineWidth, (self.rect.y + self.rect.height - self.borderRadius-1)+self.outlineWidth, self.borderRadius, self.outlineColor0)

                    pygame.draw.rect(surface, self.outlineColor0, ((self.rect.x + self.borderRadius)-self.outlineWidth, self.rect.y-self.outlineWidth, (self.rect.width - 2 * self.borderRadius)+self.outlineWidth*2, self.rect.height+self.outlineWidth*2))
                    pygame.draw.rect(surface, self.outlineColor0, ((self.rect.x)-self.outlineWidth, self.rect.y + self.borderRadius-self.outlineWidth, self.rect.width+(self.outlineWidth*2), (self.rect.height - 2 * self.borderRadius)+self.outlineWidth*2))
                else:
                    pygame.draw.rect(surface, self.outlineColor0, pygame.Rect(self._x - self.outlineWidth, self._y - self.outlineWidth, self._width + (self.outlineWidth*2), self.rect.height + (self.outlineWidth*2)))
                
            if self.arrowTimer.loop():
                self.cursorTimer.tick = 0
                self.showCursor = True
                if self.holdingRightArrow and self.currentLetter < len(self._text):
                    self.currentLetter += 1
                    if self.holdingShift:
                        if self.highlightedFirstLetter == 0 and self.highlightedLettersRight == 0 and self.highlightedLettersLeft == 0:
                            self.highlightedFirstLetter = self.currentLetter-1
                        if self.highlightedLettersLeft <= 0:
                            self.highlightedLetter = self.currentLetter-1
                            self.highlightedLettersRight += 1
                        else:
                            self.highlightedLettersLeft -= 1
                            self.highlightedLetter += 1
                            if self.highlightedLettersLeft <= 0:
                                self.highlightedLetter = 0
                                self.highlightedFirstLetter = 0

                    # Moving whole text to the left when it's too long to fit in the box
                    if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosX) + 6 > (self._width - 3):
                        self.textPosX -= (self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosX) + 6) - (self._width - 3)
                        if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosX) == (self._width - 9):
                            self.textPosX += 4
                elif self.holdingLeftArrow  and self.currentLetter > 0:
                    self.currentLetter -= 1
                    if self.holdingShift:
                        if self.highlightedFirstLetter == 0 and self.highlightedLettersLeft == 0 and self.highlightedLettersRight == 0:
                            self.highlightedFirstLetter = self.currentLetter
                        if self.highlightedLettersRight <= 0:
                            self.highlightedLetter = self.currentLetter
                            self.highlightedLettersLeft += 1
                        else:
                            self.highlightedLettersRight -= 1
                            self.highlightedLetter -= 1
                            if self.highlightedLettersRight <= 0:
                                self.highlightedLetter = 0
                                self.highlightedFirstLetter = 0
                
                    # Moving whole text to the right when it's too long to fit in to the box
                    if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosX) + 6 < 4:
                        self.textPosX += abs((self.font.size(self._text[0:self.currentLetter])[0]) + self.textPosX)

            # Deleting characters by holding backspace
            if self.backspaceTimer.loop() and self._text != "" and self.currentLetter > 0:
                self.cursorTimer.tick = 0
                self.showCursor = True
                if self.holdingBackspace:
                    if self.textPosX < 2:
                        widthDiff = self.font.size(self._text[0:self.currentLetter-1])[0]
                        self.textPosX = (self._width - 3) - widthDiff - 2
                        if self.textPosX > 2:
                            self.textPosX = 2

                    if not(self.highlighted):
                        self.currentLetter -= 1
                        self._text = self._text[:self.currentLetter] + self._text[self.currentLetter+1:]
                    else:
                        if self.highlightedLettersRight > 0 and (self.highlightedFirstLetter > 0 and self.highlightedLettersRight < len(self._text)):
                            self._text = self._text[:self.highlightedFirstLetter] + self._text[self.highlightedLetter+1:]
                            self.currentLetter -= self.highlightedLettersRight
                            self.highlightedLettersRight = 0
                            self.highlighted = False
                            self.highlightedLetter = 0
                            self.highlightedFirstLetter = 0

                        elif self.highlightedLettersLeft > 0:
                            self._text = self._text[:self.highlightedLetter] + self._text[self.highlightedFirstLetter+1:]
                            self.highlightedLettersLeft = 0
                            self.highlighted = False
                            self.highlightedLetter = 0
                            self.highlightedFirstLetter = 0    

                        elif self.highlightedLettersRight == len(self._text) and self.highlightedFirstLetter == 0:
                            self._text = ""
                            self.currentLetter = 0
                            self.highlightedLettersRight = 0
                            self.highlighted = False
                            self.highlightedLetter = 0
                            self.highlightedFirstLetter = 0
                            self.textPosX = 2

            # Drawing rounded corners and whole TextBox rectangle
            if self._background != "transparent":
                if self.borderRadius > 1:
                    gfxdraw.aacircle(surface, self.rect.x + self.borderRadius, self.rect.y + self.borderRadius, self.borderRadius, self.background0)
                    gfxdraw.filled_circle(surface, self.rect.x + self.borderRadius, self.rect.y + self.borderRadius, self.borderRadius, self.background0)
                    gfxdraw.aacircle(surface, self.rect.x + self.rect.width - self.borderRadius-1, self.rect.y + self.borderRadius, self.borderRadius, self.background0)
                    gfxdraw.filled_circle(surface, self.rect.x + self.rect.width - self.borderRadius-1, self.rect.y + self.borderRadius, self.borderRadius, self.background0)
                    gfxdraw.aacircle(surface, self.rect.x + self.borderRadius, self.rect.y + self.rect.height - self.borderRadius-1, self.borderRadius, self.background0)
                    gfxdraw.filled_circle(surface, self.rect.x + self.borderRadius, self.rect.y + self.rect.height - self.borderRadius-1, self.borderRadius, self.background0)
                    gfxdraw.aacircle(surface, self.rect.x + self.rect.width - self.borderRadius-2, self.rect.y + self.rect.height - self.borderRadius-1, self.borderRadius, self.background0)
                    gfxdraw.filled_circle(surface, self.rect.x + self.rect.width - self.borderRadius-2, self.rect.y + self.rect.height - self.borderRadius-1, self.borderRadius, self.background0)

                    pygame.draw.rect(surface, self.background0, (self.rect.x + self.borderRadius, self.rect.y, self.rect.width - 2 * self.borderRadius, self.rect.height))
                    pygame.draw.rect(surface, self.background0, (self.rect.x, self.rect.y + self.borderRadius, self.rect.width, self.rect.height - 2 * self.borderRadius))
                else:
                    pygame.draw.rect(surface, self.background0, self.rect)
            
            surface.blit(self.textSurface, (self.rect.x + 2, self.rect.y + self.rect.height // 2 - (self.textSurface.get_height() // 2)))
            if self._background != "transparent":
                self.textSurface.fill(self.background0)
            else:
                self.textSurface.fill((0,0,0,0))

            # Correcting text position when cursor is on character 0        
            if self.textPosX < 2 and self.currentLetter == 0:
                self.textPosX = 2

            # Rendering text font
            textColor = self.textColor0
            if self._text == self._placeholderText and not(self.active):
                textColor = self.placeholderColor
            self.text_surface = self.font.render(self._text, True, textColor)

            if not(self.arrowTimer.run):
                if self.cursorTimer.loop():
                    if not(self.showCursor):
                        self.showCursor = True
                    else:
                        self.showCursor = False

            if self.highlightedLettersLeft > 0 or self.highlightedLettersRight > 0:
                self.highlighted = True
                self.showCursor = False
            else:
                self.highlighted = False
            
            # Drawing highlight surface
            if self.highlighted:
                width = 0
                startX = 0
                if self.highlightedLetter > self.highlightedFirstLetter:
                    width = self.font.size(self._text[self.highlightedFirstLetter:self.highlightedLetter+1])[0]
                    startX = self.font.size(self._text[0:self.highlightedFirstLetter])[0]
                elif self.highlightedLetter == self.highlightedFirstLetter:
                    width = self.font.size(self._text[self.highlightedFirstLetter])[0]
                    startX = self.font.size(self._text[0:self.highlightedFirstLetter])[0]
                elif self.highlightedFirstLetter > self.highlightedLetter:
                    width = self.font.size(self._text[self.highlightedLetter:self.highlightedFirstLetter+1])[0]
                    startX = self.font.size(self._text[0:self.highlightedLetter])[0]

                self.highlightedRect = pygame.Surface((width,self.text_surface.get_height()))
                self.highlightedRect.fill(self.highlightColor)
                if abs(self.textPosX) > 2:
                    startX -= 4
                self.textSurface.blit(self.highlightedRect, ((startX+4)-abs(self.textPosX),0))

            # Drawing text in the box
            if self._text != "":
                self.textSurface.blit(self.text_surface, (self.textPosX, 0))

            # Drawing IBEAM cursor
            if self.showCursor and self.active:
                self.cursorIBEAM.fill(self.cursorColor)
                posX = self.font.size(self._text[0:self.currentLetter])[0] + 2
                if posX > self._width - 6 and self.currentLetter == len(self._text):
                    posX = self._width - 6
                elif self.currentLetter < len(self._text):
                    posX = posX+self.textPosX - 2

                if self.currentLetter > 0:
                    if posX > (self._width - 6):
                        posX = self._width - 6
                    self.textSurface.blit(self.cursorIBEAM, (posX, 0))
                else:
                    posX = self.textPosX
                    if posX < 2:
                        posX = 2
                    elif self.currentLetter == 0 and posX > 2:
                        posX = 2
                    self.textSurface.blit(self.cursorIBEAM, (posX, 0))


# -=-=-=- Test Class -=-=-=- #
class CricularTest():
    def __init__(self):
        self.current_angle = 1
        self.angle = math.pi*2 / 90
        self.rects_list = []

    def draw(self, surface):
        self.current_angle += self.angle
        x = math.sin(self.current_angle) * 100
        y = math.cos(self.current_angle) * 100
        pygame.draw.circle(surface, (255,0,0), (x+200,y+200), 8)

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time of {func.__name__}: {execution_time} seconds")
        return result
    return wrapper

class ColorPicker():
    def __init__(self, **kwargs):
        self._x = kwargs.get("x", 0)
        self._x = kwargs.get("_x", self._x)
        self._y = kwargs.get("y", 0)
        self._y = kwargs.get("_y", self._y)
        self._width = kwargs.get("width", 250)
        self._width = kwargs.get("_width", self._width)
        self._height = kwargs.get("height", 250)
        self._height = kwargs.get("_height", self._height)
        self._buttonWidth = kwargs.get("buttonWidth", 20)
        self._buttonWidth = kwargs.get("_buttonWidth", self._buttonWidth)
        self._buttonHeight = kwargs.get("buttonHeight", 20)
        self._buttonHeight = kwargs.get("_buttonHeight", self._buttonHeight)
        self._outlineWidth = kwargs.get("outlineWidth", 0)
        self._outlineWidth = kwargs.get("_outlineWidth", self._outlineWidth)
        self.outlineColor = kwargs.get("outlineColor", (255,255,255))
        self.background = kwargs.get("background", (30,30,30))
        self._defaultColor = kwargs.get("defaultColor", (75,10,175))
        self._defaultColor = kwargs.get("_defaultColor", self._defaultColor)
        self.showColorPicker = False
        self.clickedOutside = False
        self._clickedButton = False
        self.clicked = False
        self.allowAlphaChannel = kwargs.get("allowAlphaChannel", True)
        self.changeCursor = kwargs.get("changeCursor", True)
        self._colorPickerPosition = kwargs.get("colorPickerPosition", "bottom")
        self._colorPickerPosition = kwargs.get("_colorPickerPosition", self._colorPickerPosition)

        self.name = kwargs.get("name", None)
        self.z_index = kwargs.get("z_index", None)
        self._disable = kwargs.get("disable", False)
        self._disable = kwargs.get("_disable", self._disable)
        self._hide = kwargs.get("hide", False)
        self._hide = kwargs.get("_hide", self._hide)

        self._DISPLAY_SIZE = get_display_size(ignoreTaskBar=True)

        if self._width < 200:
            self._width = 200
        if self._height < 200:
            self._height = 200

        self._currentColor = self._defaultColor
        self.originalColor = self._defaultColor

        if len(self._currentColor) == 3:
            self._currentColor = (self._currentColor[0], self._currentColor[1], self._currentColor[2], 255)
            self.originalColor = self._currentColor

        self.button = Surface(x=self._x, y=self._y, width=self._buttonWidth, height=self._buttonHeight, background=self._currentColor)

        self.rect = pygame.Rect(self._x - self._outlineWidth, self._y - self._outlineWidth, self.button.width + (self._outlineWidth * 2), self.button.height + (self._outlineWidth * 2))
        self.colorPickerRect = pygame.Rect(self._x, self._y+self.button.height+self._outlineWidth, self._width+40, self._height+15)
        self._rectBelowSurface = pygame.Rect(self._x+10, self._y+10+self.button.height+self._outlineWidth, self._width-80, self._height-80)
        self.outlineRect = pygame.Rect(self._x+9, self._y+9+self.button.height+self._outlineWidth, self._width-78, self._height-78)
        self.currentColorSurface = pygame.Surface((50,30), pygame.SRCALPHA)
        self.originalColorSurface = pygame.Surface((50,30), pygame.SRCALPHA)
        self.currentColorLabel = Label(text="Current", x=self.outlineRect.right + 40, y=self._y+12+self.button.height, fontSize=11, textColor=(255,255,255))
        self.originalColorLabel = Label(text="Original", x=self.outlineRect.right + 40, y=self._y+72+self.button.height, fontSize=11, textColor=(255,255,255))
        
        self.redTextBox = TextBox(text=f"{self._currentColor[0]}", x=self._rectBelowSurface.x+20, y=self._rectBelowSurface.bottom+12, fontSize=11, width=35, height=25, textColor=(225,225,225), numbersOnly=True, maxCharacters=3, background=(10,10,10), activeBackground=(20,20,20), placeholderText=f"{self.currentColor[0]}")
        self.redColorLabel = Label(text="R:", x=self.redTextBox.x-16, y=self.redTextBox.y+6, fontSize=12, textColor=(255,255,255))

        self.greenTextBox = TextBox(text=f"{self._currentColor[1]}", x=self._rectBelowSurface.x+80, y=self._rectBelowSurface.bottom+12, fontSize=11, width=35, height=25, textColor=(225,225,225), numbersOnly=True, maxCharacters=3, background=(10,10,10), activeBackground=(20,20,20), placeholderText=f"{self.currentColor[1]}")
        self.greenColorLabel = Label(text="G:", x=self.greenTextBox.x-16, y=self.greenTextBox.y+6, fontSize=12, textColor=(255,255,255))

        self.blueTextBox = TextBox(text=f"{self._currentColor[2]}", x=self._rectBelowSurface.x+140, y=self._rectBelowSurface.bottom+12, fontSize=11, width=35, height=25, textColor=(225,225,225), numbersOnly=True, maxCharacters=3, background=(10,10,10), activeBackground=(20,20,20), placeholderText=f"{self.currentColor[2]}")
        self.blueColorLabel = Label(text="B:", x=self.blueTextBox.x-16, y=self.blueTextBox.y+6, fontSize=12, textColor=(255,255,255))

        self.alphaTextBox = TextBox(text=f"{self._currentColor[3]}", x=self._rectBelowSurface.x+20, y=self._rectBelowSurface.bottom+46, fontSize=11, width=35, height=25, textColor=(225,225,225), numbersOnly=True, maxCharacters=3, background=(10,10,10), activeBackground=(20,20,20), placeholderText=f"{self.currentColor[3]}")
        self.alphaColorLabel = Label(text="A:", x=self.alphaTextBox.x-16, y=self.alphaTextBox.y+6, fontSize=12, textColor=(255,255,255))

        self.hexTextBox = TextBox(text=self.rgb_to_hex(self._defaultColor), x=self._rectBelowSurface.x+96, y=self._rectBelowSurface.bottom+46, fontSize=11, width=78, height=25, textColor=(225,225,225), background=(10,10,10), activeBackground=(20,20,20), placeholderText="HEX color value")
        self.hexColorLabel = Label(text="HEX:", x=self.hexTextBox.x-32, y=self.hexTextBox.y+6, fontSize=12, textColor=(255,255,255))

        self.surface = pygame.Surface((self._width-80, self._height-80), pygame.SRCALPHA)

        self.sliderSurface = pygame.Surface((12, self._height-110))
        self.init_colors_slider()

        self.whiteColorRect = Rectangle(x=self._rectBelowSurface.right + 12, y=self._rectBelowSurface.y+(self._height-110)+12, width=12, height=12, background=(255,255,255))

        self.change_color(self._defaultColor)

        self.y = self._y
        self.x = self._x

    @property
    def disable(self):
        return self._disable
    
    @disable.setter
    def disable(self, value: bool):
        self._disable = value
        self.redTextBox.disable = self._disable
        self.greenTextBox.disable = self._disable
        self.blueTextBox.disable = self._disable
        self.alphaTextBox.disable = self._disable
        self.hexTextBox.disable = self._disable

    @property
    def hide(self):
        return self._hide
    
    @hide.setter
    def hide(self, value: bool):
        self._hide = value

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value: int):
        self._width = value
        if self._width < 200:
            self._width = 200
        self.colorPickerRect.width = self._width+40
        self._rectBelowSurface.width = self._width-80
        self.outlineRect.width = self._width-78
        self.surface = pygame.Surface((self._width-80, self._height-80), pygame.SRCALPHA)
        self._setContentPositionX()
        self._setContentPositionY()
        self.change_color(self._defaultColor)

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value: int):
        self._height = value
        if self._height < 200:
            self._height = 200
        self.colorPickerRect.height = self._height+15
        self._rectBelowSurface.height = self._height-80
        self.outlineRect.height = self._height-78
        self.sliderSurface = pygame.Surface((12, self._height-110))
        self.surface = pygame.Surface((self._width-80, self._height-80), pygame.SRCALPHA)
        self._setContentPositionX()
        self._setContentPositionY()
        self.init_colors_slider()
        self.change_color(self._defaultColor)

    @property
    def buttonWidth(self):
        return self._buttonWidth
    
    @buttonWidth.setter
    def buttonWidth(self, value: int):
        self._buttonWidth = value
        self.button.width = self._buttonWidth
        self.rect.width, self.rect.height = self.button.width + (self._outlineWidth * 2), self.button.height + (self._outlineWidth * 2)
        self._setContentPositionX()
        self._setContentPositionY()

    @property
    def buttonHeight(self):
        return self._buttonHeight
    
    @buttonHeight.setter
    def buttonHeight(self, value: int):
        self._buttonHeight= value
        self.button.height = self._buttonHeight
        self.rect.width, self.rect.height = self.button.width + (self._outlineWidth * 2), self.button.height + (self._outlineWidth * 2)
        self._setContentPositionX()
        self._setContentPositionY()

    @property
    def defaultColor(self):
        return self._defaultColor
    
    @defaultColor.setter
    def defaultColor(self, value: tuple):
        self._defaultColor = value
        self._currentColor = self._defaultColor
        self.originalColor = self._defaultColor
        self.hexTextBox.text = self.rgb_to_hex(self._defaultColor)

    @property
    def outlineWidth(self):
        return self._outlineWidth

    @outlineWidth.setter
    def outlineWidth(self, value: int):
        self._outlineWidth = value
        self.rect = pygame.Rect(self._x - self._outlineWidth, self._y - self._outlineWidth, self.button.width + (self._outlineWidth * 2), self.button.height + (self._outlineWidth * 2))
        self._setContentPositionX()
        self._setContentPositionY()

    def init_colors_slider(self):
        # Generate the color spectrum
        for y in range(self.sliderSurface.get_height()):
            for x in range(self.sliderSurface.get_width()):
                position = y / self.sliderSurface.get_height()

                rgb = tuple(round(c * 255) for c in colorsys.hsv_to_rgb(position, 1, 1))
                color = pygame.Color(*rgb)

                self.sliderSurface.set_at((x, y), color)

    def change_color(self, color):
        # Generate the color spectrum
        y_coords = np.linspace(0, 1, self.surface.get_height())
        red_values = (y_coords * color[0]).astype(int)
        green_values = (y_coords * color[1]).astype(int)
        blue_values = (y_coords * color[2]).astype(int)

        x_coords = np.linspace(1, 0, self.surface.get_width())
        black_values = (x_coords * 255).astype(int)
        white_values = ((black_values / 2) + 127).astype(int)

        for y, red, green, blue in zip(range(self.surface.get_height()-1, -1, -1), red_values, green_values, blue_values):
            surface_colors = (red, green, blue)
            for x, black, white in zip(range(self.surface.get_width()-1, -1, -1), black_values, white_values):
                self.surface.set_at((x, y), surface_colors)
    
    def rgb_to_hex(self, rgba):
        r, g, b = rgba[0], rgba[1], rgba[2]
        hex_value = f"#{r:02x}{g:02x}{b:02x}"
        return hex_value
    
    def hex_to_rgb(self, hex_value):
        try:
            hex_value = hex_value.lstrip("#")
            r = int(hex_value[0:2], 16)
            g = int(hex_value[2:4], 16)
            b = int(hex_value[4:6], 16)
            return (r, g, b)
        except:
            return self._currentColor

    @property
    def currentColor(self):
        return self._currentColor

    @currentColor.setter
    def currentColor(self, value: tuple):
        self._currentColor = value

    def _setContentPositionX(self):
        if self._colorPickerPosition == "bottom":
            self.colorPickerRect.x = self._x - self._outlineWidth
        elif self._colorPickerPosition == "right":
            self.colorPickerRect.x = self._x + self.button.width+self._outlineWidth
        elif self._colorPickerPosition == "left":
            self.colorPickerRect.right = self._x - self._outlineWidth
        self.button.x = self._x
        self.rect.x = self._x - self._outlineWidth
        self._rectBelowSurface.x = self.colorPickerRect.x+10
        self.outlineRect.x = self.colorPickerRect.x+9
        self.currentColorLabel.x = self.outlineRect.right + 40
        self.originalColorLabel.x = self.outlineRect.right + 40
        self.redTextBox.x = self._rectBelowSurface.x+20
        self.redColorLabel.x = self.redTextBox.x-16
        self.greenTextBox.x = self._rectBelowSurface.x+80
        self.greenColorLabel.x = self.greenTextBox.x-16
        self.blueTextBox.x = self._rectBelowSurface.x+140
        self.blueColorLabel.x = self.blueTextBox.x-16
        self.alphaTextBox.x = self._rectBelowSurface.x+20
        self.alphaColorLabel.x = self.alphaTextBox.x-16
        self.hexTextBox.x = self._rectBelowSurface.x+96
        self.hexColorLabel.x = self.hexTextBox.x-32
        self.whiteColorRect.x = self._rectBelowSurface.right + 12

    def _setContentPositionY(self):
        if self._colorPickerPosition == "bottom":
            self.colorPickerRect.y = self._y+self.button.height+self._outlineWidth
        elif self._colorPickerPosition == "right" or self._colorPickerPosition == "left":
            self.colorPickerRect.y = self._y - self._outlineWidth
        self.rect.y = self._y - self._outlineWidth
        self._rectBelowSurface.y = self.colorPickerRect.y+10
        self.outlineRect.y = self.colorPickerRect.y+9
        self.currentColorLabel.y = self.colorPickerRect.y+12
        self.originalColorLabel.y = self.colorPickerRect.y+72
        self.redTextBox.y = self._rectBelowSurface.bottom+12
        self.redColorLabel.y = self.redTextBox.y+6
        self.greenTextBox.y = self._rectBelowSurface.bottom+12
        self.greenColorLabel.y = self.greenTextBox.y+6
        self.blueTextBox.y = self._rectBelowSurface.bottom+12
        self.blueColorLabel.y = self.blueTextBox.y+6
        self.alphaTextBox.y = self._rectBelowSurface.bottom+46
        self.alphaColorLabel.y = self.alphaTextBox.y+6
        self.hexTextBox.y = self._rectBelowSurface.bottom+46
        self.hexColorLabel.y = self.hexTextBox.y+6
        self.whiteColorRect.y = self._rectBelowSurface.y+(self._height-110)+12

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value: int):
        self._x = value
        self.button.x = self._x
        self._setContentPositionX()

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value: int):
        self._y = value
        self.button.y = self._y
        self._setContentPositionY()

    @property
    def colorPickerPosition(self):
        return self._colorPickerPosition
    
    @colorPickerPosition.setter
    def colorPickerPosition(self, value: str):
        self._colorPickerPosition = value
        self._setContentPositionX()
        self._setContentPositionY()

    def _deactivateTextBoxes(self):
        textboxes = [self.redTextBox, self.greenTextBox, self.blueTextBox, self.alphaTextBox, self.hexTextBox]
        for i in textboxes:
            if i.active:
                i.active = False

    def mouse_click(self):
        if self.button.mouse_click():
            return True
        
    def mouse_hovering(self):
        if self.button.mouse_hovering():
            return True

    def draw(self, surface=None):
        global _changingCursor
        if not(self._hide):
            if surface == None:
                surface = _windowObject.screen

            pos = pygame.mouse.get_pos()

            if self._outlineWidth >= 1:
                pygame.draw.rect(surface, self.outlineColor, pygame.Rect(self._x-self._outlineWidth, self._y-self._outlineWidth, self._buttonWidth+(self._outlineWidth*2), self._buttonHeight+(self._outlineWidth*2)), width=1)

            if self.allowAlphaChannel:
                self.button.background = self._currentColor
            else:
                self.button.background = (self._currentColor[0], self._currentColor[1], self._currentColor[2])
            self.button.draw()

            if not(self.disable):
                if self.button.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
                    if not(self._clickedButton) and not(self.clickedOutside):
                        self._clickedButton = True

                if self.button.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 0:
                    if not(self.showColorPicker) and self._clickedButton:
                        self.clicked = True
                        self.showColorPicker = True
                        self._clickedButton = False
                    elif self.showColorPicker and self._clickedButton:
                        self.clicked = False
                        self.showColorPicker = False
                        self._deactivateTextBoxes()
                        self._clickedButton = False

                elif not(self.button.rect.collidepoint(pos)) and pygame.mouse.get_pressed()[0] == 1:
                    if not(self.colorPickerRect.collidepoint(pos)):
                        if self.showColorPicker:
                            self.clicked = False
                            self.showColorPicker = False
                            self._deactivateTextBoxes()
                            self._clickedButton = False

                if not(self.button.rect.collidepoint(pos)) and pygame.mouse.get_pressed()[0] == 1:
                    if not(self.clickedOutside):
                        self.clickedOutside = True
                        self._clickedButton = False

                if self.clickedOutside and pygame.mouse.get_pressed()[0] == 0:
                    self.clickedOutside = False
                    self._clickedButton = False

            # Changing cursor
            if self.button.rect.collidepoint(pos):
                if self.changeCursor:
                    _changingCursor = pygame.SYSTEM_CURSOR_HAND

            if self.showColorPicker:
                offsetY = self.button.height+self._outlineWidth
                pygame.draw.rect(surface, self.background, self.colorPickerRect)
                pygame.draw.rect(surface, (255,255,255), self._rectBelowSurface)
                pygame.draw.rect(surface, (0,0,0), self.outlineRect, width=1)

                if self.allowAlphaChannel:
                    self.currentColorSurface.fill(self._currentColor)
                else:
                    self.currentColorSurface.fill((self._currentColor[0], self._currentColor[1], self._currentColor[2]))

                surface.blit(self.currentColorSurface, (self.outlineRect.right + 40, self.colorPickerRect.y+30))

                if self.allowAlphaChannel:
                    self.originalColorSurface.fill(self.originalColor)
                else:
                    self.originalColorSurface.fill((self.originalColor[0], self.originalColor[1], self.originalColor[2]))

                surface.blit(self.originalColorSurface, (self.outlineRect.right + 40, self.colorPickerRect.y+90))
                surface.blit(self.surface, (self.colorPickerRect.x+10, self.colorPickerRect.y+10))
                surface.blit(self.sliderSurface, (self._rectBelowSurface.right + 12, self._rectBelowSurface.y+5))
                self.currentColorLabel.draw()
                self.originalColorLabel.draw()
                self.redTextBox.draw()
                self.redColorLabel.draw()
                self.greenTextBox.draw()
                self.greenColorLabel.draw()
                self.blueTextBox.draw()
                self.blueColorLabel.draw()
                
                if self.allowAlphaChannel:
                    self.alphaTextBox.draw()
                    self.alphaColorLabel.draw()

                self.hexTextBox.draw()
                self.hexColorLabel.draw()
                self.whiteColorRect.draw()

                if self.whiteColorRect.rect.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1:
                        self._currentColor = (255,255,255)
                        self.redTextBox.text = str(self._currentColor[0])
                        self.redTextBox.placeholderText = str(self._currentColor[0])
                        self.greenTextBox.text = str(self._currentColor[1])
                        self.greenTextBox.placeholderText = str(self._currentColor[1])
                        self.blueTextBox.text = str(self._currentColor[2])
                        self.blueTextBox.placeholderText = str(self._currentColor[2])
                        self.alphaTextBox.text = "255"
                        self.alphaTextBox.placeholderText = "255"
                        self.hexTextBox.text = str(self.rgb_to_hex(self._currentColor))
                        self.change_color(self._currentColor)

                if self.redTextBox.text != "":
                    if int(self.redTextBox.text) > 255:
                        self.redTextBox.text = "255"
                if len(self.redTextBox.text) > 1:
                    if self.redTextBox.text[0] == "0":
                        self.redTextBox.text = "0"
                    
                if self.greenTextBox.text != "":
                    if int(self.greenTextBox.text) > 255:
                        self.greenTextBox.text = "255"
                if len(self.greenTextBox.text) > 1:
                    if self.greenTextBox.text[0] == "0":
                        self.greenTextBox.text = "0"

                if self.blueTextBox.text != "":
                    if int(self.blueTextBox.text) > 255:
                        self.blueTextBox.text = "255"
                if len(self.blueTextBox.text) > 1:
                    if self.blueTextBox.text[0] == "0":
                        self.blueTextBox.text = "0"

                if self.alphaTextBox.text != "":
                    if int(self.alphaTextBox.text) > 255:
                        self.alphaTextBox.text = "255"
                if len(self.alphaTextBox.text) > 1:
                    if self.alphaTextBox.text[0] == "0":
                        self.alphaTextBox.text = "0"
                
                pos = pygame.mouse.get_pos()
                if self._rectBelowSurface.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1:
                        color = self.surface.get_at((pos[0]-self._rectBelowSurface.x, pos[1]-self._rectBelowSurface.y))
                        self.redTextBox.text = str(color[0])
                        self.redTextBox.placeholderText = str(color[0])
                        self.greenTextBox.text = str(color[1])
                        self.greenTextBox.placeholderText = str(color[1])
                        self.blueTextBox.text = str(color[2])
                        self.blueTextBox.placeholderText = str(color[2])
                        self.alphaTextBox.text = str(color[3])
                        self.alphaTextBox.placeholderText = str(color[3])

                colorR = self.redTextBox.text
                colorG = self.greenTextBox.text
                colorB = self.blueTextBox.text
                colorA = self.alphaTextBox.text

                if colorR == "":
                    colorR = self.redTextBox.placeholderText
                if colorG == "":
                    colorG = self.greenTextBox.placeholderText
                if colorB == "":
                    colorB = self.blueTextBox.placeholderText
                if colorA == "":
                    colorA = self.alphaTextBox.placeholderText

                self.currentColor = (int(colorR), int(colorG), int(colorB), int(colorA))

                textboxes = [self.redTextBox, self.greenTextBox, self.blueTextBox, self.alphaTextBox, self.hexTextBox]

                if self.originalColorSurface.get_rect(topleft=(self.outlineRect.right + 40, self.colorPickerRect.y+90)).collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1:
                        originalColor = self.originalColorSurface.get_at((pos[0]-(self.outlineRect.right + 40), pos[1]-(self.colorPickerRect.y+90)))
                        self.redTextBox.text = str(originalColor[0])
                        self.greenTextBox.text = str(originalColor[1])
                        self.blueTextBox.text = str(originalColor[2])
                        self.alphaTextBox.text = str(originalColor[3])
                        self.hexTextBox.text = str(self.rgb_to_hex(originalColor))
                        self.change_color(originalColor)

                if self.sliderSurface.get_rect(topleft=(self._rectBelowSurface.right + 12, self._rectBelowSurface.y+5)).collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1:
                        self._currentColor = self.sliderSurface.get_at((pos[0]-(self._rectBelowSurface.right + 12), pos[1]-(self._rectBelowSurface.y+5)))
                        self.change_color(self._currentColor)
                        self.redTextBox.text = str(self._currentColor[0])
                        self.greenTextBox.text = str(self._currentColor[1])
                        self.blueTextBox.text = str(self._currentColor[2])
                        self.alphaTextBox.text = str(self._currentColor[3])
                        self.hexTextBox.text = str(self.rgb_to_hex(self._currentColor))

                for i in textboxes:
                    if i.active:
                        if i == self.hexTextBox:
                            if i.get_enter_press():
                                self.change_color(self.hex_to_rgb(self.hexTextBox.text))

                        if i.get_enter_press() and i != self.hexTextBox:
                            self.change_color(self._currentColor)
                            self.hexTextBox.text = self.rgb_to_hex(self._currentColor)


class Animation():
    def __init__(self, **kwargs):
        self._x = kwargs.get("x", 0)
        self._x = kwargs.get("_x", self._x)
        self._y = kwargs.get("y", 0)
        self._y = kwargs.get("_y", self._y)
        self._images = kwargs.get("images", None)
        self._images = kwargs.get("_images", self._images)
        if self._images == None:
            self._images = ["PyniteAssets/no-animation-image1.png", "PyniteAssets/no-animation-image2.png",
                            "PyniteAssets/no-animation-image3.png"]
            for item in self._images:
                if not(os.path.exists(item)): 
                    self._images.remove(item)
            if self._images == []:
                self._images = None

        # -=-=-=-=- Fixing images path -=-=-=-=-=-=-==-= #
        temp_images_list = []
        for i in range(len(self._images)):
            if not(self._images.__contains__(_filePath)):
                if os.path.exists(f"{_filePath}/" + self._images[i]):
                    temp_images_list.append(f"{_filePath}/" + self._images[i])
                elif os.path.exists(self._images[i]):
                    temp_images_list.append(self._images[i])
                else:
                    temp_images_list = ["PyniteAssets/no-animation-image1.png", "PyniteAssets/no-animation-image2.png",
                                        "PyniteAssets/no-animation-image3.png"]
                    break
        if len(temp_images_list) == 0:
            temp_images_list = ["PyniteAssets/no-animation-image1.png", "PyniteAssets/no-animation-image2.png",
                                    "PyniteAssets/no-animation-image3.png"]
        self._images = temp_images_list
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

        self._animationSpeed = kwargs.get("animationSpeed", 0.2)
        self._animationSpeed = kwargs.get("_animationSpeed", self._animationSpeed)
        self._stopAnimation = kwargs.get("stopAnimation", False)
        self._stopAnimation = kwargs.get("_stopAnimation", self._stopAnimation)
        self.convertAlpha = kwargs.get("convertAlpha", True)
        self.fill = kwargs.get("fill", None)

        self.name = kwargs.get("name", None)
        self.z_index = kwargs.get("z_index", None)
        self.hide = kwargs.get("hide", False)

        self.clickEvent = None
        self.hoverEvent = None

        self._currentImage = None
        self._currentImageIndex = None
        self.rect = None
        if self._images != None:
            self._currentImage = pygame.image.load(self._images[0])
            if self.convertAlpha:
                self._currentImage.convert_alpha()
            self._currentImageIndex = 0
            self.rect = pygame.Rect(self._x, self._y, self._currentImage.get_width(), self._currentImage.get_height())

        self._imageTimer = Timer(self._animationSpeed)
        if not(self._stopAnimation):
            self._imageTimer.start()

    @property
    def animationSpeed(self):
        return self._animationSpeed

    @animationSpeed.setter
    def animationSpeed(self, value):
        self._animationSpeed = value
        self._imageTimer.time = value

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value: int):
        self._x = value
        self.rect.x = value
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value: int):
        self._y = value
        self.rect.y = value

    @property
    def images(self):
        return self._images
    
    @images.setter
    def images(self, value: list):
        self._images = value

        # -=-=-=-=- Fixing images path -=-=-=-=-=-=-==-= #
        temp_images_list = []
        for i in range(len(self._images)):
            if not(self._images.__contains__(_filePath)):
                if os.path.exists(f"{_filePath}/" + self._images[i]):
                    temp_images_list.append(f"{_filePath}/" + self._images[i])
                elif os.path.exists(self._images[i]):
                    temp_images_list.append(self._images[i])
                else:
                    temp_images_list = ["PyniteAssets/no-animation-image1.png", "PyniteAssets/no-animation-image2.png",
                                        "PyniteAssets/no-animation-image3.png"]
                    break
        if len(temp_images_list) == 0:
            temp_images_list = ["PyniteAssets/no-animation-image1.png", "PyniteAssets/no-animation-image2.png",
                                    "PyniteAssets/no-animation-image3.png"]
        self._images = temp_images_list
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

        self.restartAnimation()

    @property
    def stopAnimation(self):
        return self._stopAnimation

    @stopAnimation.setter
    def stopAnimation(self, value: bool):
        self._stopAnimation = value
        if not(self._stopAnimation):
            self._imageTimer.start()
        else:
            self._imageTimer.stop()

    def startAnimation(self):
        self._stopAnimation = False
        self._imageTimer.start()
    
    def restartAnimation(self):
        self._stopAnimation = False
        self._currentImageIndex = 0
        self._currentImage = pygame.image.load(self._images[0])
        if self.convertAlpha:
            self._currentImage.convert_alpha()
        self._imageTimer.restart()

    def _has_arguments(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters
        argument_names = [param.name for param in parameters.values()]
        if len(argument_names) > 0:
            return True
        else:
            return False

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def mouse_hovering(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        
    def mouse_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

    def draw(self, surface=None):
        if surface == None:
            surface = _windowObject.screen

        if not(self.hide):
            if self._images != None:
                if self._imageTimer.loop():
                    if self._currentImageIndex+1 < len(self._images):
                        self._currentImageIndex += 1          
                    else:
                        self._currentImageIndex = 0

                    self._currentImage = pygame.image.load(self._images[self._currentImageIndex])
                    self.rect.width, self.rect.height = self._currentImage.get_width(), self._currentImage.get_height()

                    if self.convertAlpha:
                        self._currentImage.convert_alpha()
                    
                if self.convertAlpha:
                    self._currentImage.convert_alpha()

                if self.fill != None:
                    pygame.draw.rect(surface, self.fill, self.rect)
                
                surface.blit(self._currentImage, (self._x, self._y))

class ProgressBar():
    def __init__(self, **kwargs):
        self._x = kwargs.get("x", 0)
        self._x = kwargs.get("_x", self._x)
        self._y = kwargs.get("y", 0)
        self._y = kwargs.get("_y", self._y)
        self._width = kwargs.get("width", 100)
        self._width = kwargs.get("_width", self._width)
        self._height = kwargs.get("height", 25)
        self._height = kwargs.get("_height", self._height)
        self.background = kwargs.get("background", (40,40,40))
        self.valueBackground = kwargs.get("valueBackground", (75,10,175))
        self.borderRadius = kwargs.get("borderRadius", 0)
        self._value = kwargs.get("value", 0)
        self._value = kwargs.get("_value", self._value)
        self._maxValue = kwargs.get("maxValue", 100)
        self._maxValue = kwargs.get("_maxValue", self._maxValue)

        if self._value > self._maxValue:
            self._value = self._maxValue
        elif self._value < 0:
            self._value = 0

        self.hide = kwargs.get("hide", False)
        self.name = kwargs.get("name", None)
        self.z_index = kwargs.get("z_index", None)

        self.clickEvent = None
        self.hoverEvent = None

        self.rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self.valueRect = pygame.Rect(self._x, self._y, (self._width / self._maxValue) * self._value, self._height)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value
        self.rect.x = self._x
        self.valueRect.x = self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value
        self.rect.y = self._y
        self.valueRect.y = self._y

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value
        self.rect.width = self._width
        self.valueRect.width = (self._width / self._maxValue) * self._value

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value: int):
        self._height = value
        self.rect.height = self._height
        self.valueRect.height = self._height

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: int):
        self._value = value
        if self._value > self._maxValue:
            self._value = self._maxValue
        elif self._value < 0:
            self._value = 0

        self.valueRect.width = (self._width / self._maxValue) * self._value

    @property
    def maxValue(self):
        return self._maxValue
    
    @maxValue.setter
    def maxValue(self, value: int):
        self._maxValue = value
        if self._maxValue < self._value:
            self._value = self._maxValue

        self.valueRect.width = (self._width / self._maxValue) * self._value

    def _has_arguments(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters
        argument_names = [param.name for param in parameters.values()]
        if len(argument_names) > 0:
            return True
        else:
            return False

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def mouse_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                return True
            
    def mouse_hovering(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True

    def draw(self, surface=None):
        if surface == None:
            surface = _windowObject.screen

        if not(self.hide):
            
            pygame.draw.rect(surface, self.background, self.rect, 0, self.borderRadius)
            pygame.draw.rect(surface, self.valueBackground, self.valueRect, 0, self.borderRadius)

class CheckBox():
    def __init__(self, **kwargs):
        global _clickableObjects, _allObjects
        self._x = kwargs.get("x", 0)
        self._x = kwargs.get("_x", self._x)
        self._y = kwargs.get("y", 0)
        self._y = kwargs.get("_y", self._y)
        self._size = kwargs.get("size", 20)
        self._size = kwargs.get("_size", self._size)
        self.background = kwargs.get("background", (75,10,175))
        self.checkSignColor = kwargs.get("checkSignColor", (255,255,255))
        self._changeCursor: bool = kwargs.get("changeCursor", True)
        self._changeCursor: bool = kwargs.get("_changeCursor", self._changeCursor)
        self.checked = kwargs.get("checked", False)

        if self._size < 16:
            self._size = 16

        self.hide = kwargs.get("hide", False)
        self.name = kwargs.get("name", None)
        self.z_index = kwargs.get("z_index", None)
        self.disable = kwargs.get("disable", False)

        self.clickEvent = None
        self.hoverEvent = None

        self._hoveringAction = False

        self._clicked = False
        self.clickedOutside = False

        self.rect = pygame.Rect(self._x, self._y, self._size, self._size)

        _allObjects.append(self)
        _clickableObjects.append(self)

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value: int):
        self._x = value
        self.rect.x = self._x

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value: int):
        self._y = value
        self.rect.y = self._y

    @property
    def changeCursor(self):
        return self._changeCursor

    @changeCursor.setter
    def changeCursor(self, value: bool):
        self._changeCursor = value

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value: int):
        self._size = value
        if self._size < 16:
            self._size = 16
        self.rect.width = self._size
        self.rect.height = self._size

    def _has_arguments(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters
        argument_names = [param.name for param in parameters.values()]
        if len(argument_names) > 0:
            return True
        else:
            return False

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def mouse_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                return True
            
    def mouse_hovering(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True

    def draw(self, surface=None):
        global _clickedObjects, _changingCursor
        if surface == None:
            surface = _windowObject.screen
        
        if not(self.hide):
            if not(self.disable):
                pos = pygame.mouse.get_pos()

                if not(self.rect.collidepoint(pos)) and pygame.mouse.get_pressed()[0] == 1:
                    self.clickedOutside = True
                elif pygame.mouse.get_pressed()[0] == 0:
                    self.clickedOutside = False

                if self.z_index == None:
                    self._hoveringAction = True

                if self.rect.collidepoint(pos):
                    if not(_clickedObjects.__contains__(self)):
                        _clickedObjects.append(self)
                    if self._hoveringAction:
                        if self._changeCursor:
                            _changingCursor = pygame.SYSTEM_CURSOR_HAND
                        if self.hoverEvent != None:
                            if self._has_arguments(self.hoverEvent):
                                self.hoverEvent(self)
                            else:
                                self.hoverEvent()
                        if pygame.mouse.get_pressed()[0] == 1 and not(self.clickedOutside):
                            self._clicked = True

                        if not(self.clickedOutside):
                            if pygame.mouse.get_pressed()[0] == 0 and self._clicked:
                                self._clicked = False
                                if self.clickEvent != None:
                                    if self._has_arguments(self.clickEvent):
                                        self.clickEvent(self)
                                    else:
                                        self.clickEvent()


                                self.checked = not(self.checked)
                                return True
                    else:
                        self._clicked = False
                else:
                    self._clicked = False

            if not(self.checked):
                pygame.draw.rect(surface, self.background, self.rect, width=1)
            else:
                pygame.draw.rect(surface, self.background, self.rect)

                pygame.draw.line(surface, self.checkSignColor, (self.x + (self.size * 0.25), self.y + (self.size // 2)), (self.x + (self.size // 2), self.rect.bottom - (self.size * 0.25)), width=3)
                pygame.draw.line(surface, self.checkSignColor, (self.x + (self.size // 2), self.rect.bottom - (self.size * 0.25)), (self.rect.right - (self.size * 0.25), self.y + (self.size * 0.25)), width=3)

class Line():
    def __init__(self, **kwargs):
        self._startX = kwargs.get("startX")
        self._startX = kwargs.get("_startX", self._startX)
        self._startY = kwargs.get("startY")
        self._startY = kwargs.get("_startY", self._startY)
        self._endX = kwargs.get("endX")
        self._endX = kwargs.get("_endX", self._endX)
        self._endY = kwargs.get("endY")
        self._endY = kwargs.get("_endY", self._endY)
        self.color = kwargs.get("color", (255,255,255))
        self.width = kwargs.get("width", 2)

        self.hide = kwargs.get("hide", False)
        self.name = kwargs.get("name", None)
        self.z_index = kwargs.get("z_index", None)

        self.rect = pygame.Rect(0,0,0,0)
        self._setRectSize()

    def _setRectSize(self):
        posX = [self._startX, self._endX]
        posY = [self._startY, self._endY]

        width = max(posX) - min(posX)
        height = max(posY) - min(posY)

        self.rect = pygame.Rect(min(posX), min(posY), width, height)

    @property
    def startX(self):
        return self._startX
    
    @startX.setter
    def startX(self, value: int):
        self._startX = value
        self._setRectSize()

    @property
    def startY(self):
        return self._startY
    
    @startY.setter
    def startY(self, value: int):
        self._startY = value
        self._setRectSize()

    @property
    def endX(self):
        return self._endX
    
    @endX.setter
    def endX(self, value: int):
        self._endX = value
        self._setRectSize()

    @property
    def endY(self):
        return self._endY
    
    @endY.setter
    def endY(self, value: int):
        self._endY = value
        self._setRectSize()

    def draw(self, surface=None):
        if surface == None:
            surface = _windowObject.screen

        pygame.draw.line(surface, self.color, (self.startX, self.startY), (self.endX, self.endY), width=self.width)

class CustomButton():
    def __init__(self, **kwargs):
        global _allObjects, _clickableObjects
        self._x = kwargs.get("x", 0)
        self._x = kwargs.get("_x", self._x)
        self._y = kwargs.get("y", 0)
        self._y = kwargs.get("_y", self._y)
        self.background = kwargs.get("background", (50,50,50))
        self._text = kwargs.get("text", "")
        self._text = kwargs.get("_text", self._text)
        self._textColor: tuple = kwargs.get("textColor", (255,255,255))
        self._textColor: tuple = kwargs.get("_textColor", self._textColor)

        self.hoverBackground = kwargs.get("hoverBackground", self.background)
        self.activeBackground = kwargs.get("activeBackground", self.hoverBackground)
        self.hoverTextColor = kwargs.get("hoverTextColor", self.textColor)
        self.activeTextColor = kwargs.get("activeTextColor", self.hoverTextColor)
        self.outlineColor = kwargs.get("outlineColor", self.background)
        self.hoverOutlineColor = kwargs.get("hoverOutlineColor", self.outlineColor)
        self.activeOutlineColor = kwargs.get("activeOutlineColor", self.hoverOutlineColor)

        self.textColor0 = self.textColor
        self.background0 = self.background
        self.outlineColor0 = self.outlineColor

        self.clickAnimation = kwargs.get("clickAnimation", False)

        self._fontName: str = kwargs.get("fontName", defaultFont)
        self._fontName: str = kwargs.get("_fontName", self._fontName)
        self._fontSize: int = kwargs.get("fontSize", 14)
        self._fontSize: int = kwargs.get("_fontSize", self._fontSize)

        self.textOffsetX = kwargs.get("textOffsetX", 0)
        self.textOffsetY = kwargs.get("textOffsetY", 0)

        self.thickness = kwargs.get("thickness", 2)

        self.disable = kwargs.get("disable", False)

        self._textLabel = Label(text=self._text, fontSize=self._fontSize, fontName=self._fontName, textColor=self._textColor,
                                x=-1000, y=-1000)
    
        self._changeCursor = kwargs.get("changeCursor", True)
        self._changeCursor = kwargs.get("_changeCursor", self._changeCursor)

        self._points: list = kwargs.get("points", [])
        if self._points == [] or len(self._points) < 3:
            self._points = [(15,0), (125,0), (125,20), (110,35), (0,35), (0,15)]

        self._clicked = False
        self.clickedOutside = False
        self.clickEvent = None
        self.hoverEvent = None
        self._clicked = False
        self._hoveringAction = False

        self.hide = kwargs.get("hide", False)
        self.name = kwargs.get("name", None)
        self.z_index = kwargs.get("z_index", None)
        self.disable = kwargs.get("disable", False)

        self.rect = pygame.Rect(0,0,0,0)
        if self._points != []:
            self._setPos()

        _allObjects.append(self)
        _clickableObjects.append(self)

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value: int):
        self._x = value
        self._setPos()

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value: int):
        self._y = value
        self._setPos()

    @property
    def points(self):
        return self._points
    
    @points.setter
    def points(self, value: list):
        self._points = value

    @property
    def changeCursor(self):
        return self._changeCursor

    @changeCursor.setter
    def changeCursor(self, value: bool):
        self._changeCursor = value

    @property
    def fontSize(self):
        return self._fontSize
    
    @fontSize.setter
    def fontSize(self, value: int):
        self._fontSize = value
        self._fontLabel.fontSize = self._fontSize

    @property
    def fontName(self):
        return self._fontName

    @fontName.setter
    def fontName(self, value: str):
        self._fontName = value
        self._fontLabel.fontName = self._fontName

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self._fontLabel.text = self._text

    @property
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, value: tuple):
        self._textColor = value
        self._fontLabel.textColor = self._textColor

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def _has_arguments(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters
        argument_names = [param.name for param in parameters.values()]
        if len(argument_names) > 0:
            return True
        else:
            return False

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def mouse_hovering(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        
    def mouse_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

    def _setPos(self):
        yPos = []
        xPos = []
        for index, item in enumerate(self._points):
            xPos.append(self._points[index][0])
            yPos.append(self._points[index][1])
        
        width = (max(xPos) - min(xPos)+self.thickness)
        height = (max(yPos) - min(yPos)+self.thickness)

        self.rect = pygame.Rect(self.x, self.y, width, height)

    def draw(self, surface=None):
        global _changingCursor
        if surface == None:
            surface = _windowObject.screen

        if not(self.hide):
            pos = pygame.mouse.get_pos()
            points = []
            for point in self._points:
                points.append(point)

            points = [(p[0]+self._x, p[1]+self._y) for p in points]
            if self.clickAnimation and self._clicked:
                points = [(p[0]+1, p[1]+1) for p in points]

            pygame.draw.polygon(surface, self.background0, points)
            
            for index, item in enumerate(points):
                if index+1 < len(points):
                    pygame.draw.line(surface, self.outlineColor0, (points[index]), (points[index+1]), width=self.thickness)
                else:
                    pygame.draw.line(surface, self.outlineColor0, (points[index]), (points[0]), width=self.thickness)

            if self._text != "":
                if not(self._clicked):
                    self._textLabel.x = self._x + (self.rect.width - self._textLabel.rect.width) // 2 + self.textOffsetX
                    self._textLabel.y = self._y + (self.rect.height - self._textLabel.rect.height) // 2 + self.textOffsetY
                elif self.clickAnimation:
                    self._textLabel.x = self._x+1 + (self.rect.width - self._textLabel.rect.width) // 2 + self.textOffsetX
                    self._textLabel.y = self._y+1 + (self.rect.height - self._textLabel.rect.height) // 2 + self.textOffsetY
                self._textLabel.textColor = self.textColor0
                self._textLabel.draw(surface)

            if not(self.disable):
                if not(self.rect.collidepoint(pos)) and pygame.mouse.get_pressed()[0] == 1:
                    self.clickedOutside = True
                elif pygame.mouse.get_pressed()[0] == 0:
                    self.clickedOutside = False

                if self.z_index == None:
                    self._hoveringAction = True

                if self.rect.collidepoint(pos):
                    if not(_clickedObjects.__contains__(self)):
                        _clickedObjects.append(self)
                    if self._hoveringAction:
                        if self._changeCursor:
                            _changingCursor = pygame.SYSTEM_CURSOR_HAND
                        if self.hoverEvent != None:
                            if self._has_arguments(self.hoverEvent):
                                self.hoverEvent(self)
                            else:
                                self.hoverEvent()

                        if not(self._clicked):
                            self.background0 = self.hoverBackground
                            self.textColor0 = self.hoverTextColor
                            self.outlineColor0 = self.hoverOutlineColor

                        if pygame.mouse.get_pressed()[0] == 1 and not(self.clickedOutside):
                            self._clicked = True
                            self.background0 = self.activeBackground
                            self.textColor0 = self.activeTextColor
                            self.outlineColor0 = self.activeOutlineColor

                        if not(self.clickedOutside):
                            if pygame.mouse.get_pressed()[0] == 0 and self._clicked:
                                self._clicked = False
                                if self.clickEvent != None:
                                    if self._has_arguments(self.clickEvent):
                                        self.clickEvent(self)
                                    else:
                                        self.clickEvent()
                                
                                return True
                                
                    else:
                        self.background0 = self.background
                        self.textColor0 = self.textColor
                        self.outlineColor0 = self.outlineColor
                        self._clicked = False
                else:
                    self.background0 = self.background
                    self.textColor0 = self.textColor
                    self.outlineColor0 = self.outlineColor
                    self._clicked = False

class Slider():
    def __init__(self, **kwargs):
        global _allObjects
        self._x = kwargs.get("x", 0)
        self._x = kwargs.get("_x", self._x)
        self._y = kwargs.get("y", 0)
        self._y = kwargs.get("_y", self._y)
        self._width = kwargs.get("width", 100)
        self._width = kwargs.get("_width", self._width)
        self._height = kwargs.get("height", 6)
        self._height = kwargs.get("_height", self._height)
        self.background = kwargs.get("background", (60,60,60))
        self.valueBackground = kwargs.get("valueBackground", (160,160,160))
        self.sliderColor = kwargs.get("sliderColor", (235,235,235))
        self.borderRadius = kwargs.get("borderRadius", 3)
        self._valueTextColor = kwargs.get("valueTextColor", (235,235,235))
        self._valueTextColor = kwargs.get("_valueTextColor", self._valueTextColor)
        self._valueSize = kwargs.get("valueSize", 15)
        self._valueSize = kwargs.get("_valueSize", self._valueSize)
        self._fontName = kwargs.get("fontName", defaultFont)
        self._fontName = kwargs.get("_fontName", self._fontName)
        self._valuePosition = kwargs.get("valuePosition", "left")
        self._valuePosition = kwargs.get("_valuePosition", self._valuePosition)
        self._valueOffsetX = kwargs.get("valueOffsetX", 0)
        self._valueOffsetX = kwargs.get("_valueOffsetX", self._valueOffsetX)
        self._valueOffsetY = kwargs.get("valueOffsetY", 0)
        self._valueOffsetY = kwargs.get("_valueOffsetY", self._valueOffsetY)

        self._sliderType = kwargs.get("sliderType", 2)
        self._sliderType = kwargs.get("_sliderType", self._sliderType)
        self._scrollType = kwargs.get("scrollType", "horizontal")
        self._scrollType = kwargs.get("_scrollType", self._scrollType)

        self._sliderWidth = kwargs.get("sliderWidth", 8)
        self._sliderWidth = kwargs.get("_sliderWidth", self._sliderWidth)
        self._sliderHeight = kwargs.get("sliderHeight", self._height + 4)
        self._sliderHeight = kwargs.get("_sliderHeight", self._sliderHeight)

        self._sliderBallSize = kwargs.get("sliderBallSize", 17)
        self._sliderBallSize = kwargs.get("_sliderBallSize", self._sliderBallSize)

        self._value = kwargs.get("value", 0)
        self._value = kwargs.get("_value", self._value)
        self._maxValue = kwargs.get("maxValue", 100)
        self._maxValue = kwargs.get("_maxValue", self._maxValue)
        if self._value > self._maxValue:
            self._value = self._maxValue
        elif self._value < 0:
            self._value = 0
        self.showValue = kwargs.get("showValue", True)

        self.clickEvent = None
        self.hoverEvent = None

        self.name = kwargs.get("name", None)
        self.z_index = kwargs.get("z_index", None)
        self.hide = kwargs.get("hide", False)
        self.disable = kwargs.get("disable", False)

        self._sliderOffsetX = None
        self._sliderOffsetY = None
        self._sliding = False

        self.sliderRect = pygame.Rect(self._x, self._y, self._sliderWidth, self._sliderHeight)
        self.rect = pygame.Rect(self._x, self._y+(self.sliderRect.height // 2) - self._height // 2, self._width, self._height)
        self.valueRect = pygame.Rect(self._x, self._y+(self.sliderRect.height // 2) - self._height // 2, self._width, self._height)
        self.valueLabel = Label(text=str(self._value), textColor=self._valueTextColor, fontSize=self._valueSize, fontName=self._fontName)
        self._setSliderStateType(True)
        self._setValueTextPosition()

        _allObjects.append(self)

    def _setValueTextPosition(self):
        if self._valuePosition == "left":
            if self._scrollType == "horizontal":
                self.valueLabel.x = self.rect.x - (self.valueLabel.rect.width+10) + self._valueOffsetX
                self.valueLabel.y = self.rect.y - (self.valueLabel.rect.height / 2) + (self.rect.height / 2)+self._valueOffsetY
            elif self._scrollType == "vertical":
                self.valueLabel.x = self.rect.x - (self.valueLabel.rect.width+10) + self._valueOffsetX
                self.valueLabel.y = self.rect.y - (self.valueLabel.rect.height / 2) + (self.rect.height / 2)+self._valueOffsetY
        elif self._valuePosition == "right":
            if self._scrollType == "horizontal":
                self.valueLabel.x = self.rect.right + 7 + self._valueOffsetX + self.sliderRect.width
                self.valueLabel.y = self.rect.y - (self.valueLabel.rect.height / 2) + (self.rect.height / 2)+self._valueOffsetY
            elif self._scrollType == "vertical":
                self.valueLabel.x = self.rect.right + 10 + self._valueOffsetX
                self.valueLabel.y = self.rect.y - (self.valueLabel.rect.height / 2) + (self.rect.height / 2)+self._valueOffsetY
        elif self._valuePosition == "top":
            if self._scrollType == "horizontal":
                self.valueLabel.x = self.rect.x - (self.valueLabel.rect.width / 2) + (self.rect.width / 2)+self._valueOffsetX
                self.valueLabel.y = self.rect.y - (self.valueLabel.rect.height+10) + self._valueOffsetY
            elif self._scrollType == "vertical":
                self.valueLabel.x = self.rect.x - (self.valueLabel.rect.width / 2) + (self.rect.width / 2)
                self.valueLabel.y = self.rect.y - (self.valueLabel.rect.height+7) + self._valueOffsetY - self.sliderRect.height
        elif self._valuePosition == "bottom":
            if self._scrollType == "horizontal":
                self.valueLabel.x = self.rect.x - (self.valueLabel.rect.width / 2) + (self.rect.width / 2)+self._valueOffsetX
                self.valueLabel.y = self.rect.bottom+10+self._valueOffsetY
            elif self._scrollType == "vertical":
                self.valueLabel.x = self.rect.x - (self.valueLabel.rect.width / 2) + (self.rect.width / 2)+self._valueOffsetX
                self.valueLabel.y = self.rect.bottom + 10 + self._valueOffsetY

    @property
    def valueTextColor(self):
        return self._valueTextColor
    
    @valueTextColor.setter
    def valueTextColor(self, value: tuple):
        self._valueTextColor = value
        self.valueLabel.textColor = self._valueTextColor

    @property
    def valueOffsetX(self):
        return self._valueOffsetX

    @valueOffsetX.setter
    def valueOffsetX(self, value: int):
        self._valueOffsetX = value
        self._setValueTextPosition()

    @property
    def valueOffsetY(self):
        return self._valueOffsetY

    @valueOffsetY.setter
    def valueOffsetY(self, value: int):
        self._valueOffsetY = value
        self._setValueTextPosition()

    @property
    def fontName(self):
        return self._fontName

    @fontName.setter
    def fontName(self, value: int):
        self._fontName = value
        self.valueLabel.fontName = self._fontName
        self._setValueTextPosition()

    @property
    def valueSize(self):
        return self._valueSize
    
    @valueSize.setter
    def valueSize(self, value: int):
        self._valueSize = value
        self.valueLabel.fontSize = self._valueSize
        self._setValueTextPosition()

    @property
    def valuePosition(self):
        return self._valuePosition

    @valuePosition.setter
    def valuePosition(self, value: str):
        positions = ["left", "top", "right", "bottom"]
        self._valuePosition = value if positions.__contains__(value) else "left"
        self._setValueTextPosition()

    @property
    def sliderType(self):
        return self._sliderType
    
    @sliderType.setter
    def sliderType(self, value: int):
        self._sliderType = value
        if self._sliderType > 2:
            self._sliderType = 2
        elif self._sliderType < 1:
            self._sliderType = 1

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value: int):
        self._x = value
        self._setSliderStateType(False,True)

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value: int):
        self._y = value
        self._setSliderStateType(False,True)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value
        self.rect.width = self._width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value
        self.rect.height = self._height

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: int):
        self._value = value
        if self._value > self._maxValue:
            self._value = self._maxValue
        elif self._value < 0:
            self._value = 0

        if self._scrollType == "horizontal":
            self.sliderRect.x = self._x + (self.rect.width / self._maxValue) * self._value
        elif self._scrollType == "vertical":
            self.sliderRect.bottom = self.rect.bottom - (self.rect.height / self._maxValue) * self._value
        
    @property
    def maxValue(self):
        return self._maxValue
    
    @maxValue.setter
    def maxValue(self, value: int):
        self._maxValue = value
        if self._maxValue < self._value:
            self.value = self._maxValue

    @property
    def sliderWidth(self):
        return self._sliderWidth

    @sliderWidth.setter
    def sliderWidth(self, value: int):
        self._sliderWidth = value
        self._setSliderStateType(False)

    @property
    def sliderHeight(self):
        return self._sliderHeight

    @sliderHeight.setter
    def sliderHeight(self, value: int):
        self._sliderHeight = value
        self._setSliderStateType(False)

    def _setSliderStateType(self, init=None, changingPos=False):
        if (init == None and changingPos == False):
            self._width, self._height = self._height, self._width
            self._sliderWidth, self._sliderHeight = self._sliderHeight, self._sliderWidth

        if self._scrollType == "horizontal":
            self.sliderRect = pygame.Rect(self._x, self._y, self._sliderWidth, self._sliderHeight)
            self.rect = pygame.Rect(self._x, self._y+(self.sliderRect.height // 2) - self._height // 2, self._width, self._height)
            self.valueRect = pygame.Rect(self._x, self._y+(self.sliderRect.height // 2) - self._height // 2, self._width, self._height)
            self.value = self._value

        elif self._scrollType == "vertical":
            self.rect = pygame.Rect(self._x+(self._sliderWidth // 2) - self._width // 2, self._y, self._width, self._height)
            self.sliderRect = pygame.Rect(self._x, self.rect.bottom-(self._sliderHeight), self._sliderWidth, self._sliderHeight)
            self.valueRect = pygame.Rect(self._x+(self._sliderWidth // 2) - self._width // 2, self._y, self._width, self._height)
            self.value = self._value
        
        self._setValueTextPosition()

    @property
    def scrollType(self):
        return self._scrollType

    @scrollType.setter
    def scrollType(self, value: str):
        if self._scrollType != value:
            self._scrollType = value if (value == "horizontal" or value == "vertical") else "horizontal"
            self._setSliderStateType()

    @property
    def sliderBallSize(self):
        return self._sliderBallSize
    
    @sliderBallSize.setter
    def sliderBallSize(self, value: int):
        self._sliderBallSize = value

    def _has_arguments(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters
        argument_names = [param.name for param in parameters.values()]
        if len(argument_names) > 0:
            return True
        else:
            return False

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def mouse_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                return True
            
    def mouse_hovering(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True

    def draw(self, surface=None):
        
        if surface == None:
            surface = _windowObject.screen

        if not(self.hide):
            pos = pygame.mouse.get_pos()
            if self._scrollType == "horizontal":
                self.valueRect.x = self.rect.x
                if self._sliderType == 1:
                    self.valueRect.width = (self.sliderRect.x - self.rect.x) + self.sliderRect.width
                elif self._sliderType == 2:
                    self.valueRect.width = (self.sliderRect.x - self.rect.x) + (self.sliderRect.width / 2)
            elif self._scrollType == "vertical":
                if self._sliderType == 1:
                    self.valueRect.height = (self.rect.bottom - self.sliderRect.y - (self.sliderRect.height // 2))
                elif self._sliderType == 2:
                    self.valueRect.height = (self.rect.bottom - self.sliderRect.y - (self.sliderRect.height // 2))
                self.valueRect.bottom = self.rect.bottom
            self.valueLabel.text = str(self._value)
            self._setValueTextPosition()

            if not(self.disable):
                if (pygame.mouse.get_pressed()[0] == 1 and self.sliderRect.collidepoint(pos)) or (pygame.mouse.get_pressed()[0] == 1 and self._sliding):
                    self._sliding = True
                    if self._scrollType == "horizontal":
                        if self._sliderOffsetX == None:
                            self._sliderOffsetX = pos[0] - self.sliderRect.x
                        self.sliderRect.x = pos[0] - self._sliderOffsetX
                        self.value = round((self._maxValue / self.rect.width) * (self.sliderRect.x - self.rect.x))
                        if self.sliderRect.x < self._x:
                            self.sliderRect.x = self._x
                            self.value = 0
                        elif self.sliderRect.x > self.rect.right:
                            self.sliderRect.x = self.rect.right
                            self.value = self._maxValue

                    elif self._scrollType == "vertical":
                        if self._sliderOffsetY == None:
                            self._sliderOffsetY = self.sliderRect.y - pos[1]
                        self.sliderRect.y = pos[1] + self._sliderOffsetY
                        self.value = round((self._maxValue / self.rect.height) * (self.rect.bottom-self.sliderRect.bottom))
                        if self.sliderRect.bottom > self.rect.bottom:
                            self.sliderRect.bottom = self.rect.bottom
                            self.value = 0
                        elif self.sliderRect.bottom < self.rect.y:
                            self.sliderRect.bottom = self.rect.y
                            self.value = self._maxValue

                elif pygame.mouse.get_pressed()[0] == 1 and self.rect.collidepoint(pos):
                    if self._scrollType == "horizontal":
                        self.sliderRect.x = pos[0] - (self.sliderRect.width / 2)
                        self.value = round((self._maxValue / self.rect.width) * (self.sliderRect.x - self.rect.x))
                    elif self._scrollType == "vertical":
                        self.sliderRect.bottom = pos[1] + (self.sliderRect.height / 2)
                        self.value = round((self._maxValue / self.rect.height) * (self.rect.bottom-self.sliderRect.bottom))

            if pygame.mouse.get_pressed()[0] == 0:
                self._sliderOffsetX = None
                self._sliderOffsetY = None
                self._sliding = False
            pygame.draw.rect(surface, self.background, self.rect, 0, self.borderRadius)
            pygame.draw.rect(surface, self.valueBackground, self.valueRect, 0, self.borderRadius)
            
            if self._sliderType == 1:
                pygame.draw.rect(surface, self.sliderColor, self.sliderRect)
                self.sliderRect.width = self._sliderWidth
                self.sliderRect.height = self._sliderHeight
                if not(self._sliding):
                    if self._scrollType == "horizontal":
                        self.sliderRect.y = self.rect.y - (self.sliderRect.height // 2) + self.rect.height // 2
                        if not(self._sliding):
                            self.sliderRect.x = self.rect.x + (self.rect.width / self._maxValue) * self._value
                            self.sliderRect.top = self.rect.y - (self.sliderRect.height / 2) + (self.rect.height / 2)
                    elif self._scrollType == "vertical":
                        self.valueRect.y = self.sliderRect.y - (self.sliderRect.height // 2)
                        if not(self._sliding):
                            self.sliderRect.bottom = self.rect.bottom - (self.rect.height / self._maxValue) * self._value
                            self.sliderRect.x = self.rect.x - (self.sliderRect.width / 2) + (self.rect.width / 2)
            else:
                self.sliderRect.width = self._sliderBallSize
                self.sliderRect.height = self._sliderBallSize
                if self._scrollType == "horizontal":
                    self.sliderRect.y = self.rect.y - (self.sliderRect.height // 2) + self.rect.height // 2
                    if not(self._sliding):
                        self.sliderRect.x = self.rect.x + (self.rect.width / self._maxValue) * self._value
                        self.sliderRect.top = self.rect.y - (self.sliderRect.height / 2) + (self.rect.height / 2)
                elif self._scrollType == "vertical":
                    self.valueRect.y = self.sliderRect.y - (self.sliderRect.height // 2)
                    if not(self._sliding):
                        self.sliderRect.bottom = self.rect.bottom - (self.rect.height / self._maxValue) * self._value
                        self.sliderRect.x = self.rect.x - (self.sliderRect.width / 2) + (self.rect.width / 2)

                circle_radius = (self._sliderBallSize // 2)-1
                circle_center = (self.sliderRect.x + self._sliderBallSize // 2-1, self.sliderRect.y + self._sliderBallSize // 2)
                gfxdraw.filled_circle(surface, circle_center[0], circle_center[1], circle_radius, self.sliderColor)
                gfxdraw.aacircle(surface, circle_center[0], circle_center[1], circle_radius, self.sliderColor)

            if self.showValue:
                self.valueLabel.draw()

class TextBox():
    def __init__(self, **kwargs):
        global _allObjects, _textBoxList
        self._x = kwargs.get("x", 0)
        self._x = kwargs.get("_x", self._x)
        self._y = kwargs.get("y", 0)
        self._y = kwargs.get("_y", self._y)
        self._width = kwargs.get("width", 125)
        self._width = kwargs.get("_width", self._width)
        self._height = kwargs.get("height", 35)
        self._height = kwargs.get("_height", self._height)
        self._text = kwargs.get("text", "")
        self._text = kwargs.get("_text", self._text)
        self._placeholderText = kwargs.get("placeholderText", "Text")
        self._placeholderText = kwargs.get("_placeholderText", self._placeholderText)
        self.background = kwargs.get("background", (50,50,50))
        self.activeBackground = kwargs.get("activeBackground", (80,80,80))
        self.outlineColor = kwargs.get("outlineColor", self.background)
        self._outlineWidth = kwargs.get("outlineWidth", 0)
        self._outlineWidth = kwargs.get("_outlineWidth", self._outlineWidth)
        self.activeOutlineColor = kwargs.get("activeOutlineColor", self.activeBackground) 
        self._textColor = kwargs.get("textColor", (235,235,235))
        self._textColor = kwargs.get("_textColor", self._textColor)
        self._placeholderColor = kwargs.get("placeholderColor", (180,180,180))
        self._placeholderColor = kwargs.get("_placeholderColor", self._placeholderColor)
        self._activeTextColor = kwargs.get("activeTextColor", (235,235,235))
        self._activeTextColor = kwargs.get("_activeTextColor", self._activeTextColor)
        self.cursorColor = kwargs.get("cursorColor", (235,235,235))
        self.highlightColor = kwargs.get("highlightColor", (0,100,255))
        self._cursorBlinking = kwargs.get("cursorBlinking", True)
        self._cursorBlinking = kwargs.get("_cursorBlinking", self._cursorBlinking)
        self.borderRadius = kwargs.get("borderRadius", 0)
        self.textColor0 = self._placeholderColor
        self.activeTextColor0 = self._activeTextColor
        self.background0 = self.background
        self.activeBackground0 = self.activeBackground
        self.activeOutlineColor0 = self.activeOutlineColor

        self.maxCharacters = kwargs.get("maxCharacters", 9999)

        self.lettersOnly = kwargs.get("lettersOnly", False)
        self.numbersOnly = kwargs.get("numbersOnly", False)
        self.exceptionChars = kwargs.get("exceptionChars", [])
        self.acceptedFormat = kwargs.get("acceptedFormat", None)

        self._fontName = kwargs.get("fontName", defaultFont)
        self._fontName = kwargs.get("_fontName", self._fontName)
        self._fontSize = kwargs.get("fontSize", 14)
        self._fontSize = kwargs.get("_fontSize", self._fontSize)

        self._changeCursor: bool = kwargs.get("changeCursor", True)
        self._changeCursor: bool = kwargs.get("_changeCursor", self._changeCursor)

        self._active = False
        self._bold = kwargs.get("bold", False)
        self._bold = kwargs.get("_bold", self._bold)

        self.hide = kwargs.get("hide", False)
        self.name = kwargs.get("name", None)
        self.z_index = kwargs.get("z_index", None)
        self.disable = kwargs.get("disable", False)

        self.clicked = False
        self.clickedOutside = False

        self.clickEvent = None
        self.hoverEvent = None

        self.currentLetter = 0

        self.textPosition = 4
        
        self.ctrlA = KeyBindCombination(key1=pygame.K_LCTRL, key2=pygame.K_a)
        self.ctrlV = KeyBindCombination(key1=pygame.K_LCTRL, key2=pygame.K_v)
        self.ctrlC = KeyBindCombination(key1=pygame.K_LCTRL, key2=pygame.K_c)
        self.ctrlX = KeyBindCombination(key1=pygame.K_LCTRL, key2=pygame.K_x)

        self.cursorBlinkingTimer = Timer(time=0.50)
        self.cursorBlinkingTimer.start()
        self._showCursor = True

        self.backspaceTimer = Timer(time=0.025)
        self.leftArrowTimer = Timer(time=0.040)
        self.rightArrowTimer = Timer(time=0.040)

        self._leftArrowTickTimer = 0
        self._rightArrowTickTimer = 0
        self._backspaceTickTimer = 0

        self.highlighted = False
        self.highlightedLettersToLeft = []
        self.highlightedLettersToRight = []
        self.lastLetterIndex = None
        self.highlightedLastLetter = None
        self.holdingShift = False

        self.font = None
        if self._fontName[-4:] == ".ttf":
            self.font = pygame.font.Font(self._fontName, self._fontSize)
        else:
            self.font = pygame.font.SysFont(self._fontName, self._fontSize, bold=self.bold)
        self.textLabel = self.font.render(self._text, True, (self._textColor))

        self.textSurface = pygame.Surface((self._width, self.textLabel.get_height()), pygame.SRCALPHA)
        self.cursorSurface = pygame.Surface((2, self.textLabel.get_height()))
        self.highlightSurface = pygame.Surface((0,self.textLabel.get_height()), pygame.SRCALPHA)

        self.textBoxRect = pygame.Rect(self._x, self._y, self._width, self._height)
        self.rect = pygame.Rect(self._x-self.outlineWidth, self._y-self.outlineWidth, self._width+(self.outlineWidth * 2), self._height + (self.outlineWidth * 2))

        self.active = self._active

        _allObjects.append(self)
        _textBoxList.append(self)
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value
        self.rect.x = self._x-self._outlineWidth
        self.textBoxRect.x = self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value
        self.rect.y = self._y-self._outlineWidth
        self.textBoxRect.y = self._y

    @property
    def cursorBlinking(self):
        return self._cursorBlinking
    
    @cursorBlinking.setter
    def cursorBlinking(self, value: bool):
        self._cursorBlinking = value
        if self._cursorBlinking:
            if not(self.cursorBlinkingTimer.run):
                self.cursorBlinkingTimer.start()
        else:
            self.cursorBlinkingTimer.stop()
            self._showCursor = True

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value: bool):
        self._active = value
        if self._active:
            self.textColor0 = self.textColor
            self.background0 = self.activeBackground
            self.outlineColor0 = self.activeOutlineColor
        else:
            if self._text == "" or self._text == self._placeholderText:
                self.textColor0 = self.placeholderColor
            else:
                self.textColor0 = self.textColor
            self.background0 = self.background
            self.outlineColor0 = self.outlineColor
            self.highlightSurface = pygame.Surface((0,self.textLabel.get_height()), pygame.SRCALPHA)

    @property
    def changeCursor(self):
        return self._changeCursor

    @changeCursor.setter
    def changeCursor(self, value: bool):
        self._changeCursor = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self.active = self._active
        if not(self.active):
            if self._text == self._placeholderText:
                self.currentLetter = 0
        if self._text == "":
            self.currentLetter = 0

    @property
    def placeholderText(self):
        return self._placeholderText

    @placeholderText.setter
    def placeholderText(self, value: str):
        self._placeholderText = value

    @property
    def bold(self):
        return self._bold

    @bold.setter
    def bold(self, value: bool):
        self._bold = value
        if self._fontName[-4:] == ".ttf":
            self.font = pygame.font.Font(self._fontName, self._fontSize)
        else:
            self.font = pygame.font.SysFont(self._fontName, self._fontSize, bold=self.bold)

    @property
    def outlineWidth(self):
        return self._outlineWidth
    
    @outlineWidth.setter
    def outlineWidth(self, value: int):
        self._outlineWidth = value
        self.rect.x = self._x-self.outlineWidth
        self.rect.y = self._y-self.outlineWidth
        self.rect.width = self._width+(self.outlineWidth*2)
        self.rect.height = self._height+(self.outlineWidth*2)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: str):
        self._width = value
        self.rect.width = self._width+(self.outlineWidth*2)
        self.textBoxRect.width = self._width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: str):
        self._height = value
        self.rect.height = self._height+(self.outlineWidth*2)
        self.textBoxRect.height = self._height

    @property
    def textColor(self):
        return self._textColor

    @textColor.setter
    def textColor(self, value: tuple):
        self._textColor = value

    @property
    def placeholderColor(self):
        return self._placeholderColor

    @placeholderColor.setter
    def placeholderColor(self, value: tuple):
        self._placeholderColor = value

    @property
    def fontName(self):
        return self._fontName

    @fontName.setter
    def fontName(self, value: tuple):
        self._fontName = value
        if self._fontName[-4:] == ".ttf":
            self.font = pygame.font.Font(self._fontName, self._fontSize)
        else:
            self.font = pygame.font.SysFont(self._fontName, self._fontSize, bold=self.bold)
        if not(self._active):
            self.textLabel = self.font.render(self._text, True, (self._textColor))
        else:
            self.textLabel = self.font.render(self._text, True, (self._activeTextColor))

    @property
    def fontSize(self):
        return self._fontSize

    @fontSize.setter
    def fontSize(self, value: tuple):
        self._fontSize = value
        self.fontName = self._fontName
        self.textSurface = pygame.Surface((self._width, self.textLabel.get_height()), pygame.SRCALPHA)

    @property
    def changeCursor(self):
        return self._changeCursor

    @changeCursor.setter
    def changeCursor(self, value: bool):
        self._changeCursor = value

    def _has_arguments(self, function):
        signature = inspect.signature(function)
        parameters = signature.parameters
        argument_names = [param.name for param in parameters.values()]
        if len(argument_names) > 0:
            return True
        else:
            return False

    def loadEvents(self, func, ev):
        if callable(func):
            if ev == "clickEvent":
                self.clickEvent = func
            elif ev == "hoverEvent":
                self.hoverEvent = func

    def mouse_click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

    def mouse_hovering(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True

    def get_enter_press(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] and self.active:
            self.active = False
            self.background0 = self.background
            self.outlineColor0 = self.outlineColor
            return True

    def _arrowKeyLeftHighlight(self):
        if self.highlightedLastLetter == None:
            self.highlightedLastLetter = self.currentLetter+1
            self.highlighted = True
            highlightSurfaceWidth = self.font.size(self._text[self.currentLetter:self.highlightedLastLetter])[0]
            self.highlightSurface = pygame.Surface((highlightSurfaceWidth, self.textLabel.get_height()), pygame.SRCALPHA)
        else:
            highlightSurfaceWidth = 0
            if self.currentLetter < self.highlightedLastLetter:
                highlightSurfaceWidth = self.font.size(self._text[self.currentLetter:self.highlightedLastLetter])[0]
            else:
                highlightSurfaceWidth = self.font.size(self._text[self.highlightedLastLetter:self.currentLetter])[0]
            self.highlightSurface = pygame.Surface((highlightSurfaceWidth, self.textLabel.get_height()), pygame.SRCALPHA)

    def _arrowKeyRightHighlight(self):
        if self.highlightedLastLetter == None:
            self.highlightedLastLetter = self.currentLetter-1
            self.highlighted = True
            highlightSurfaceWidth = self.font.size(self._text[self.highlightedLastLetter:self.currentLetter])[0]
            self.highlightSurface = pygame.Surface((highlightSurfaceWidth, self.textLabel.get_height()), pygame.SRCALPHA)
        else:
            highlightSurfaceWidth = 0
            if self.currentLetter > self.highlightedLastLetter:
                highlightSurfaceWidth = self.font.size(self._text[self.highlightedLastLetter:self.currentLetter])[0]
            else:
                highlightSurfaceWidth = self.font.size(self._text[self.currentLetter:self.highlightedLastLetter])[0]
            self.highlightSurface = pygame.Surface((highlightSurfaceWidth, self.textLabel.get_height()), pygame.SRCALPHA)

    def _deleteHighlightedText(self):
        if self.highlighted:
            if self.currentLetter > self.highlightedLastLetter:
                previousTextLength = len(self.text)
                self.text = self.text[:self.highlightedLastLetter] + self.text[self.currentLetter:]
                self.currentLetter -= previousTextLength - len(self.text)
            elif self.currentLetter < self.highlightedLastLetter:
                self.text = self.text[:self.currentLetter] + self.text[self.highlightedLastLetter:]
            self.highlighted = False
            self.highlightedLastLetter = None
            if self.text == "":
                self.currentLetter = 0
            
        # Moving whole text to the right when it's too long to fit in the box
        if self.textPosition < 4:
            widthDiff = self.font.size(self._text[0:self.currentLetter])[0]
            self.textPosition = (self._width - 3) - widthDiff - 4
            if self.textPosition > 4:
                self.textPosition = 4  
        if self.textPosition > 4:
            self.textPosition = 4

    def _update(self, event):
        if event.type == pygame.TEXTINPUT and self.active and len(self._text) < self.maxCharacters:
            charToAdd = event.text

            # Adding char to text, no matter if it's letter or a number
            if (not(self.lettersOnly) and not(self.numbersOnly)) or self.exceptionChars.__contains__(charToAdd):
                self._deleteHighlightedText()
                self.text = self.text[:self.currentLetter] + charToAdd + self.text[self.currentLetter:]
                self.currentLetter += 1
                self.cursorBlinkingTimer.tick = 0
                self._showCursor = True

            # Adding char only if it's a number
            elif ((not(self.lettersOnly) and self.numbersOnly) and charToAdd.isdigit()) or self.exceptionChars.__contains__(charToAdd):
                self._deleteHighlightedText()
                self.text = self.text[:self.currentLetter] + charToAdd + self.text[self.currentLetter:]
                self.currentLetter += 1
                self.cursorBlinkingTimer.tick = 0
                self._showCursor = True
                
            # Adding chat only if it's a letter
            elif ((not(self.numbersOnly) and self.lettersOnly) and not(charToAdd.isdigit())) or self.exceptionChars.__contains__(charToAdd):
                self._deleteHighlightedText()
                self.text = self.text[:self.currentLetter] + charToAdd + self.text[self.currentLetter:]
                self.currentLetter += 1
                self.cursorBlinkingTimer.tick = 0
                self._showCursor = True

            # Moving whole text to the left when it's too long to fit in the box
            if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosition) + 6 > (self._width - 3):
                self.textPosition -= ((self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosition) + 6) - (self._width - 3))
                if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosition) == (self._width - 9):
                    self.textPosition += 4

        if self.active and not(self.disable):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.currentLetter-1 >= 0:
                        self.cursorBlinkingTimer.tick = 0
                        self._showCursor = True
                        if self.highlighted and not(self.holdingShift):
                            self.highlighted = False
                            self.highlightSurface = pygame.Surface((0, self.textLabel.get_height()), pygame.SRCALPHA)
                            if self.currentLetter > self.highlightedLastLetter:
                                self.currentLetter = self.highlightedLastLetter
                        else:
                            self.currentLetter -= 1
                        if self.holdingShift:
                            self._arrowKeyLeftHighlight()
                            if self.highlightedLastLetter == self.currentLetter:
                                self.highlighted = False
                                self.highlightSurface = pygame.Surface((0, self.textLabel.get_height()), pygame.SRCALPHA)
                        
                        # Moving whole text to the right when it's too long to fit in to the box
                        if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosition) + 6 < 4:
                            self.textPosition += abs((self.font.size(self._text[0:self.currentLetter])[0]) + self.textPosition)
                        if self.textPosition > 4:
                            self.textPosition = 4

                    elif self.highlighted and not(self.holdingShift):
                        self.highlighted = False
                        self.highlightSurface = pygame.Surface((0, self.textLabel.get_height()), pygame.SRCALPHA)
                        if self.currentLetter > self.highlightedLastLetter:
                            self.currentLetter = self.highlightedLastLetter
                        

                if event.key == pygame.K_RIGHT:
                    if self.currentLetter+1 <= len(self.text):
                        self.cursorBlinkingTimer.tick = 0
                        self._showCursor = True
                        if self.highlighted and not(self.holdingShift):
                            self.highlighted = False
                            self.highlightSurface = pygame.Surface((0, self.textLabel.get_height()), pygame.SRCALPHA)
                            if self.currentLetter < self.highlightedLastLetter:
                                self.currentLetter = self.highlightedLastLetter
                        else:
                            self.currentLetter += 1
                        if self.holdingShift:
                            self._arrowKeyRightHighlight()
                            if self.highlightedLastLetter == self.currentLetter:
                                self.highlighted = False
                                self.highlightSurface = pygame.Surface((0, self.textLabel.get_height()), pygame.SRCALPHA)
                        # Moving whole text to the left when it's too long to fit in the box
                        if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosition) + 6 > self._width - 3:
                            self.textPosition -= (self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosition) + 6) - (self._width - 3)
                            if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosition) == (self._width - 9):
                                self.textPosition += 4

                    elif self.highlighted and not(self.holdingShift):
                        self.highlighted = False
                        self.highlightSurface = pygame.Surface((0, self.textLabel.get_height()), pygame.SRCALPHA)
                        if self.currentLetter < self.highlightedLastLetter:
                            self.currentLetter = self.highlightedLastLetter

                if event.key == pygame.K_DELETE and self.text != "":
                    if self.highlighted:
                        self._deleteHighlightedText()

                if event.key == pygame.K_BACKSPACE and self.text != "":
                    self.cursorBlinkingTimer.tick = 0
                    self._showCursor = True
                    if self.currentLetter-1 >= 0 and not(self.highlighted):
                        self.text = self.text[:self.currentLetter-1] + self.text[self.currentLetter:]
                        self.currentLetter -= 1
                    elif self.highlighted:
                        if self.currentLetter > self.highlightedLastLetter:
                            previousTextLength = len(self.text)
                            self.text = self.text[:self.highlightedLastLetter] + self.text[self.currentLetter:]
                            self.currentLetter -= previousTextLength - len(self.text)
                        elif self.currentLetter < self.highlightedLastLetter:
                            self.text = self.text[:self.currentLetter] + self.text[self.highlightedLastLetter:]
                        self.highlighted = False
                        self.highlightedLastLetter = None

                    if self.currentLetter < 0:
                        self.currentLetter = 0
                        
                    # Moving whole text to the right when it's too long to fit in the box
                    if self.textPosition < 4:
                        widthDiff = self.font.size(self._text[0:self.currentLetter])[0]
                        self.textPosition = (self._width - 3) - widthDiff - 4
                        if self.textPosition > 4:
                            self.textPosition = 4  
                    if self.textPosition > 4:
                        self.textPosition = 4

                if event.key == pygame.K_LSHIFT:
                    self.holdingShift = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self._leftArrowTickTimer = 0
                    self.leftArrowTimer.stop()
                if event.key == pygame.K_RIGHT:
                    self._rightArrowTickTimer = 0
                    self.rightArrowTimer.stop()
                if event.key == pygame.K_BACKSPACE:
                    self._backspaceTickTimer = 0
                    self.backspaceTimer.stop()
                if event.key == pygame.K_LSHIFT:
                    self.holdingShift = False

        # Selecting the whole text
        if self._active:
            if self.ctrlA.update() and self.text != "":
                # Highlighting the whole text
                if not(self.highlighted):
                    self.highlighted = True
                    self.currentLetter = len(self.text)
                    self.highlightedLastLetter = 0
                    highlightSurfaceWidth = self.font.size(self._text[self.lastLetterIndex:self.currentLetter])[0]
                    self.highlightSurface = pygame.Surface((highlightSurfaceWidth, self.textLabel.get_height()), pygame.SRCALPHA)
                else:
                    # Highlighting the whole text
                    if self.currentLetter != len(self.text) and self.highlightedLastLetter != 0:
                        self.currentLetter = len(self.text)
                        self.highlightedLastLetter = 0
                        highlightSurfaceWidth = self.font.size(self._text[self.lastLetterIndex:self.currentLetter])[0]
                        self.highlightSurface = pygame.Surface((highlightSurfaceWidth, self.textLabel.get_height()), pygame.SRCALPHA)
                    else:
                        # Unhighlighting the whole text
                        self.highlighted = False
                        self.currentLetter = len(self.text)
                        self.highlightedLastLetter = None
                        self.lastLetterIndex = None

            # Cutting text and copying cut text to a clipboard
            if self.ctrlX.update() and self.highlighted:
                if self.currentLetter > self.highlightedLastLetter:
                    previousTextLength = len(self.text)
                    pyperclip.copy(self.text[self.highlightedLastLetter:self.currentLetter])
                    self.text = self.text[:self.highlightedLastLetter] + self.text[self.currentLetter:]
                    self.currentLetter -= previousTextLength - len(self.text)
                elif self.currentLetter < self.highlightedLastLetter:
                    pyperclip.copy(self.text[self.currentLetter:self.highlightedLastLetter])
                    self.text = self.text[:self.currentLetter] + self.text[self.highlightedLastLetter:]

                self.highlighted = False
                self.highlightedLastLetter = None
                self.lastLetterIndex = None
                # Moving whole text to the right when it's too long to fit in the box
                if self.textPosition < 4:
                    widthDiff = self.font.size(self._text[0:self.currentLetter])[0]
                    self.textPosition = (self._width - 3) - widthDiff - 4
                    if self.textPosition > 4:
                        self.textPosition = 4  
                if self.textPosition > 4:
                    self.textPosition = 4

            # Copying highlighted text to a clipboard
            if self.ctrlC.update():
                if self.currentLetter > self.highlightedLastLetter:
                    pyperclip.copy(self.text[self.highlightedLastLetter:self.currentLetter])
                else:
                    pyperclip.copy(self.text[self.currentLetter:self.highlightedLastLetter])
            
            # Pasting text in to a text box
            if self.ctrlV.update():
                pastedText = pyperclip.paste()
                self.text = self._text[:self.currentLetter] + pastedText + self._text[self.currentLetter:]
                self.currentLetter += len(pastedText)
                # Moving whole text to the left when it's too long to fit in the box
                if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosition) + 6 > self._width - 3:
                    self.textPosition -= (self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosition) + 6) - (self._width - 3)
                    if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosition) == (self._width - 9):
                        self.textPosition += 4

    def _scrollTroughTextByMouse(self):
        pass

    def _setCursorPosition(self, pos):
        if self._text != "":
            clickedPos = (pos[0] - self._x) + abs(self.textPosition) - 4
            charLengthList = []
            for i in range(len(self._text)):
                charLengthList.append((self.font.size(self._text[0:i])[0]))

            closest_number = min(charLengthList, key=lambda x: abs(x - clickedPos))
            self.currentLetter = charLengthList.index(closest_number)
            if self.textPosition < 0:
                self.currentLetter += 1
            if clickedPos > self.font.size(self._text[0:len(self._text)-1])[0] + (self.font.size(self._text[-1])[0] // 2):
                self.currentLetter = len(self._text)

            if self.lastLetterIndex != None:
                if self.currentLetter < self.lastLetterIndex:
                    self.highlighted = True
                    highlightSurfaceWidth = self.font.size(self._text[self.currentLetter:self.lastLetterIndex])[0]
                    self.highlightSurface = pygame.Surface((highlightSurfaceWidth, self.textLabel.get_height()), pygame.SRCALPHA)
                elif self.currentLetter > self.lastLetterIndex:
                    self.highlighted = True
                    highlightSurfaceWidth = self.font.size(self._text[self.lastLetterIndex:self.currentLetter])[0]
                    self.highlightSurface = pygame.Surface((highlightSurfaceWidth, self.textLabel.get_height()), pygame.SRCALPHA)
                self.highlightedLastLetter = self.lastLetterIndex
                if self.currentLetter == self.lastLetterIndex:
                    self.highlightSurface = pygame.Surface((0, self.textLabel.get_height()), pygame.SRCALPHA)
                    self.highlighted = False

    def _resetTextPosition(self):
        self.textPosition = 4

    def draw(self, surface=None):
        global _changingCursor
        if self.active:
            self._scrollTroughTextByMouse()
        if surface == None:
            surface = _windowObject.screen

        if self.active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self._leftArrowTickTimer < 20:
                self._leftArrowTickTimer += 1
                if self._leftArrowTickTimer >= 20:
                    self.leftArrowTimer.restart()
            if keys[pygame.K_RIGHT] and self._rightArrowTickTimer < 20:
                self._rightArrowTickTimer += 1
                if self._rightArrowTickTimer >= 20:
                    self.rightArrowTimer.restart()
            if keys[pygame.K_BACKSPACE] and self._backspaceTickTimer < 20:
                self._backspaceTickTimer += 1
                if self._backspaceTickTimer >= 20:
                    self.backspaceTimer.restart()

            if self.leftArrowTimer.loop():
                if self.currentLetter-1 >= 0:
                    self.currentLetter -= 1
                    self.cursorBlinkingTimer.tick = 0
                    self._showCursor = True
                    if self.holdingShift:
                        self._arrowKeyLeftHighlight()
                    # Moving whole text to the right when it's too long to fit in to the box
                    if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosition) + 6 < 4:
                        self.textPosition += abs((self.font.size(self._text[0:self.currentLetter])[0]) + self.textPosition)
                    if self.textPosition > 4:
                        self.textPosition = 4

            if self.rightArrowTimer.loop():
                if self.currentLetter+1 <= len(self.text):
                    self.currentLetter += 1
                    self.cursorBlinkingTimer.tick = 0
                    self._showCursor = True
                    if self.holdingShift:
                        self._arrowKeyRightHighlight()
                    # Moving whole text to the left when it's too long to fit in the box
                    if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosition) + 6 > self._width - 3:
                        self.textPosition -= (self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosition) + 6) - (self._width - 3)
                        if self.font.size(self._text[0:self.currentLetter])[0] - abs(self.textPosition) == (self._width - 9):
                            self.textPosition += 4

            if self.backspaceTimer.loop():
                if self.currentLetter-1 >= 0:
                    self.cursorBlinkingTimer.tick = 0
                    self._showCursor = True
                    self.text = self.text[:self.currentLetter-1] + self.text[self.currentLetter:]
                    self.currentLetter -= 1

                    # Moving whole text to the right when it's too long to fit in the box
                    if self.textPosition < 4:
                        widthDiff = self.font.size(self._text[0:self.currentLetter])[0]
                        self.textPosition = (self._width - 3) - widthDiff - 4
                        if self.textPosition > 4:
                            self.textPosition = 4  

        if not(self.hide):
            pos = pygame.mouse.get_pos()

            if self.lastLetterIndex == None:
                if self.active and (self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1):
                    self.highlightSurface = pygame.Surface((0, self.textLabel.get_height()), pygame.SRCALPHA)
                    self._setCursorPosition(pos)
                    self.lastLetterIndex = self.currentLetter
            elif (self.active and self.lastLetterIndex != None) and pygame.mouse.get_pressed()[0] == 1:
                self._setCursorPosition(pos)
            elif self.active and pygame.mouse.get_pressed()[0] == 0:
                self.lastLetterIndex = None

            if not(self.disable):
                if self.rect.collidepoint(pos):
                    if self._changeCursor:
                        _changingCursor = pygame.SYSTEM_CURSOR_IBEAM
                if pygame.mouse.get_pressed()[0] == 1 and self.rect.collidepoint(pos):
                    if not(self.clicked) and not(self.clickedOutside):
                        self.active = True
                        self.clicked = True
                        self.cursorBlinkingTimer.tick = 0
                        self._showCursor = True
                        
                        if self._text == self._placeholderText:
                            self.text = ""

                        if self.clickEvent != None:
                            if self._has_arguments(self.clickEvent):
                                self.clickEvent(self)
                            else:
                                self.clickEvent()

                elif pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                    self.clicked = False

                elif pygame.mouse.get_pressed()[0] == 0 and self.clickedOutside:
                    self.clickedOutside = False

                elif pygame.mouse.get_pressed()[0] == 1 and self.active:
                    if not(self.rect.collidepoint(pos)) and not(self.clicked):
                        self.active = False

                elif pygame.mouse.get_pressed()[0] == 1 and not(self.clicked):
                    if not(self.active) and not(self.rect.collidepoint(pos)):
                        self.clickedOutside = True
                        self.highlighted = False
            
            if self.outlineWidth > 0:
                if self.borderRadius > 0:
                    gfxdraw.aacircle(surface, (self.textBoxRect.x + self.borderRadius)-self.outlineWidth, (self.textBoxRect.y + self.borderRadius)-self.outlineWidth, self.borderRadius, self.outlineColor0)
                    gfxdraw.filled_circle(surface, (self.textBoxRect.x + self.borderRadius)-self.outlineWidth, (self.textBoxRect.y + self.borderRadius)-self.outlineWidth, self.borderRadius, self.outlineColor0)
                    gfxdraw.aacircle(surface, (self.textBoxRect.x + self.textBoxRect.width - self.borderRadius-1)+self.outlineWidth, (self.textBoxRect.y + self.borderRadius)-self.outlineWidth, self.borderRadius, self.outlineColor0)
                    gfxdraw.filled_circle(surface, (self.textBoxRect.x + self.textBoxRect.width - self.borderRadius-1)+self.outlineWidth, (self.textBoxRect.y + self.borderRadius)-self.outlineWidth, self.borderRadius, self.outlineColor0)
                    gfxdraw.aacircle(surface, (self.textBoxRect.x + self.borderRadius)-self.outlineWidth, (self.textBoxRect.y + self.textBoxRect.height - self.borderRadius-1)+self.outlineWidth, self.borderRadius, self.outlineColor0)
                    gfxdraw.filled_circle(surface, (self.textBoxRect.x + self.borderRadius)-self.outlineWidth, (self.textBoxRect.y + self.textBoxRect.height - self.borderRadius-1)+self.outlineWidth, self.borderRadius, self.outlineColor0)
                    gfxdraw.aacircle(surface, (self.textBoxRect.x + self.textBoxRect.width - self.borderRadius-2)+self.outlineWidth, (self.textBoxRect.y + self.textBoxRect.height - self.borderRadius-1)+self.outlineWidth, self.borderRadius, self.outlineColor0)
                    gfxdraw.filled_circle(surface, (self.textBoxRect.x + self.textBoxRect.width - self.borderRadius-2)+self.outlineWidth, (self.textBoxRect.y + self.textBoxRect.height - self.borderRadius-1)+self.outlineWidth, self.borderRadius, self.outlineColor0)

                    pygame.draw.rect(surface, self.outlineColor0, ((self.textBoxRect.x + self.borderRadius)-self.outlineWidth, self.textBoxRect.y-self.outlineWidth, (self.textBoxRect.width - 2 * self.borderRadius)+self.outlineWidth*2, self.textBoxRect.height+self.outlineWidth*2))
                    pygame.draw.rect(surface, self.outlineColor0, ((self.textBoxRect.x)-self.outlineWidth, self.textBoxRect.y + self.borderRadius-self.outlineWidth, self.textBoxRect.width+(self.outlineWidth*2), (self.textBoxRect.height - 2 * self.borderRadius)+self.outlineWidth*2))

            if self.borderRadius <= 0:
                pygame.draw.rect(surface, self.background0, self.textBoxRect)
                if self.outlineWidth > 0:
                    pygame.draw.rect(surface, self.outlineColor, pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height), width=self.outlineWidth)
                    
            elif self.borderRadius > 0:
                gfxdraw.aacircle(surface, self.textBoxRect.x + self.borderRadius, self.textBoxRect.y + self.borderRadius, self.borderRadius, self.background0)
                gfxdraw.filled_circle(surface, self.textBoxRect.x + self.borderRadius, self.textBoxRect.y + self.borderRadius, self.borderRadius, self.background0)
                gfxdraw.aacircle(surface, self.textBoxRect.x + self.textBoxRect.width - self.borderRadius-1, self.textBoxRect.y + self.borderRadius, self.borderRadius, self.background0)
                gfxdraw.filled_circle(surface, self.textBoxRect.x + self.textBoxRect.width - self.borderRadius-1, self.textBoxRect.y + self.borderRadius, self.borderRadius, self.background0)
                gfxdraw.aacircle(surface, self.textBoxRect.x + self.borderRadius, self.textBoxRect.y + self.textBoxRect.height - self.borderRadius-1, self.borderRadius, self.background0)
                gfxdraw.filled_circle(surface, self.textBoxRect.x + self.borderRadius, self.textBoxRect.y + self.textBoxRect.height - self.borderRadius-1, self.borderRadius, self.background0)
                gfxdraw.aacircle(surface, self.textBoxRect.x + self.textBoxRect.width - self.borderRadius-2, self.textBoxRect.y + self.textBoxRect.height - self.borderRadius-1, self.borderRadius, self.background0)
                gfxdraw.filled_circle(surface, self.textBoxRect.x + self.textBoxRect.width - self.borderRadius-2, self.textBoxRect.y + self.textBoxRect.height - self.borderRadius-1, self.borderRadius, self.background0)

                pygame.draw.rect(surface, self.background0, (self.textBoxRect.x + self.borderRadius, self.textBoxRect.y, self.textBoxRect.width - 2 * self.borderRadius, self.textBoxRect.height))
                pygame.draw.rect(surface, self.background0, (self.textBoxRect.x, self.textBoxRect.y + self.borderRadius, self.textBoxRect.width, self.textBoxRect.height - 2 * self.borderRadius))

            surfX = self.rect.x + self.outlineWidth
            surfY = (self.rect.y - (self.textSurface.get_height() / 2) + (self.height / 2))+self.outlineWidth
            surface.blit(self.textSurface, (surfX, surfY))
            self.textSurface.fill(self.background0)
            if not(self.active) and (self._text == "" or self._text == self._placeholderText):
                self.text = self._placeholderText

            if not(self.highlighted):
                self.highlightedLastLetter = None

            if (self.active and self.highlighted) and self.highlightedLastLetter != None:
                self.highlightSurface.fill(self.highlightColor)
                highlightSurfaceX = 0
                if self.currentLetter < self.highlightedLastLetter:
                    self.highlighted = True
                    highlightSurfaceX = (self.textPosition + self.font.size(self._text[0:self.highlightedLastLetter])[0]) - self.font.size(self._text[self.currentLetter:self.highlightedLastLetter])[0]
                elif self.currentLetter > self.highlightedLastLetter:
                    self.highlighted = True
                    highlightSurfaceX = self.textPosition + self.font.size(self._text[0:self.highlightedLastLetter])[0]
                self.textSurface.blit(self.highlightSurface, (highlightSurfaceX,0))

            self.textLabel = self.font.render(self.text, True, (self.textColor0))
            self.textSurface.blit(self.textLabel, (self.textPosition,0))

            if self.cursorBlinkingTimer.loop():
                self._showCursor = not(self._showCursor)

            if self._active and not(self.highlighted):
                cursorPosX = self.textPosition + self.font.size(self.text[0:self.currentLetter])[0]
                if self._showCursor:
                    self.textSurface.blit(self.cursorSurface, (cursorPosX,0))
                    self.cursorSurface.fill(self.cursorColor)

class DisableObjects():
    def __init__(self):
        self.disablePropertiesTempDict = {}

    def disable_all_objects(self, all_objects):
        for obj in all_objects:
            if hasattr(obj, "disable"):
                self.disablePropertiesTempDict[obj] = obj.disable
                obj.disable = True

    def restore_disable_property(self):
        for obj, original_value in self.disablePropertiesTempDict.items():
            obj.disable = original_value