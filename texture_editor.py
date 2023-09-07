"""this code should take in a map texture, and create new files from it for color correction,
land/water isolation, and heightmap."""

import cv2


def color_correction(img):
    """this function takes in an image and saturates the colors to make them more vibrant.
    It also darkens the blue and green colors."""
    # convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # split into channels
    h, s, v = cv2.split(hsv)
    # increase saturation
    s = s + 25

    # increase hue
    h = h + 10

    # decrease value
    v = v - 25
    # merge channels
    hsv = cv2.merge([h, s, v])

    # convert back to bgr
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)





    return img


def land_water_isolation(img):
    """This should isolate all of the blue pixels on the map, and make them white, while all other pixels are black."""
    # read in image
    img = cv2.imread(img)
    # find all pixels that are mostly blue based on hue
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # split into channels
    h, s, v = cv2.split(hsv)
    # create mask
    mask = cv2.inRange(h, 100, 130)
    # apply mask
    img = cv2.bitwise_and(img, img, mask=mask)
    # convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def height_map(img, land_water):
    """This should take in an map image, and create a heightmap from it. Should return a grayscale image, where white is high, and black is low."""
    # read in image
    img = cv2.imread(img)
    # convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # invert colors
    img = cv2.bitwise_not(img)
    # adjust color levels to make it more contrasty
    img = cv2.equalizeHist(img)
    # use land/water image as a mask to make water black
    mask = cv2.imread(land_water)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    # invert mask
    mask = cv2.bitwise_not(mask)
    img = cv2.bitwise_and(img, img, mask=mask)
    # invert colors
    img = cv2.bitwise_not(img)




    return img




def main():
    """this is the main function."""
    # read in image
    img = cv2.imread("map.png")
    # correct colors
    img = color_correction(img)
    # save image
    cv2.imwrite("map_corrected.png", img)

    # isolate land and water
    img = land_water_isolation("map_corrected.png")
    # save image
    cv2.imwrite("map_land_water.png", img)

    # generate heightmap
    img = height_map("map_corrected.png", "map_land_water.png")
    # save image
    cv2.imwrite("heightmap.png", img)


if __name__ == "__main__":
    main()
