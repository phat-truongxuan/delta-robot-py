from tkinter import *
from tkinter import messagebox
from math import pi, sqrt, sin, cos, asin, acos
import time
import csv
import threading
#import RPi.GPIO as GPIO
#import spidev
from inversegeo4 import *

root = Tk()
root.title('Delta Robot')
root.geometry("1000x500")

#set up GPIO and SPI               
'''spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000
GPIO.setmode(GPIO.BCM)
s1 = 22
GPIO.setup(s1, GPIO.OUT)
s2 = 24
GPIO.setup(s2, GPIO.OUT)
s3 = 25
GPIO.setup(s3, GPIO.OUT)
s4 = 23
GPIO.setup(s4, GPIO.OUT)
s5 = 18
pm = 17
va = 27
GPIO.setup(pm, GPIO.OUT)
GPIO.setup(s5, GPIO.OUT)
GPIO.setup(va, GPIO.OUT)
GPIO.output(s1, True)
GPIO.output(s2, True)
GPIO.output(s3, True)
GPIO.output(s4, True)
GPIO.output(s5, True)
GPIO.output(va, False)
GPIO.output(pm, False)
'''

wp = 35.25
gp = round(wp/2, 2)
ep = round(sqrt(3)*wp/2, 2)

#add global variables from here
#t10 = IntVar()
#t20 = IntVar()
#t30 = IntVar() 

a = 0
x0 = 0
y0 = 0
z0 = -228.3
r0 = 0
con = 0
acom = [0, 0, 0, 0]

stplen = 5 # step length of position movement
reso = 0.15   #stepper motor resolution = 0.45 / 3 

t10 = 28.09
t20 = 28.09
t30 = 28.09
t40 = 0.0
pnp = 0
#to here

stp1 = 0
stp2 = 0
stp3 = 0
stp4 = 0

stp = [stp1, stp2, stp3, stp4]

inputx1 = Entry(root, width=6, borderwidth=3)
inputx1.place(x=25, y=10)
inputx1.insert(0, 0)

inputy1 = Entry(root, width=6, borderwidth=3)
inputy1.place(x=125, y=10)
inputy1.insert(0, 0)

inputz1 = Entry(root, width=6, borderwidth=3)
inputz1.place(x=225, y=10)
inputz1.insert(0, -228.3)

inputr1 = Entry(root, width=6, borderwidth=3)
inputr1.place(x=325, y=10)
inputr1.insert(0, 0)

'''command= Entry(root , width=50, borderwidth=5)
command.place(x=10,y=320)'''


def pick():
    global pnp
    pnp = 1
    '''GPIO.output(va, True)
    GPIO.output(pm, False)'''
    

def hold():
    global pnp 
    '''GPIO.output(va, False)'''
    pnp = 2

def place():
    global pnp
    '''GPIO.output(pm, True)'''
    pnp = 0



