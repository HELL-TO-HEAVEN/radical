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


if (len(sys.argv)<2) or (len(sys.argv)>3):
	print "Usage: python %s <picture> <backround> - default dark (use 'b' for 'bright')." % __file__ 
	print "Please run the script again!"
	sys.exit(-1)

elif (len(sys.argv)==3) and (sys.argv[2]=='b'):
	bright_backround = 1

else:
	bright_backround = 0


img = io.imread(sys.argv[1])

img_gray = rgb2gray(img)

thresh = threshold_otsu(img_gray)

if bright_backround:
	foreground_mask = img_gray <= thresh          #for bright backround
else:
	foreground_mask = img_gray > thresh 		  #for dark backround


# compute the exact Euclidean distance from every binary
# pixel to the nearest zero pixel, then find peaks in this
# distance map
D = ndimage.distance_transform_edt(foreground_mask)

localMax = peak_local_max(D, indices=False, min_distance=20, labels=foreground_mask)

# perform a connected component analysis on the local peaks,
# using 8-connectivity, then apply the Watershed algorithm
markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
labels = watershed(-D, markers, mask=foreground_mask)

print "There are {} segments found!".format(len(np.unique(labels)) - 1)


# loop over the unique labels returned by the Watershed
# algorithm

mask = np.zeros(img_gray.shape, dtype="uint8")

for label in np.unique(labels):

	# if the label is zero, we are examining the 'background' so simply ignore it
	if label == 0:
		continue

	mask[labels == label] = 255

io.imsave('outputs_mask/out_'+sys.argv[1], mask)
