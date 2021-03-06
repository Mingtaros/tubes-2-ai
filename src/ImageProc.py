# Tugas Besar 2
# IF3170 Intelegensi Buatan
# Anggota:
#   13517013 / Aditya Putra Santosa
#   13517048 / Leonardo
#   13517054 / Vinsen Marselino Andreas
#   13517124 / Arvin Yustin
# File: ImageProc.py
# Deskripsi: Penggunaan OpenCV dalam mendeteksi Contour dan sudut untuk dievaluasi Rule-Based System

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
    # print(has)
    for i, h in enumerate(has):
        for j, cek in enumerate(has):
            if(norm(cek-h) < epsTitik and i < j):
                delSoon.update({j})
    titikSimple = [h for idx, h in enumerate(has) if idx not in delSoon]
    return titikSimple

preProc = None

def preProcImg(img, d=15, sigmaColor=93, sigmaSpace=71, kSize=6, thres=47):
    global preProc
    sigma = 0.33
    pp = img.copy()

    #Smoothing Image
    pp = cv2.bilateralFilter(pp, d, sigmaColor, sigmaSpace)
    pp = cv2.cvtColor(pp, cv2.COLOR_BGR2GRAY)
    
    #Morphology Transformation
    kernel = np.ones((kSize, kSize), np.uint8)
    pp = cv2.morphologyEx(pp, cv2.MORPH_GRADIENT, kernel)
    
    #Thresholding
    pp = cv2.threshold(pp,thres,255,cv2.THRESH_BINARY_INV)
    pp = cv2.bitwise_not(pp[1])
    
    # Apply Canny
    v = np.median(pp)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    pp = cv2.Canny(pp, lower, upper)
    pp = cv2.copyTo(img, pp)
    preProc = pp
    pp = cv2.cvtColor(pp, cv2.COLOR_BGR2GRAY)
    return pp


contour = []

def process(img, d=15, sigmaColor=93, sigmaSpace=71, kSize=6, thres=47):
    global contour
    # ctr = img.copy()
    
    pp = preProcImg(img, d, sigmaColor, sigmaSpace, kSize, thres)

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
            approx = cv2.approxPolyDP(contour[conArea[i][0]], 0.01*cv2.arcLength(contour[conArea[i][0]], True), True)
            approx = simplifikasiTitik([a[0] for a in approx], 20) #pixel
            
            if(len(approx) > 2):
                sudut = []
                for j in range(len(approx)-2):
                    p1 = approx[j]
                    p2 = approx[j+1]
                    p3 = approx[j+2]
                    sudut.append(sudutTigaTitik(p1, p2, p3))
                sudut.append(sudutTigaTitik(approx[j+1], approx[j+2], approx[0]))
                sudut.append(sudutTigaTitik(approx[j+2], approx[0], approx[1]))
                sudutPoly.append((conArea[i][0], sudut))

    return sudutPoly

def gambarContour(img, idx):
    global contour
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    x, y = contour[idx][0][0]
    img = cv2.putText(img, str(idx), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
    return cv2.drawContours(img, contour, idx, color, 5)
    