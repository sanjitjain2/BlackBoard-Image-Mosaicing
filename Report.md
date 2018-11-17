# Multimedia Processing and Applications
## Blackboard Image Mosaicing
## Project Report by
* 16UCS169 Sanjit Jain
* 16UCS075 Harshit Agarwal 

How to run the script:
`python mosiac.py [run-type]`
> run-type = 0 to use predefined points for stitching images

> run-type = 1 to manually select 8 points to stitch images

**Images that are to be stitched:**
![image](https://github.com/sanjitjain2/BlackBoard-Image-Mosaicing/blob/master/m0.jpg)

![image](https://github.com/sanjitjain2/BlackBoard-Image-Mosaicing/blob/master/m1.jpg)

![image](https://github.com/sanjitjain2/BlackBoard-Image-Mosaicing/blob/master/m2.jpg)

![image](https://github.com/sanjitjain2/BlackBoard-Image-Mosaicing/blob/master/m3.jpg)

![image](https://github.com/sanjitjain2/BlackBoard-Image-Mosaicing/blob/master/m4.jpg)

![image](https://github.com/sanjitjain2/BlackBoard-Image-Mosaicing/blob/master/m5.jpg)

**Our Result after stitching images:**

![image](https://github.com/sanjitjain2/BlackBoard-Image-Mosaicing/blob/master/result012345.jpg)

## Theory on Image Mosaicing
Image stitching or photo stitching is the process of combining multiple photographic images with overlapping fields of view to produce a segmented panorama or high-resolution image.

Consider a point x = (u,v,1) in one image and
x’=(u’,v’,1) in another image
A homography is a 3 by 3 matrix M.

The homography relates the pixel co-ordinates in the two images if x’ = M * x.
When applied to every pixel the new image is a warped version of the original image

## Our Obervations

## Our Implementation

### Finding Homography Matrix of two images
```
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
```

### Finding New Alligned Corners of Source Image
```
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
```

### Finding minimum and maximum X and Y
```
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
```

### Stitching of the Two Imaegs
```
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
```
