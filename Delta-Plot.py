import random
import time
import csv
from  math import sin, cos , pow , sqrt , pi
from inversegeo4 import t1, t2, t3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.animation import FuncAnimation


fig = plt.figure()
fig.canvas.set_window_title('Delta Robot Simulation')

ax1 = fig.add_subplot(111, projection='3d')
ax1.set_autoscale_on(False)
plt.suptitle('Delta Robot Simulation ')
plt.axis([-400,400, -400,400])


wp = 35.25
gp = round(wp/2, 2)
ep = round(sqrt(3)*wp/2, 2)

a = 0
x= 0
y = 0
z = -260
X = []
Y = []
Z = []
def animate(i):
    ax1.clear()
    bl = 200
    '''global a
    a = a + pi/8
    x = -80*cos(a)
    y = 80*sin(a)
    z = -280
    x = float(input("x = "))
    y = float(input("y = "))
    z = -float(input("z = "))'''

    data = []
    with open('position.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        #for row in readCSV:
            #data.append(row[1])
        data = [row for row in readCSV]

    x = float(data[0][1])
    y = float(data[1][1])
    z = float(data[2][1])

    xb = [0, -88.33, 88.33, 0]
    yb = [102, -51, -51, 102 ]
    zb = [0, 0, 0, 0 ]

    xc = [-bl , bl, bl, -bl, -bl , bl, bl, -bl ]
    yc = [-bl, -bl, bl , bl, -bl, -bl, bl , bl ]
    zc = [100, 100, 100, 100 , -400, -400, -400, -400 ]

    xp = [x,       x + ep, x - ep,  x,      x]
    yp = [y + wp , y - gp, y - gp, y + wp, y ]
    zp = [z, z, z, z, z ]

    xa1 = t1(x, y, z)[1]
    xa2 = t2(x, y, z)[1]
    xa3 = t3(x, y, z)[1]

    ya1 = t1(x, y, z)[2]
    ya2 = t2(x, y, z)[2]
    ya3 = t3(x, y, z)[2]

    za1 = t1(x, y, z)[3]
    za2 = t2(x, y, z)[3]
    za3 = t3(x, y, z)[3]

    #print(f" L2 is: {sqrt(pow(xa2-(x+ep), 2) + pow(ya2-(y-gp), 2) + pow(za2-z, 2) )} ")

    Ax1 = [0, xa1, x ] 
    Ay1 = [102, ya1, y + wp]
    Az1 = [0, za1, z ]

    Ax2 = [88.33, xa2, x + ep ]
    Ay2 = [ -51, ya2, y - gp ]
    Az2 = [0, za2, z ]

    Ax3 = [-88.33, xa3, x - ep]
    Ay3 = [ -51, ya3, y - gp ]
    Az3 = [0, za3, z]

    X.append(x)
    Y.append(y)
    Z.append(z)

    #time.sleep(1)
    ax1.plot(xb,yb,zb)
    ax1.plot(xp, yp, zp)

    ax1.plot(X, Y, Z, 'r')

    ax1.plot(Ax1, Ay1, Az1, 'k')
    ax1.plot(Ax2, Ay2, Az2, 'k')
    ax1.plot(Ax3, Ay3, Az3, 'k')

    ax1.scatter(xp, yp, zp, c='r', marker ="*")
    ax1.scatter(xb, yb, zb, c='b', marker ="o")

    ax1.scatter(xa1, ya1, za1, c='c', marker ="o")
    ax1.scatter(xa2, ya2, za2, c='c', marker ="o")
    ax1.scatter(xa3, ya3, za3, c='k', marker ="o")

    ax1.scatter(xc, yc, zc, c='g', marker =".")


def runplot():
    ani = FuncAnimation(plt.gcf(), animate, interval = 200)

    plt.tight_layout()
    plt.show()
runplot()
