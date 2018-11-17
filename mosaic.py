import numpy as np
import cv2
import sys
import click


def calcHomography(pts1,pts2):
	# Calculate Homography using SVD

	A = np.zeros((8,9),dtype = 'float')

	for i in range(0,8,2):

		A[i][0], A[i][1], A[i][2] = pts1[i/2][0], pts1[i/2][1], 1
		A[i][6], A[i][7], A[i][8] = pts1[i/2][0]*(-1)*pts2[i/2][0], pts1[i/2][1]*(-1)*pts2[i/2][0], (-1)*pts2[i/2][0]

		A[i+1][3], A[i+1][4], A[i+1][5] = pts1[i/2][0], pts1[i/2][1], 1
		A[i+1][6], A[i+1][7], A[i+1][8] = pts1[i/2][0]*(-1)*pts2[i/2][1], pts1[i/2][1]*(-1)*pts2[i/2][1], (-1)*pts2[i/2][1]
	
	# Matrix A created, calculating SVD	
	U,S,V = np.linalg.svd(A)
	
	# Extracting H from V
	V = V[-1,:]/V[-1,-1]
	H = V.reshape(3,3)

	return H

def findNewCorners(r,c,inv_H):


	# Corner coordinates of source image
	initial_corners = [[0,0,1],[c-1,0,1],[0,r-1,1],[c-1,r-1,1]]	

	new_corners = []

	# Iterate over source coordinates to calculate new alligned corner coordinates
	for i in initial_corners:
		coord = np.array(i).reshape(3,1)	
		corner_point = np.dot(inv_H,coord)
		x = int(corner_point[0]/corner_point[2])
		y = int(corner_point[1]/corner_point[2])
		new_corners.append([x,y])


	return new_corners


def findMaxMin(r,c,new_corners):
	base_min_x = 0
	base_min_y = 0

	base_max_x = c-1
	base_max_y = r-1

	min_x = min(base_min_x,new_corners[0][0],new_corners[1][0],new_corners[2][0],new_corners[3][0])
	max_x = max(base_max_x,new_corners[0][0],new_corners[1][0],new_corners[2][0],new_corners[3][0])

	min_y = min(base_min_y,new_corners[0][1],new_corners[1][1],new_corners[2][1],new_corners[3][1])
	max_y = max(base_max_y,new_corners[0][1],new_corners[1][1],new_corners[2][1],new_corners[3][1])


	return min_x,min_y,max_x,max_y


def StichImage(max_x,max_y,min_x,min_y,r,c,H,img1,img2):


	# Creating a new canvas to paste and stitch images on
	canvas = np.full((max_y+1000,max_x+1000,3),255)
	
	row_canvas, col_canvas,_ = canvas.shape
		



	# Translate and paste destiantion image on canvas	
	for y in range(r):
		for x in range(c):
			canvas[y+abs(min_y)][x+abs(min_x)] = img1[y][x]
	



	# Iterate over empty canvas and find corresponding alligned points from source image
	for i in range(min_y,row_canvas-abs(min_y)):
		
		for j in range(min_x,col_canvas-abs(min_x)):
			
			# If point is white, find its alligned point
			if canvas[i+abs(min_y),j+abs(min_x)][0] == 255 and canvas[i+abs(min_y),j+abs(min_x)][1] == 255 and canvas[i+abs(min_y),j+abs(min_x)][2] == 255:
				point = np.array([i,j,1]).reshape(3,1)
				homographed_point = np.dot(H,point)
				row_homographed = int(homographed_point[0]/homographed_point[2])
				col_homographed = int(homographed_point[1]/homographed_point[2])

				# if calculated point lies within source image,bring it into the canvas
				if row_homographed >= 0 and row_homographed < img2.shape[0]:
					if col_homographed >= 0 and col_homographed < img2.shape[1]:
						canvas[i+abs(min_y),j+abs(min_x)] = img2[row_homographed][col_homographed]
	

	return canvas


def main():
	i1 = 'm0.jpg'
	i2 = 'm1.jpg'
	

	# Reading Destination(base) image 
	img1 = cv2.imread(i1)

	# Reading Source(need to be aligned) image
	img2 = cv2.imread(i2)
	
	# dimmensions of Destination image	
	r,c,p = img1.shape

	if (len(sys.argv) == 1) or (len(sys.argv) == 2 and str(sys.argv[1]) == '0'):
		# ---------------Common points---------------------- 

		# pts1 => corner points of destiantion image
		# pts2 => corner points of source image

		"""
		pts1 = [[1543,1924],[918,1705],[1054,584],[1786,960]]			# m0+m1+m2+m3+m4
		pts2 = [[1174,2240],[397,2086],[279,713],[925,882]]				# m5

		"""
		"""
		pts1 = [[1169,2430],[993,1310],[1537,1173],[1527,2674]]			# m0+m1+m2+m3
		pts2 = [[735,1946],[596,375],[979,214],[1131,2385]]				# m4
		"""

		"""
		pts1 = [[1038,2050],[1040,2491],[1273,2119],[1617,2425]]		# m0+m1+m2
		pts2 = [[263,264],[120,1300],[549,365],[1026,978]]				# m3
		"""
		"""
		pts1 = [[894,1766],[971,2484],[1576,1930],[1594,2389]]			# mo+m1
		pts2 = [[519,59],[767,1479],[1289,30],[1618,870]]				# m2
		"""
			
		pts1 = [[1541,1926],[534,1779],[972,2483],[1617,2423]] 			# m0
		pts2 = [[1364,1484],[470,500],[96,2057],[901,2396]]				# m1
	
	else:

		pts1,pts2 = click.main(i1,i2)



	
	# Calculating Homography Matrix
	H = calcHomography(pts1,pts2)

	# Calculating Inverse_homography matrix
	inv_H = np.linalg.inv(H)


	# New corners found by by multiplying with inv_H
	new_corners = findNewCorners(r,c,inv_H)



	# Calculate min_x, max_x, min_y, max_y and offset values

	min_x,min_y,max_x,max_y = findMaxMin(r,c,new_corners)


	new_image = StichImage(max_x,max_y,min_x,min_y,r,c,H,img1,img2)


	# Write and save the final stitched canvas image
	cv2.imwrite('result.jpg',new_image)

main()