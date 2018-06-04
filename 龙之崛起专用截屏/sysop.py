#-*- coding=utf-8 -*-
import pythoncom;
import pyautogui as pag;
import win32con;
import win32gui
import win32api
import PIL.Image  as Image;
from ctypes import *;
import PyHook3 as pyHook;


class winapi(object):

    @classmethod
    def get_window_rect(cls):
        #user32=windll.user32;
        # 获取最上层的窗口句柄  
        #hwnd=user32.GetForegroundWindow();
        # 获取进程ID  
        #pid=c_ulong(0);
        #user32.GetWindowThreadProcessId(hwnd,byref(pid));
        classname = "Emperor"
        titlename = "龙之崛起";
        #获取句柄
        hwnd = win32gui.FindWindow(None, titlename)
        #获取窗口左上角和右下角坐标,左上右下
        return win32gui.GetWindowRect(hwnd)
        


class keycode(object):
    up="up";
    down="down";
    left="left";
    right="right";

class keyboard(object):

    def __init__(self):
        self.user32 = windll.user32  
        self.kernel32 = windll.kernel32  
        self.psapi = windll.psapi  
        self.current_window = None  

    '''
    键盘相关
    '''
    def on_keyboard(self,func=None):
        """
        函数说明:监听键盘
        Parameters:
            无
        Returns:55
            func:触发按键时执行的回调函数
        Modify:
            2018-05-30
        """
      
        #定义快捷键  
        HOTKEYS = {  
                    1 : (win32con.VK_F1, win32con.MOD_CONTROL),  
                    2 : (win32con.VK_F4, win32con.MOD_CONTROL)  
                    }  
  
        #快捷键对应的驱动函数  
        HOTKEY_ACTIONS = {  
            1 : self.handle_start_InspecEvent,  
            2 : self.handle_stop_InspecEvent  
            }      
  
        #注册快捷键  
        for id, (vk, modifiers) in HOTKEYS.items ():  
            if not self.user32.RegisterHotKey (None, id, modifiers, vk):  
                print("Unable to register id", id )     
      
        #启动监听          
        try:  
            msg = wintypes.MSG ()  
            while self.user32.GetMessageA (byref (msg), None, 0, 0) != 0:  
                if msg.message == win32con.WM_HOTKEY:  
                    action_to_take = HOTKEY_ACTIONS.get (msg.wParam)  
                    if action_to_take:  
                        action_to_take (func)  
  
                self.user32.TranslateMessage (byref (msg))  
                self.user32.DispatchMessageA (byref (msg))  
  
        finally:  
            for id in HOTKEYS.keys ():  
                self.user32.UnregisterHotKey (None, id)   


    def handle_start_InspecEvent(self,func=None):  
        "开始监控（按下Ctrl + F1）"  
        func();
  
    def handle_stop_InspecEvent(self):  
        "停止监控  (按下Ctrl + F2)"  
        pass;

    def key_down(self,keycode,num=1):
        for x in range(0,num):
            pag.keyDown(keycode)

