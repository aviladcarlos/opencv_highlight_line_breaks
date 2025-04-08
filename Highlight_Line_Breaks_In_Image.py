import cv2
import numpy as np


# Determines if a point is an endpoint by checking the value of adjacent pixels/points. If only 1 adjacent pixel is
# considered to be part of the drawn line(value 255) then it is considered to be an endpoint.
def get_end_pnts(points, image):

    endpoints = []

    # Converts values of numpy array from uint8 (0 to 255) to uint16 (0 to 65535) to fix the overflow error caused by
    # the value 'n' being over 255 which is the limit of uint8.
    image = image.astype("uint16")

    for point in points:

        x = point[0]
        y = point[1]
        n = 0

        n += image[y - 1, x]
        n += image[y - 1, x - 1]
        n += image[y - 1, x + 1]
        n += image[y, x - 1]
        n += image[y, x + 1]
        n += image[y + 1, x]
        n += image[y + 1, x - 1]
        n += image[y + 1, x + 1]
        n /= 255

        if n == 1:
            endpoints.append(point)

    return endpoints


# Loads image in grayscale
img = cv2.imread('Example_Image_JPEG.jpg', cv2.IMREAD_GRAYSCALE)

# Converts the image from gray to color
img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# Copy of img_color that will be used later to make highlighted areas transparent
overlay = img_color.copy()

# Coverts image to a binary image (foreground: white, background: black)
# Values: white = 255 and black = 0
# cv2.THRESH_OTSU, uses the image histogram to determine the ideal global threshold value
# cv2.THRESH_BINARY_INV, all pixels that equal or higher than threshold are set to the value 0
# all other pixels are set to a value of 255
# thresh_used is threshold value cv2.THRESH_OTSU choose
# img is a 2D Numpy array of the image, img[y-coordinate, x-coordinate] = value of given pixel 0 or 255
threshold_used, img = cv2.threshold(img, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)

# Reduces the regions of the image where the value of the pixels is set to 255 to a single pixel
# at the center the region creating a skeleton effect
img = cv2.ximgproc.thinning(img)

# Filters for all pixels with a value that is not zero in the image
# Returned  3D array (n, 1, 2) where n is the number of nonzero pixels found
# and 2 is the coordinates which are formatted as [x-coordinate, y-coordinate]
# the middle dimension (1) is used for compatibility with other OpenCV functions
pnts = cv2.findNonZero(img)

# Removes single-dimensional entries from the shape of the array, in this case the middle dimension(1) in (n, 1, 2)
pnts = np.squeeze(pnts)

# Finds and returns the endpoints of the image
endpnts = get_end_pnts(pnts, img)


# Draws a filled red circle at each endpoint on the overlay image
for pnt in endpnts:
    cv2.circle(overlay, (pnt[0], pnt[1]), 10, (0, 0, 255), -1)

# Level of transparency
alpha = 0.5

# Blends two images together based on the transparency set for each image
final_img = cv2.addWeighted(overlay, alpha, img_color, 1 - alpha, 0)

# Displays final_img in a pop-up window that is close by pressing any key
cv2.imshow('Line_Breaks_Detected', final_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Saves the final_img, uncomment if you want to save the file
# cv2.imwrite('Line_Breaks_Detected.jpg', final_img)
