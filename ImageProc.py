import cv2
from random import randint
import numpy as np
from numpy.linalg import norm
from functools import reduce

def sekip(x):
    pass

def show(x, name):
    cv2.imshow(name, x)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def sudutTigaTitik(a, b, c):
    # Return sudut antara garis a-b dan b-c
    vAB = b - a
    vBC = b - c
    
    dot = np.dot(vAB, vBC)
    dAB = norm(vAB)
    dBC = norm(vBC)
    
    temp = dot/(dAB * dBC)
    temp = max(temp, -1)
    temp = min(temp, 1)
    return np.rad2deg(np.arccos(temp))

def DouglasPeucker(titik, eps):
    dmax = 0
    index = 0
    end = len(titik)
    pEnd = titik[end-1][0]
    pStart = titik[0][0]
    for i in range(2, end-1):
        p = titik[i][0]
        d = norm(np.cross(pEnd-pStart, pStart-p))/norm(pEnd-pStart)
        if(d > dmax):
            index = i
            dmax = d
    hasil = []
    if(dmax > eps):
#         Rekursif
        hasil1 = DouglasPeucker(titik[:index], eps)
        hasil2 = DouglasPeucker(titik[index:], eps)
        hasil = hasil1 + hasil2
    else:
        hasil = [pStart, pEnd]
    return hasil

def simplifikasiTitik(has, epsTitik):
    delSoon = set([])
    for i, h in enumerate(has):
        for j, cek in enumerate(has):
            if(norm(cek-h) < epsTitik and i < j):
                delSoon.update({j})
    titikSimple = [h for idx, h in enumerate(has) if idx not in delSoon]
    return titikSimple

def createTrackbar():
    cv2.namedWindow('setting')
    cv2.createTrackbar('d', 'setting', 14, 50, sekip)
    cv2.createTrackbar('sigmaColor', 'setting', 93, 200, sekip)
    cv2.createTrackbar('sigmaSpace', 'setting', 71, 200, sekip)
    cv2.createTrackbar('kSize', 'setting', 6, 10, sekip)
    cv2.createTrackbar('thres', 'setting', 47, 255, sekip)

def preProcImg(img):
    # createTrackbar()
    sigma = 0.33
    pp = img.copy()

    #Smoothing Image
    d = 15 # cv2.getTrackbarPos('d', 'setting')+1
    sigmaColor = 93 # cv2.getTrackbarPos('sigmaColor', 'setting')
    sigmaSpace = 71 # cv2.getTrackbarPos('sigmaSpace', 'setting')
    pp = cv2.bilateralFilter(pp, d, sigmaColor, sigmaSpace)
    pp = cv2.cvtColor(pp, cv2.COLOR_BGR2GRAY)
    
    #Morphology Transformation
    kSize = 6 # cv2.getTrackbarPos('kSize', 'setting')
    kernel = np.ones((kSize, kSize), np.uint8)
    pp = cv2.morphologyEx(pp, cv2.MORPH_GRADIENT, kernel)
    
    #Thresholding
    thres = 47 # cv2.getTrackbarPos('thres', 'setting')
    pp = cv2.threshold(pp,thres,255,cv2.THRESH_BINARY_INV)
    pp = cv2.bitwise_not(pp[1])
    
    # Apply Canny
    v = np.median(pp)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    pp = cv2.Canny(pp, lower, upper)
    pp = cv2.copyTo(img, pp)
    pp = cv2.cvtColor(pp, cv2.COLOR_BGR2GRAY)
    return pp


contour = []

def process(img):
    global contour
    ctr = img.copy()
    
    pp = preProcImg(img)

    #Contour detection
    contour, tree = cv2.findContours(pp, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    conArea = [(i,cv2.contourArea(c)) for i,c in enumerate(contour)]
    conArea.sort(key=lambda x : x[1], reverse=True)
    maxNumContour = 30
    eps = 30
    epsTitik = 30
        
    sudutPoly = []
    # print(tree[0][22])
    for i in range(min(len(conArea), maxNumContour)):
            # print(" YES")
    #         has = simplifikasiTitik(DouglasPeucker(con[conArea[i][0]], eps), epsTitik)
            approx = cv2.approxPolyDP(contour[conArea[i][0]], 0.01*cv2.arcLength(contour[conArea[i][0]], True), True)
            approx = simplifikasiTitik([a[0] for a in approx], 20) #pixel
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
            ctr = cv2.drawContours(ctr, contour, 22, color, 3)
            # for a in approx:
            #     x,y = a[0]
            #     ctr = cv2.circle(ctr, (x, y), 3, (0, 0, 255), 3)
            if(len(approx) > 2):
                sudut = []
                # print(conArea[i][0]," ",approx, end=" ")
                for j in range(len(approx)-2):
                    # print(j, end=", ")
                    p1 = approx[j]
                    p2 = approx[j+1]
                    p3 = approx[j+2]
                    sudut.append(sudutTigaTitik(p1, p2, p3))
                # print("")
                sudut.append(sudutTigaTitik(approx[j+1], approx[j+2], approx[0]))
                sudut.append(sudutTigaTitik(approx[j+2], approx[0], approx[1]))
                sudutPoly.append((conArea[i][0], sudut))
                # print(conArea[i][0], " | ", sudut, " | ", approx)
    # show(ctr,"bangsat")
    # print(sudutPoly)
    # print(contour[22])
    return sudutPoly

def gambarContour(img, idx):
    global contour
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    x, y = contour[idx][0][0]
    # print(x, ' ', y)
    img = cv2.putText(img, str(idx), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
    # color = (0, 0, 255)
    # print(contour[idx])
    return cv2.drawContours(img, contour, idx, color, 3)
    