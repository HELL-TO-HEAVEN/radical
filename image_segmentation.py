import os
import sys
import cv2
import numpy as np



if (len(sys.argv)<2) or (len(sys.argv)>3):
	print "Usage: python %s <picture> <backround-color> - default backround color is 'white' (use 'b' for 'black')." % __file__ 
	print "Please run the script again!"
	sys.exit(-1)

elif (len(sys.argv)==3) and (sys.argv[2]=='b'):
	factor = 0.2
	use_inverse = 0

else:
	factor = 0.4
	use_inverse = 1

img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
if use_inverse:
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
else:
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


# noise removal
kernel = np.ones((3,3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 2)

# sure background area
sure_bg = cv2.dilate(opening, kernel, iterations=3)

# sure foreground area
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
ret, sure_fg = cv2.threshold(dist_transform, factor*dist_transform.max(), 255, 0)

# unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg, sure_fg)

ret, markers = cv2.connectedComponents(sure_fg)

# background is 1
markers = markers+1

# region of unknown is 0
markers[unknown==255] = 0

markers = cv2.watershed(img, markers)
img[markers == -1] = [0,255,0]


cv2.imwrite('out_'+sys.argv[1] , img)
