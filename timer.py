import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2
import time

#pomodoro focus timer: 25-5 min focus intervals
#urseamajoris 11/1/22


def timer(secs, count):
    i = round((count/secs) * 100)
    secs = secs - 1

    return [i, secs]
    
def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def canvas():
    WHITE = (255,255,255,255)
    RED = (0,0,255,255)
    GREEN = (0,255,0,255)
    b,g,r,a = 255,255,255,255


    fontpath = "THSarabunNew Bold.ttf"     
    font = ImageFont.truetype(fontpath, 32)
    img = np.zeros((550,350,3),np.uint8)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)

    return font, img, img_pil, draw

def clock(secs, focus):
    WHITE = (255,255,255,255)
    RED = (0,0,255,255)
    GREEN = (0,255,0,255)

    for i in range(secs):
        font, img, img_pil, draw = canvas()
        progress = timer(secs, i)
        count = int(progress[1]) - i
        angle = 360 - (progress[0]/100)*360
        text = time.strftime("%d/%m/%y \n%H:%M:%S \n%Z", time.localtime()) 
        draw.text((50,50), text, font=font,fill=WHITE)
        prog = f'Progress = {str(progress[0])} % \nand {str(convert(count))} left.'
        draw.text((50, 150),  prog, font = font, fill = WHITE)
        prog2 = f'{str(convert(count))}'
        draw.text((90, 290),  prog2, font = font, fill = WHITE)
        if focus == True:
            text2 = 'IN FOCUS SESSION'
            draw.text((50,400),text2, font = font, fill = RED)
        elif focus == False:
            text2 = 'BREAK'
            draw.text((50,400),text2, font = font, fill = GREEN)
        img = np.array(img_pil)
        cv2.ellipse(img, (125,312), (75,75), 270, 0, angle, (255,255,255), 5)

        cv2.imshow("res", img);cv2.waitKey(1000)

def summary(intervals):
    font, img, img_pil, draw = canvas()

    WHITE = (255,255,255,255)

    text = f'SUMMARY\nToday you have\nfocused for:\n\n {str(intervals*25)} minutes\n over {str(intervals)} intervals'
    draw.text((25,25), text, font=font,fill=WHITE)
    img = np.array(img_pil)
    cv2.imshow('res', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def intervals(intervals):
    for i in range(intervals):
        clock(1500, focus=True)
        clock(300, focus=False)        
    summary(intervals)

rounds = input('put in intervals:')
intervals(rounds)

