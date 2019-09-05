#!/usr/bin/python3
#-*- coding:utf-8 -*-

# a)检测按键需要
import win32api as wapi
import time

# b)执行按键
import ctypes
import time
import pyautogui as pag

# 声音提示模块
import winsound
import sys



# 按键仓库-BGN
SendInput = ctypes.windll.user32.SendInput
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

M = 0x32
R = 0x13
T = 0x14
C = 0x2E

O1 = 0x02
O2 = 0x03
O3 = 0x04
O4 = 0x05
O5 = 0x06
O6 = 0x07
O7 = 0x08
O8 = 0x09
O9 = 0x0A
O0 = 0x0B

UP = 0xC8
LEFT = 0xCB
RIGHT = 0xCD
DOWN = 0xD0

CAPITAL = 0x3A
ENT = 0x1C

F11 = 0x57
SPACE = 0x39

# a)获取键盘按键-BGN
keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890,.'£$/\\":
    keyList.append(char)


def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys


# b)执行按键-BGN
# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def set_pos(x, y):
    x = 1 + int(x * 65536./1920.)
    y = 1 + int(y * 65536./1080.)
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x, y, 0, (0x0001 | 0x8000), 0, ctypes.pointer(extra))
    command = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

def left_click( speed= 0.05 ):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    time.sleep( speed ) # 按驻鼠标左键x秒

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0004, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def right_click( speed = 0.05 ):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    time.sleep(speed) # 按驻鼠标左键x秒

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0010, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# b)执行按键-END

# c)功能调试区域-BGN

#   1. -1/2- 开启/关闭鼠标左单击,鼠标右单击
def MouseClick( door, speed = 0.05 ):
    if( door == 1 ):
        left_click( speed )
    elif( door == 2 ):
        right_click( speed )
    else:
        return 0

#  2. -0- 自定模式

# 获取鼠标位置
def getPos():
    x, y = pag.position()
    return [x,y]

# 逻辑分析
#   开头准备:
#       获取蟠桃位置,提示 - 等待3秒
#       获取万事通位置,提示 - 等待3秒
#       获取兑换金丹位置 - 提示
#   获取经验:
#       移动到蟠桃位置
#       右键10663下 - 停止右键
#   兑换金丹:
#       循环2次:
#           移动到万事通位置 - 0.3s
#           左键1下 - 0.3s
#           移动到获取金丹的位置 - 0.3s
#           左键1下 - 0.5s

#   主控:
#       开头准备
#       循环:
#           获取当前按键 - 判断是否停止键
#           开头准备()
#           循环:
#               获取经验()
#               兑换金丹()
def mReadyPos():

    panTao = getPos()
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    time.sleep(3)

    npc = getPos()
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    time.sleep(3)

    jinDan = getPos()
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    time.sleep(1)

    return [ panTao, npc, jinDan ]

def mGetEx( panTao, clickNum = 5500 ):
    x,y = panTao
    set_pos(x,y)
    i=0
    while( i < clickNum ):
        if( '3' in key_check() ):
            break
        MouseClick(2, 0.01)
        i+=1

def mGetJianDan( npc, jinDan ):
    nx, ny = npc
    jx, jy = jinDan
    for i in range(1):
        set_pos(nx, ny)
        time.sleep(0.4)

        MouseClick(1, 0.08)
        time.sleep(0.4)

        set_pos(jx, jy)
        time.sleep(0.4)

        MouseClick(1, 0.08)
        time.sleep(0.8)





if __name__ == "__main__":
    print("\
\n\
#   MousePoint v1.2( 鼠标连点器 )\n\
#   作者: __OO7__ ( 反馈意见给作者: QQ - 1069798804 )\n\
#   作者更新链接及开源链接: https://github.com/ZTaer/MousePoint/\n\
#   注意: 此程序仅供个人研究学习,恶意使用本程序造成游戏破坏,作者将不承担任何法律责任( 依然执行本程序代表你已同意此协议! )\n\
#   注意: 此程序完全免费,如果想获得最新版本可以访问上方GitHub链接\n\
#   注意: 如果你有什么更好的改进意见可以联系上放作者QQ( 加好友留言时输入: MouseUser )\n\
    \n\
# 用法:\n\
#   0. -KS- 开启功能( 进入游戏中输入即可 )\n\
#   1. -JS- 结束功能( 结束功能后,再次输入KS依然可以开启功能 )\n\
#   2. -TC- 退出程序\n\
    \n\
# 功能:\n\
#   0. -1- 鼠标左键连点\n\
#   1. -2- 鼠标右键连点\n\
#   2. -3- 停止鼠标连点\n\
    \n\
#   3. -7- 低速连点\n\
#   4. -8- 中速连点\n\
#   5. -9- 高速连点"\
        )
    print("\n!!!开启成功 - OPEN SUCCESSFULLY!!!( 注意: 直接进入游戏,不要关闭本窗口,最小化即可 )")
    while( True ):
        door = 0
        speed = 0.05
        bgn = False

        keysIng = key_check()
        if( 'K' in keysIng and 'S' in keysIng ):
            bgn = True
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
        elif ('T' in keysIng and 'C' in keysIng):
            print("成功退出,欢迎下次使用!")
            time.sleep(2)
            sys.exit()
        else:
            continue
        while(bgn):
            keysIng = key_check()
            if( '1' in keysIng or '3' in keysIng ):
                door = 1
                while( True ):
                    if( '3' in key_check() or '2' in key_check() ):
                        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                        door = 0
                        break
                    else:
                        MouseClick(door, speed)

            elif( '2' in keysIng or '3' in keysIng ):
                door = 2
                i = 0
                while( True ):
                    if( '3' in key_check() or '1' in key_check() ):
                        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                        door = 0
                        print('循环次数为: ', i )
                        break
                    else:
                        MouseClick(door, speed)
                    i+=1

            elif( '0' in keysIng ):
                panTao, npc, jinDan = mReadyPos()

                clickNum = input('请输入循环次数( 默认5500 ): ')
                if( len(clickNum) == 0 ):
                    clickNum = 5500
                else:
                    clickNum = int( clickNum )
                print(clickNum)

                while(True):
                    mGetEx( panTao )
                    if ('3' in key_check()):
                        break
                    time.sleep(1)
                    mGetJianDan(npc, jinDan)
            # 挂挡
            elif( '7' in keysIng ):
                speed = 0.08
                winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
            elif( '8' in keysIng ):
                speed = 0.05
                winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
            elif( '9' in keysIng ):
                speed = 0.01
                winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

            elif( 'J' in keysIng and 'S' in keysIng ):
                if(door):
                    door = 0
                    continue
                try:
                    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                except:
                    bgn = False
                bgn = False


