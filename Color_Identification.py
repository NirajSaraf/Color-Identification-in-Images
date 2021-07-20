# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 23:21:55 2021

@author: niraj
"""
#Python Libraries: Pandas, OpenCV
import cv2
import pandas as pd

img_path = 'image.jpg'   #IMAGE PATH
csv = 'colors.csv'  #COLORS.CSV PATH

# reading csv file
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
data = pd.read_csv(csv, names=index, header=None)

# reading image
img = cv2.imread(img_path)
img = cv2.resize(img, (800,600))

# global variables
clicked = False
r = g = b = xpos = ypos = 0

#function to calculate minimum distance from all colors and get the most matching color
def colorName(R,G,B):
	minimum = 1000
	for i in range(len(data)):
		d = abs(R - int(data.loc[i,'R'])) + abs(G - int(data.loc[i,'G'])) + abs(B - int(data.loc[i,'B']))
		if d <= minimum:
			minimum = d
			cname = data.loc[i, 'color_name']

	return cname

#function to get x,y coordinates of mouse double click
def draw(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		global b, g, r, xpos, ypos, clicked
		clicked = True
		xpos = x
		ypos = y
		b,g,r = img[y,x]
		b,g,r = int(b),int(g), int(r)

# create window
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw)

while True:
	cv2.imshow('image', img)
	if clicked:
		#cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
		cv2.rectangle(img, (20,20), (600,60), (b,g,r), -1)

		#Creating text string to display( Color name and RGB values )
		text = colorName(r,g,b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
		#cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
		cv2.putText(img, text, (50,50), 2,0.8, (255,255,255),2,cv2.LINE_AA)

		#For very light colours we will display text in black colour
		if r+g+b >=600:
			cv2.putText(img, text, (50,50), 2,0.8, (0,0,0),2,cv2.LINE_AA)

	if cv2.waitKey(20) & 0xFF == 27:
		break

cv2.destroyAllWindows()