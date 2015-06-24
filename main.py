import win32api, win32con, win32gui
import time
import gc
import pywintypes
import ctypes

# format: (x, y, (r, g, b), "text")

WINDOW_NAME = "DOTA 2"

DIRE_ANCIENT = (750, 678, (171, 0, 0))
RADIANT_ANCIENT = (661, 762)


NORMAL_MATCH = (757, 401, (27, 29, 33), "Choose normal match")
RATING_MATCH = (750, 414, (44, 43, 41))  # color - grey


GAME = (921 , 310, (29, 27, 23))
MENU = (650 , 309, (145, 142, 132))
DISCONNECT = (856, 561, (38, 39, 41), "Disconnected from game")
LEAVE_GAME1 = (913, 588, (69, 50, 49))
LEAVE_GAME2 = (912, 467, (131, 121, 122))


FIND_MATCH = (975, 435, (49, 60, 33), "Start finding match")
ACCEPT_GAME = (890, 480, (41, 44, 49), "Game accepted")
HERO_PICK = (1053, 642, (49, 60, 71), "Hero picked")
LP_TABLE = (956, 520, (33, 32, 33), "Lp table closed")
END_TABLE = (1168, 608, (24, 24, 24), "Game score closed")


mmr_list = [FIND_MATCH, ACCEPT_GAME, MENU, GAME,  DISCONNECT, LEAVE_GAME1, LEAVE_GAME2]
coords_list = [FIND_MATCH, ACCEPT_GAME, HERO_PICK, LP_TABLE, END_TABLE]

class Bot():
    def __init__(self):
        self.window_id = win32gui.GetDesktopWindow()
        self.window_dc = win32gui.GetWindowDC(self.window_id)
        pass

    def get_pixel_colour(self, i_x, i_y):
        long_colour = win32gui.GetPixel(self.window_dc, i_x, i_y)
        i_colour = int(long_colour)
        return (i_colour & 0xff, (i_colour >> 8) & 0xff,
            (i_colour >> 16) & 0xff)

    def click(self, coords):
        ctypes.windll.user32.SetCursorPos(coords[0], coords[1])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,coords[0],coords[1],0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,coords[0],coords[1],0,0)
        time.sleep(2)

    def find_window(self, WINDOW_NAME):
        try:
            winID = win32gui.FindWindow(None, WINDOW_NAME)
            win32gui.ShowWindow(winID, win32con.SW_RESTORE)
            win32gui.SetWindowPos(winID,win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
            win32gui.SetWindowPos(winID,win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        except pywintypes.error:
            print("Maybe window is not found?")

    def check_color(self, coords):
        if self.get_pixel_colour(coords[0], coords[1]) == coords[2]:
            try:
                print(coords[3])
            except IndexError:
                pass
            return 1
        else:
            return 0
            #print("The color is not match")

    def loop(self):
        if self.check_color(FIND_MATCH):
            self.click(RATING_MATCH)
            if self.check_color(FIND_MATCH):
                self.click(FIND_MATCH)
                while self.check_color(GAME) == False or self.check_color(NORMAL_MATCH) == False:
                    for x in mmr_list:
                        if self.check_color:
                            self.click(x)
            else:
                self.click(NORMAL_MATCH)
        for x in coords_list:
            if self.check_color(x):
                self.click(x)
            elif self.check_color(DIRE_ANCIENT):
                win32api.keybd_event(win32con.VK_F4, 0x3E, 0, 0)
                win32api.keybd_event(win32con.VK_F4, 0x3E, win32con.KEYEVENTF_KEYUP, 0)
                self.click(DIRE_ANCIENT)
            elif self.check_color(DIRE_ANCIENT) == False:
                win32api.keybd_event(win32con.VK_F4, 0x3E, 0, 0)
                win32api.keybd_event(win32con.VK_F4, 0x3E, win32con.KEYEVENTF_KEYUP, 0)
                self.click(RADIANT_ANCIENT)


"""
    def loop(self):
        if self.check_color(FIND_MATCH):
            self.click(RATING_MATCH[0], RATING_MATCH[1])
            if self.check_color(RATING_MATCH) == False:
                self.click(FIND_MATCH[0], FIND_MATCH[1])
                while self.check_color(GAME) == False or self.check_color(NORMAL_MATCH) == False:
                    for x in mmr_list:
                        if self.check_color:
                            self.click(x[0], x[1])
            else:
                self.click(NORMAL_MATCH)
                pass

        for x in coords_list:
            if self.check_color(x):
                self.click(x[0], x[1])
            elif self.check_color(DIRE_ANCIENT):
                win32api.keybd_event(win32con.VK_F4, 0x3E, 0, 0)
                win32api.keybd_event(win32con.VK_F4, 0x3E, win32con.KEYEVENTF_KEYUP, 0)
                self.click(DIRE_ANCIENT[0], DIRE_ANCIENT[1])
            elif self.check_color(DIRE_ANCIENT) == False:
                win32api.keybd_event(win32con.VK_F4, 0x3E, 0, 0)
                win32api.keybd_event(win32con.VK_F4, 0x3E, win32con.KEYEVENTF_KEYUP, 0)
                self.click(RADIANT_ANCIENT[0], RADIANT_ANCIENT[1])
"""

b = Bot()

while True:
    b.find_window(WINDOW_NAME)
    b.loop()

