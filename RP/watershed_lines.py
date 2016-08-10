import os
import sys
import numpy as np

from scipy import ndimage
from skimage import feature
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu, sobel
from skimage.feature import peak_local_max
from skimage.morphology import watershed

from skimage import io
io.use_plugin('pil')



#-------------------------------------------------------------------------------

if (len(sys.argv)<3) or (len(sys.argv)>4):
	print "Usage: python %s <index of first image to process> <index of last image to process> \
				<backround> - default bright (use 'd' for 'dark')." % __file__ 
	print "Please run the script again!"
	sys.exit(-1)

elif (len(sys.argv)==4) and (sys.argv[3]=='d'):
	bright_backround = 0

else:
	bright_backround = 1


path = '/oasis/scratch/comet/statho/temp_project/Dataset_2GB/'
path_for_input = path + 'inputs/file_'
path_for_output =  path + 'outputs/out_file_'

read_from = int(sys.argv[1])
read_until = int(sys.argv[2])  


while read_from <= read_until:
	
	image = path_for_input + str(read_from) + '.BMP'
	img = io.imread(image)
	img_gray = rgb2gray(img)

	thresh = threshold_otsu(img_gray)

	if bright_backround:
		foreground_mask = img_gray <= thresh          #for bright backround
	else:
		foreground_mask = img_gray > thressh 		  #for dark backround


	# compute the Euclidean distance from every binary pixel to the nearest zero pixel 
	# and then find peaks in this distance map
	#
	D = ndimage.distance_transform_edt(foreground_mask)

	localMax = peak_local_max(D, indices=False, min_distance=30, labels=foreground_mask)

	# perform a connected component analysis on the local peaks,
	# using 8-connectivity, then apply the Watershed algorithm
	#
	markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
	labels = watershed(-D, markers, mask=foreground_mask)

	#print "In image {}, there are {} segments found!".format(image, len(np.unique(labels)) - 1)


	# loop over the unique labels returned by the Watershed algorithm
	#
	for label in np.unique(labels):
	
		# if the label is zero, we are examining the 'background' so ignore it
		#
		if label == 0:
			continue

		mask = np.zeros(img_gray.shape, dtype="uint8")	
		mask[labels == label] = 255

		edge_sobel = sobel(mask)	
		img[edge_sobel > 0] = [0,255,0] 

	io.imsave(path_for_output + str(read_from) + '.BMP', img)

	read_from += 1

#-------------------------------------------------------------------------------
