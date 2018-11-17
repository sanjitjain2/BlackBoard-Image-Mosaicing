import argparse
import cv2
import numpy as np
import time
pts1 = []
count = 0
img1 = []

def clickCoord(event,x,y,flags,param):
	
	global pts1,count

	# When user does left click
	if event == cv2.EVENT_LBUTTONDOWN:
		if count < 4:
			# store the coordinates
			pts1.append([x,y])

		# Increment click count
		count = count + 1
		
		# Create the polygon withe the points as vertices
		if count > 1 and count<5:
			cv2.polylines(img1,[np.array(pts1).reshape((-1,1,2))],True,(0,0,255),10)

def main(a1,a2):	

	# a1 and a2 are the images to be read

	global pts1,count,img1			
	img1 = cv2.imread(a1)

	cv2.namedWindow("image1",cv2.WINDOW_NORMAL)
	cv2.resizeWindow("image1", 1000,1000)
	cv2.setMouseCallback("image1", clickCoord)

	while True:
		cv2.imshow("image1",img1)
		key = cv2.waitKey(1) & 0xFF

		if key == ord("e") or count == 5:
			print "4 points recorded"
			break

	print pts1

	# Storing the points of a1 in point1
	point1 = pts1
	pts1 = []

	# Now getting the points for a2

	img1 = cv2.imread(a2)

	cv2.namedWindow("image2",cv2.WINDOW_NORMAL)
	cv2.resizeWindow("image2", 800,800)
	cv2.setMouseCallback("image2", clickCoord)
	count = 0
	"""
	if __name__ == "__main__":
		main()
	"""

	while True:
		cv2.imshow("image2",img1)
		key = cv2.waitKey(1) & 0xFF

		if key == ord("e") or count == 5:
			print "4 points recorded"
			break

	print pts1

	cv2.destroyAllWindows() 
	return point1,pts1