def move(x, y, z, r): #angles divide # 2
    global t10, t20, t30 , t40 , acom, x0, y0, z0, r0 , stp1, stp2 , stp3 , stp4
    theta10 = t10
    theta20 = t20
    theta30 = t30
    theta40 = t40

    print(f"coordinate of current position {x0}, {y0}, {z0}, {r0}")
    print(f"current theta :  {t10}  {t20}  {t30}  {t40} ")
    print("-                                               -") 
    x0 = x
    y0 = y
    z0 = z
    r0 = r

    csvOpen = open('position.csv','w')   #write out csv file the actual coordinate
    c = csv.writer(csvOpen, dialect='excel')
    c.writerows([['x', float(x)],['y', float(y)],['z', float(z)], ['r', float(r)]])
            
    print(f"coordinate of destination {round(x,3)}, {round(y, 3)}, {round(z, 3)}, {round(r, 3)}")


    theta1 = t1(x, y, z)[0]
    theta2 = t2(x, y, z)[0]
    theta3 = t3(x, y, z)[0]
    theta4 = r

    print(f"destination theta :  {theta1}  {theta2}  {theta3}  {r} ")
    print("-                                               -")
    ang1 = round(theta1-theta10, 2)
    ang2 = round(theta2-theta20, 2)
    ang3 = round(theta3-theta30, 2)
    ang4 = round(theta4-theta40, 2)
    print(f"angle to go is {ang1}  {ang2}  {ang3}  {ang4}")       
    angle = [ang1, ang2, ang3, ang4]
    asend = [0, 0, 0, 0]

    anglemax = max(abs(angle[0]), abs(angle[1]), abs(angle[2]), abs(angle[3]))
    print(f'anglemax is {anglemax}')
    if anglemax >18:
        resen = int(anglemax//18+1)
        print(f" resen is {resen} ")
        m = 1
        for m in range(resen):
            print(f"send spi")
            angle = [ang1/resen, ang2/resen, ang3/resen, ang4/resen]
            asend = [0, 0, 0, 0]
            for m in range(len(angle)):     # new algorithm 
                asend[m] = int(angle[m]/reso)
                if asend[m] != 0:
                    acom[m] = round(acom[m] + ((abs(angle[m])%reso)*(angle[m]/abs(angle[m]))), 5)
                if abs(acom[m]) > reso:
                    asend[m] = int(asend[m] + (abs(asend[m])/asend[m]))
                    acom[m] = round((abs(acom[m])%reso)*(acom[m]/abs(acom[m])), 5) 
                print(f' angle{m +1} to send is {asend[m]}  and its acom is {acom[m]}')

            as1 = asend[0]
            as2 = asend[1]
            as3 = asend[2]
            as4 = asend[3]

            stp1 = stp1 + as1
            stp2 = stp2 + as2 
            stp3 = stp3 + as3
            stp4 = stp4 + as4

            # convert to data to send via spi 
            if asend[0] < 0:
                as1 = int(abs(asend[0]) + 110)
            if asend[1] < 0:
                as2 = int(abs(asend[1]) + 110)
            if asend[2] < 0:
                as3 = int(abs(asend[2]) + 110)
            if asend[3] < 0:
                as4= int(abs(asend[3]) + 110)
            
            print(f' as1 is {as1}')
            print(f' as2 is {as2}')
            print(f' as3 is {as3}')
            print(f' as4 is {as4}')

            '''csvOpen = open('angle.csv','a')   #write out csv file the actual angle
            c = csv.writer(csvOpen, dialect='excel')
            c.writerow([round(stp1*reso, 2),round(stp2*reso, 2),round(stp3*reso, 2)])

            tisl = 0.01

            GPIO.output(s1, False)
            resp = spi.xfer2([as1])
            GPIO.output(s1, True)

            GPIO.output(s2, False)
            resp = spi.xfer2([as2])
            GPIO.output(s2, True)

            GPIO.output(s3, False)
            resp = spi.xfer2([as3])
            GPIO.output(s3, True)

            GPIO.output(s4, False)
            resp = spi.xfer2([as4])
            GPIO.output(s4, True)
            time.sleep(tisl)'''

            t10 = theta1
            t20 = theta2
            t30 = theta3
            t40 = r

            slide1.set(100*theta1)
            slide2.set(100*theta2)
            slide3.set(100*theta3)
            slide4.set(100*r)

            slide5.set(stp1)
            slide6.set(stp2)
            slide7.set(stp3)
            slide8.set(stp4)

            inputx1.delete(0, 'end')
            inputy1.delete(0, 'end')
            inputz1.delete(0, 'end')
            inputr1.delete(0, 'end')

            inputx1.insert(0, round(x, 3))
            inputy1.insert(0, round(y, 3))
            inputz1.insert(0, round(z, 3))
            inputr1.insert(0, round(r, 3))

            print(f" angle1 = {ang1}  angle2 = {ang2}  angle3 = {ang3} angle4 = {ang4}")
            csvOpen = open('angle.csv','a')   #write out csv file the actual angle
            c = csv.writer(csvOpen, dialect='excel')
            c.writerow([round(theta1, 2),round(theta2, 2),round(theta3, 2),round(theta4, 2)])
            print("--------------------------- ")
            time.sleep(0.2)  # change this 
            root.update() 

    else:   #=========================================================
        for m in range(len(angle)):     # new algorithm 
            asend[m] = int(angle[m]/reso)
            if asend[m] != 0:
                acom[m] = round(acom[m] + ((abs(angle[m])%reso)*(angle[m]/abs(angle[m]))), 5)
            if abs(acom[m]) > reso:
                asend[m] = int(asend[m] + (abs(asend[m])/asend[m]))
                acom[m] = round((abs(acom[m])%reso)*(acom[m]/abs(acom[m])), 5) 
            print(f' angle{m +1} to send is {asend[m]}  and its acom is {acom[m]}')

        as1 = asend[0]
        as2 = asend[1]
        as3 = asend[2]
        as4 = asend[3]

        stp1 = stp1 + as1
        stp2 = stp2 + as2 
        stp3 = stp3 + as3
        stp4 = stp4 + as4

        rep = 1
        asenmax = max(abs(asend[0]), abs(asend[1]), abs(asend[2]), abs(asend[3]))
        print(f'asenmax is {asenmax}')
        if asenmax > 110:
                rep = rep+ int(asenmax/110)
        print(f' rep is {rep}')
        if rep == 1:
            # convert to data to send via spi 
            if asend[0] < 0:
                as1 = int(abs(asend[0]) + 110)
            if asend[1] < 0:
                as2 = int(abs(asend[1]) + 110)
            if asend[2] < 0:
                as3 = int(abs(asend[2]) + 110)
            if asend[3] < 0:
                as4= int(abs(asend[3]) + 110)
            
            print(f' as1 is {as1}')
            print(f' as2 is {as2}')
            print(f' as3 is {as3}')
            print(f' as4 is {as4}')

            '''csvOpen = open('angle.csv','a')   #write out csv file the actual angle
            c = csv.writer(csvOpen, dialect='excel')
            c.writerow([round(stp1*reso, 2),round(stp2*reso, 2),round(stp3*reso, 2)])

            tisl = 0.01

            GPIO.output(s1, False)
            resp = spi.xfer2([as1])
            GPIO.output(s1, True)

            GPIO.output(s2, False)
            resp = spi.xfer2([as2])
            GPIO.output(s2, True)

            GPIO.output(s3, False)
            resp = spi.xfer2([as3])
            GPIO.output(s3, True)

            GPIO.output(s4, False)
            resp = spi.xfer2([as4])
            GPIO.output(s4, True)
            time.sleep(tisl)'''

            t10 = theta1
            t20 = theta2
            t30 = theta3
            t40 = r

            slide1.set(100*theta1)
            slide2.set(100*theta2)
            slide3.set(100*theta3)
            slide4.set(100*r)

            slide5.set(stp1)
            slide6.set(stp2)
            slide7.set(stp3)
            slide8.set(stp4)

            inputx1.delete(0, 'end')
            inputy1.delete(0, 'end')
            inputz1.delete(0, 'end')
            inputr1.delete(0, 'end')

            inputx1.insert(0, round(x, 3))
            inputy1.insert(0, round(y, 3))
            inputz1.insert(0, round(z, 3))
            inputr1.insert(0, round(r, 3))

            print(f" angle1 = {ang1}  angle2 = {ang2}  angle3 = {ang3} angle4 = {ang4}")
            csvOpen = open('angle.csv','a')   #write out csv file the actual angle
            c = csv.writer(csvOpen, dialect='excel')
            c.writerow([round(theta1, 2),round(theta2, 2),round(theta3, 2),round(theta4, 2)])
            print("--------------------------- ")
            time.sleep(0.2)  # change this 
            root.update()    
        else:
            messagebox.showinfo("Delta Robot Program!!!", "Error stepping")
            print("error stepping: out of step range")
            print("                                  ")

def line():
    #fixing under construction
    global stplen
    data = []
    with open('xyz.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(row[1])

    x = float(data[0])
    y = float(data[1])
    z = float(data[2])

    x1 = float(inputx1.get())
    y1 = float(inputy1.get())
    z1 = float(inputz1.get()) 

    csvOpen = open('xyz.csv','w')
    c = csv.writer(csvOpen, dialect='excel')
    c.writerows([['x', x1],['y', y1],['z', z1]])
 

    distant = sqrt(pow(x-x1,2)+pow(y-y1,2)+pow(z-z1,2))
    step = int(distant/resolution)
    comple = float(distant%resolution)
    print(f"number of step is {step} and complement is :{comple}")


def picknplace():
    move(0, 0, -250, 0)
    move(0, 0, -280, 0)
    move(50, 0, -280, 45)
    move(100, 0, -300, 45)
    move(50, 0, -280, 45)
    move(0, 0, -280, 0)
    move(-50, 0, -280, 0)
    move(-100, 0, -300, 0)
    move(-50, 0, -280, 0)
    move(0, 0, -280, 0)
    move(0, 0, -250, 0)

def star():
    global x, y, z, r
    move(0, -60, -260, 0)
    move(-20, -22, -260, 0)
    move(-60, -14, -260, 0)
    move(-32, 18, -260, 0)
    move(-38, 60, -260, 0)
    move(0, 42, -260, 0)
    move(38, 60, -260, 0)
    move(32, 18, -260, 0)
    move(60, -14, -260, 0)
    move(20, -22, -260, 0)
    move(0, -60, -260, 0)


def heart():
    move(0, 0, -240, 30)
    time.sleep(0.5)
    root.update()
    move(0, 10, -230, 0)
    time.sleep(0.5)
    root.update()
    move(0, 25, -230, -30)
    time.sleep(0.5)
    root.update()
    move(0, 35, -260, 0)
    time.sleep(0.5)
    root.update()
    move(0, 35, -260, 45)
    time.sleep(0.5)
    root.update()
    move(0, 0, -290, 0)
    time.sleep(0.5)
    root.update()
    move(0, -35, -260, 20)
    time.sleep(0.5)
    root.update()
    move(0, -35, -260, 0)
    time.sleep(0.5)
    root.update()
    move(0, -25, -230, 0)
    time.sleep(0.5)
    root.update()
    move(0, -10, -230, 0)
    time.sleep(0.5)
    root.update()
    move(0, 0, -240, 0)
    time.sleep(0.5)
    root.update()


def go():
    x = float(inputx1.get())
    y = float(inputy1.get())
    z = float(inputz1.get()) 

    global t10, t20, t30
    theta10 = t10
    theta20 = t20
    theta30 = t30

    csvOpen = open('xyz.csv','w')
    c = csv.writer(csvOpen, dialect='excel')
    c.writerows([['x', x],['y', y],['z', z]])

    print(f"coordinate of destination {x}, {y}, {z}")
    print(f"current theta :  {theta10}  {theta20}  {theta30}  ")

    theta1 = t1(x, y, z)[0]
    theta2 = t2(x, y, z)[0]
    theta3 = t3(x, y, z)[0]

    print(f"destination theta :  {theta1}  {theta2}  {theta3}  ")

    t10 = (theta1)
    t20 = (theta2)
    t30 = (theta3)

    slide1.set(100*theta1)
    slide2.set(100*theta2)
    slide3.set(100*theta3)
    

    #---------send ang1 2 3 via SPI-----------
    ang1 = round(theta1-theta10, 2)
    ang2 = round(theta2-theta20, 2)
    ang3 = round(theta3-theta30, 2)

    print(f" angle1 = {ang1}  angle2 = {ang2}  angle3 = {ang3}")
    print("--------------------------- ")


def popup():
    messagebox.showinfo("this is Delta Robot Controlling Program!!!", "I'm watching you")


def jog():
    global x, y, z, r
    a = 0
    while a < 8*pi+pi/10:
        x = 70*cos(a)
        y = 70*sin(a)
        z = -260 #+abs(20*sin(6*a))
        r = 90*sin(a)
        move(x, y, z, r)
        a = a + pi/16
        print(f"{a*100/(8*pi+pi/10)} %")
        root.update()
        #time.sleep(0.8)
    move(0, 0, -228.3, 0)
    root.update()


def home():
    global t10, t20, t30, x0, y0, z0,stp1, stp2, stp3
    t10 = 28.09
    t20 = 28.09
    t30 = 28.09
    x0 = 0
    y0 = 0
    z0 = -228.3
    stp1 = 0
    stp2 = 0
    stp3 = 0

    slide1.set(2809)
    slide2.set(2809)
    slide3.set(2809)
    slide4.set(0)

    slide5.set(0)
    slide6.set(0)
    slide7.set(0)
    slide8.set(0)

    inputx1.delete(0, 'end')
    inputy1.delete(0, 'end')
    inputz1.delete(0, 'end')
    inputr1.delete(0, 'end')

    inputx1.insert(0, 0)
    inputy1.insert(0, 0)
    inputz1.insert(0, -228.3)
    inputr1.insert(0, 0)
    print("back home!!!")

def convey():

    spd = int(slide9.get())
    if spd < 0:
        spd = abs(spd) 
    elif spd > 0:
        spd = spd + 110
    '''GPIO.output(s5, False)
    resp = spi.xfer2([spd])
    GPIO.output(s5, True)'''
    print(f'speed conveyor is {spd}')
    #time.sleep(0.2)
    root.update()


def onKeyPress(event):
    if event.char == 'J':
        jog()
    if event.char == 'H':
        home()
    if event.char == 'M':
        global t10, t20, t30, t40
        print(f' current theta is {t10} , {t20} , {t30}, {t40}')
    if event.char == 'P':
        pick()
    if event.char == 'O':
        hold()
    if event.char == 'I':
        place()
    if event.char == 'C':
        global con
        if con==1:
            con =0
            ''' GPIO.output(s5, False)
                resp = spi.xfer2([0])
                GPIO.output(s5, True)'''
            print('stopped conveyor')
        elif con==0:
            con  = 1
            print("started conveyor")
            convey()
    if event.char == 'S':
        global pnp
        x = float(inputx1.get())
        y = float(inputy1.get())
        z = float(inputz1.get())
        r = float(inputr1.get())
        csvOpen = open('record.csv','a')   #write out csv file the actual angle
        c = csv.writer(csvOpen, dialect='excel')
        c.writerow([round(x, 2),round(y, 2),round(z, 2),round(r, 2), pnp])
    if event.char == 'D':
        f = open("record.csv", "w")
        f.truncate()
        f.close()
    if event.char == 'A':
        rex = []
        rey = []
        rez = []
        rer = []
        rep = []
        with open('record.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                rex.append(float(row[0]))
                rey.append(float(row[1]))
                rez.append(float(row[2]))
                rer.append(float(row[3]))
                rep.append(float(row[4]))
        print(rex)
        for n in range(len(rex)):
            move(rex[n],rey[n],rez[n],rer[n])
            if rep[n]==0:
                place()
            elif rep[n]==1:
                pick()
            elif rep[n]==2:
                hold()



def enter(event):
    move(float(inputx1.get()), float(inputy1.get()), float(inputz1.get()), float(inputr1.get()))


def xplus(event):
    move(float(inputx1.get())+int(slidelen.get()), float(inputy1.get()), float(inputz1.get()), float(inputr1.get()))

def xminus(event):
    move(float(inputx1.get())-int(slidelen.get()), float(inputy1.get()), float(inputz1.get()), float(inputr1.get()))

def yplus(event):
    move(float(inputx1.get()), float(inputy1.get())+int(slidelen.get()), float(inputz1.get()), float(inputr1.get()))

def yminus(event):
    move(float(inputx1.get()), float(inputy1.get())-int(slidelen.get()), float(inputz1.get()), float(inputr1.get()))

def zplus(event):
    move(float(inputx1.get()), float(inputy1.get()), float(inputz1.get())+int(slidelen.get()), float(inputr1.get()))

def zminus(event):
    move(float(inputx1.get()), float(inputy1.get()), float(inputz1.get())-int(slidelen.get()), float(inputr1.get()))
    
def rplus():
    move(float(inputx1.get()), float(inputy1.get()), float(inputz1.get()), float(inputr1.get())+int(slidelen.get()))

def rminus():
    move(float(inputx1.get()), float(inputy1.get()), float(inputz1.get()), float(inputr1.get())-int(slidelen.get()))

def close_window(): 
    #move(0, 0, -228.3, 0)
    root.quit()


def quit(event):
    root.quit()


GoBtn = Button(root, text="GO ", padx=36, pady=16, command=lambda:move(float(inputx1.get()), float(inputy1.get()), float(inputz1.get()), float(inputr1.get())), fg='blue', highlightbackground='#49ff01')
GoBtn.place(x=410, y=10)

slide1 = Scale(root, from_=-10000, to=10000, orient=HORIZONTAL, length=100)
slide1.place(x=10, y=80)
slide1.set(2809)

slide2 = Scale(root, from_=-10000, to=10000, orient=HORIZONTAL, length=100)
slide2.place(x=110, y=80)
slide2.set(2809)

slide3 = Scale(root, from_=-10000, to=10000, orient=HORIZONTAL, length=100)
slide3.place(x=210, y=80)
slide3.set(2809)

slide4 = Scale(root, from_=-9000, to=9000, orient=HORIZONTAL, length=100)
slide4.place(x=310, y=80)
slide4.set(0)

slide5 = Scale(root, from_=10, to=-800, orient=HORIZONTAL, length=100)
slide5.place(x=10, y=150)
slide5.set(0)

slide6 = Scale(root, from_=10, to=-800, orient=HORIZONTAL, length=100)
slide6.place(x=110, y=150)
slide6.set(0)

slide7 = Scale(root, from_=10, to=-800, orient=HORIZONTAL, length=100)
slide7.place(x=210, y=150)
slide7.set(0)

slide8 = Scale(root, from_=-600, to=600, orient=HORIZONTAL, length=100)
slide8.place(x=310, y=150)
slide8.set(0)

slide9 = Scale(root, from_=-110, to=110, orient=HORIZONTAL, length=100)
slide9.place(x=10, y=220)
slide9.set(0)

'''slide11 = Scale(root, from_=0, to=1, orient=HORIZONTAL, length=100)
slide11.place(x=10, y=270)
slide11.set(0)
'''

xlabel = Label(root, text="X")
xlabel.place(x= 10, y=15)

ylabel = Label(root, text="Y")
ylabel.place(x= 110, y=15)

zlabel = Label(root, text="Z")
zlabel.place(x= 210, y=15)

rlabel = Label(root, text="R")
rlabel.place(x= 310, y=15)

a1label = Label(root, text="Angle1")
a1label.place(x= 10, y=60)

a2label = Label(root, text="Angle2")
a2label.place(x= 110, y=60)

a3label = Label(root, text="Angle3")
a3label.place(x= 210, y=60)

a4label = Label(root, text="Angle4")
a4label.place(x= 310, y=60)

s1label = Label(root, text="Step1")
s1label.place(x= 10, y=130)

s2label = Label(root, text="Step2")
s2label.place(x= 110, y=130)

s3label = Label(root, text="Step3")
s3label.place(x= 210, y=130)

s4label = Label(root, text="Step4")
s4label.place(x= 310, y=130)

cvlabel = Label(root, text="conveyor speed")
cvlabel.place(x= 10, y=200)


Jog = Button(root, text="Jog", padx=40, pady=15, command=lambda:jog(), fg='black', highlightbackground='#07e0ff')
Jog.place(x=510, y=60)

Line = Button(root, text="Line", padx=40, pady=15, command=lambda:line(), fg='black', highlightbackground='#004ef5')
Line.place(x=620, y=60)

Heart = Button(root, text="Heart", padx=40, pady=15, command=lambda:star(), fg='black', highlightbackground='#f5b400')
Heart.place(x=730, y=10)

Home = Button(root, text="Home", padx=40, pady=15, command=lambda:home(), fg='black', highlightbackground='#f75f00')
Home.place(x=620, y=10)

Pop = Button(root, text="Popup", padx=40, pady=15, command=lambda:picknplace(), fg='black', highlightbackground='#00f59f')
Pop.place(x=730, y=60)

Escape = Button(root, text="EXIT", padx=40, pady=15, command=lambda:close_window(), fg='black',highlightbackground='#ff0000')
Escape.place(x=880, y=10)

Convey = Button(root, text="Convey", padx=40, pady=15, command=lambda:convey(), fg='black', highlightbackground='#f75f00')
Convey.place(x=120, y=220)

FW = Button(root, text="⇧", padx=40, pady=10, command=lambda:yplus(0), fg='black', highlightbackground='#07e0ff')
FW.place(x=510, y=140)

BW = Button(root, text="⇩", padx=40, pady=10, command=lambda:yminus(0), fg='black', highlightbackground='#07e0ff')
BW.place(x=510, y=280)

LF = Button(root, text="⇦", padx=10, pady=40, command=lambda:xminus(0), fg='black', highlightbackground='#07e0ff')
LF.place(x=440, y=180)

RG = Button(root, text="⇨", padx=10, pady=40, command=lambda:xplus(0), fg='black', highlightbackground='#07e0ff')
RG.place(x=640, y=180)

RLF = Button(root, text="⤽", padx=6, pady=30, command=lambda:rplus(0), fg='black', highlightbackground='#07e0ff')
RLF.place(x=486, y=190)

RRG = Button(root, text="⤼", padx=6, pady=30, command=lambda:rminus(0), fg='black', highlightbackground='#07e0ff')
RRG.place(x=600, y=190)

UP = Button(root, text="⬆", padx=30, pady=10, command=lambda:zplus(0), fg='black', highlightbackground='#07e0ff')
UP.place(x=520, y=185)

DW = Button(root, text="⬇", padx=30, pady=10, command=lambda:zminus(0), fg='black', highlightbackground='#07e0ff')
DW.place(x=520, y=235)

Pick = Button(root, text="Pick", padx=20, pady=15, command=lambda:pick(), fg='black', highlightbackground='#07e0ff')
Pick.place(x=10, y=280)

Hold = Button(root, text="Hold", padx=19, pady=15, command=lambda:hold(), fg='black', highlightbackground='#07e0ff')
Hold.place(x=10, y=350)

Plac = Button(root, text="Place", padx=16, pady=15, command=lambda:place(), fg='black', highlightbackground='#07e0ff')
Plac.place(x=10, y=420)

slidelen = Scale(root, from_=0, to=20, orient=HORIZONTAL, length=100)
slidelen.place(x=510, y=340)
slidelen.set(5)

steplen = Label(root, text="Jog length")
steplen.place(x= 520, y=320)

adR = Label(root, text="Adjust R")
adR.place(x= 300, y=240)

ARpl = Button(root, text="↺", padx=10, pady=10, command=lambda:rplus(0), fg='black', highlightbackground='#07e0ff')
ARpl.place(x=280, y=260)

ARmi = Button(root, text="↻", padx=10, pady=10, command=lambda:rminus(0), fg='black', highlightbackground='#07e0ff')
ARmi.place(x=340, y=260)

savere = Button(root, text="Teach", padx=10, pady=15, command=lambda:pick(), fg='black', highlightbackground='#07e0ff')
savere.place(x=150, y=380)

automode = Button(root, text="Auto mode", padx=10, pady=15, command=lambda:hold(), fg='black', highlightbackground='#07e0ff')
automode.place(x=240, y=380)

deletere = Button(root, text="Delete record", padx=10, pady=15, command=lambda:place(), fg='black', highlightbackground='#07e0ff')
deletere.place(x=350, y=380)

autorepeat = Scale(root, from_=0, to=10, orient=HORIZONTAL, length=100)
autorepeat.place(x=240, y=430)
autorepeat.set(1)

root.bind('<Return>', enter)
root.bind('<KeyPress>', onKeyPress)
root.bind('<Shift-Escape>', quit)
root.bind('<Shift-Left>', xplus )
root.bind('<Shift-Right>', xminus )
root.bind('<Shift-Up>', yplus )
root.bind('<Shift-Down>', yminus )
root.bind('<Prior>', zplus )
root.bind('<Next>', zminus )
root.bind('<Home>', zminus )

root.mainloop()

