import math    
from math import cos, sin, acos, asin, sqrt, degrees, radians, pi

L = 100
l = 316
wb = 102
wp = 35.25
gp = wp/2
ep = sqrt(3)*wp/2
sqt3 = sqrt(3)
m = (sqt3*66.75)/2
n = 66.75/2
k = wb - wp

def t1(x,y,z):
    x2 = x * x
    y2 = y * y
    z2 = z * z
    L2 = L * L
    l2 = l * l

    a1 = 2*(k-y)
    a2 = 2* z
    a3 = x2 + y2 + z2 + L2 - l2 - k*k
    a4 = 1 + (a1/a2)*(a1/a2)
    a5 = -2 * (k - (a3*a1)/(a2*a2))
    a6 = k*k + (a3/a2)*(a3/a2) - L2
    
    yv = (-a5 + (sqrt(a5*a5 - 4* a4 * a6)))/(2* a4)
    zv = (a1*yv+a3)/a2
    dv = yv - k

    xA = 0
    yA = yv + wp
    zA = zv 

    t1 = acos(dv/L)
    t1 = round(degrees(t1), 3)#use this line for degree
    #t1 = round(t1, 9)             #use this line for radian
    if zv<= 0:
        t1 = -t1
    return [t1, xA, yA, zA] 

def t2(x,y,z):
    x2 = x * x
    y2 = y * y
    z2 = z * z
    L2 = L * L
    l2 = l * l
    sqt3 = sqrt(3)

    b1 = -2*(-sqt3*x + y + sqt3*m + n)  # remove (-) at sqt3*x for theta3 
    b2 = 2* z
    b3 = x2 + y2 + z2 + L2 - l2 - m*m - n*n
    b4 = 4 + (b1/b2)*(b1/b2)
    b5 = 2 * (sqt3*m + n + (b1*b3)/(b2*b2))
    b6 = m*m + n*n + (b3/b2)*(b3/b2) - L2

    yv = (-b5 - (sqrt(b5*b5 - 4* b4 * b6)))/(2* b4)
    zv = (b1*yv + b3)/b2
    xv = -sqrt(3)*yv

    yA = yv - gp
    zA = zv
    xA = xv + ep

    dv = abs(2*yv + k)
    t2 = acos(dv/L)
    t2 = round(degrees(t2), 3)#use this line for degree
    #t2 = round(t2, 9)             #use this line for radian
    if zv<= 0:
        t2 = -t2
    #print(f" L2 is: {sqrt(pow(xv-(x), 2) + pow(yv-(y), 2) + pow(zv-z, 2) )} ")
    return [t2, xA, yA, zA]

def t3(x,y,z):
    x2 = x * x
    y2 = y * y
    z2 = z * z
    L2 = L * L
    l2 = l * l
    sqt3 = sqrt(3)

    c1 = -2*(sqt3*x + y + sqt3*m + n)  
    c2 = 2* z
    c3 = x2 + y2 + z2 + L2 - l2 - m*m - n*n
    c4 = 4 + (c1/c2)*(c1/c2)
    c5 = 2 * (sqt3*m + n + (c1*c3)/(c2*c2))
    c6 = m*m + n*n + (c3/c2)*(c3/c2) - L2

    yv = (-c5 - (sqrt(c5*c5 - 4* c4 * c6)))/(2* c4)
    zv = (c1*yv + c3)/c2

    yA = yv - gp
    zA = zv
    xA = sqrt(3)*yA

    dv = abs(2*yv + k)
    t3 = acos(dv/L)
    t3 = round(degrees(t3), 3) #use this line for degree
    #t3 = round(t3, 9)              #use this line for radian
    if zv<= 0:
        t3 = -t3
    return [t3, xA, yA, zA]

'''x = 50
y = 0
z = -300
theta1 = t1(x, y, z)[0]
theta2 = t2(x, y, z)[0]
theta3 = t3(x, y, z)[0]
zA1 = t1(x, y, z)[3]
zA2 = t2(x, y, z)[3]
zA3 = t3(x, y, z)[3]
print(theta1)
print(theta2)
print(theta3)
print(f" zA1 , zA2 , zA3 : {zA1} {zA2} {zA3} ")
a = 0
while a< 4*pi:
    x = 100*cos(a)
    y = 100*sin(a)
    z = -260
    theta2 = t2(x, y, z)[0]
    a = a + pi/8'''
