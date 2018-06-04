from sysop import keyboard,keycode,winapi;
import PIL.Image  as Image;
import pyautogui as pag;
import numpy as np;
import time;
import math;
import operator;
from functools import reduce;


kb=keyboard();
dict_imgs=dict();

def clear_imgs():
    dict_imgs={};



def image_contrast(img1, img2):
    '''
    对比两张图片，相同返回0.0 越多不同返回的数值越大
    '''
    h1 = img1.histogram()
    h2 = img2.histogram()

    result = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
    return result

def screenshot(id):
    global dict_imgs;
    #获取指定程序在屏幕上的坐标
    pos=winapi.get_window_rect();
    print(pos);
    #截取图片
    width=pos[2]-pos[0]-240;#窗口宽度-操控面板
    height=pos[3]-pos[1];#窗口高度
    height=height-80#去掉底部边框
    pos_x=pos[0]+3;#去掉左侧边框
    pos_y=pos[1]+66;#去掉顶部标题栏
    img=pag.screenshot(region=(pos_x,pos_y,width,height))#region=(pos.x,pos.y,size.w,size.y)
    if id not in dict_imgs.keys():
        dict_imgs[id]=[];
    if len(dict_imgs[id])>1:
        #比对最后两张图片，如果很相近 就说明是地图已经移动到顶了，不能移动了，所以截取的图片才相近
        db=image_contrast(dict_imgs[id][-1],img);
        print(db);
        if db<=45.0:
            return True;

    dict_imgs[id].append(img);
    return False;

def origin():
    return;
    kb.key_down(keycode.left,50);
    kb.key_down(keycode.up,50);


def BuildMap():
    origin();
    clear_imgs();
    newimg=None;
    i=1;


    while True:
        #纵向截图
        while True:
            #横向截图
            if(screenshot("row%s"%(i,))):
                break;
            kb.key_down(keycode.right,1);

        kb.key_down(keycode.left,50);#移动到最左
        kb.key_down(keycode.down,9);#下移一屏，9次↓箭头正好一屏
        i=i+1;
        if i>3:#只纵向移3屏，精度不够，就把上面的9减小，每点一次↓箭头是80像素，合并图片的total_y=i*h;要做“-箭头次数*80”
            break;
        

     
    newimg = Image.new('RGBA', (10000, 10000))
    total_x=0;
    total_y=0;
    for k,v in dict_imgs.items():
        i=int(str(k).replace("row",""))
        j=0;
        for item in v:
            w,h=item.size;
            item=item.resize((w,h),Image.ANTIALIAS)
            newimg.paste(item,(80*j,(i-1)*h));
            total_x=80*j+(w-80);
            total_y=i*h;
            j=j+1;
    newimg=newimg.crop((0,0,total_x,total_y));#减去多余空白
    newimg.save('screenshot/%s.png' % (time.time()));
    print("生成完毕，生成的文件在screenshot文件夹下面查找。");



#删除根目录下EmperorText.txt中的“这个任务胜利了” 换成空格
#win10 把缩放125%调到100%
#只能用1024*768的窗口模式
if __name__=="__main__":
    kb.on_keyboard(BuildMap);
    #todo:提示截图完成，增加手动截图
