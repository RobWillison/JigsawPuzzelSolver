import cv2



def isolatePeice(image, box):
    x,y,w,h = box
    img = image[y-10:y+h+10, x-10:x+w+10]
    edges = cv2.Canny(img, 100, 200)
    im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    longest_contour = sorted(contours, key=lambda c: cv2.arcLength(c, False))[-1]
    print(longest_contour)
    cv2.drawContours(img, [longest_contour], -1, (0,255,0), 1)
    cv2.imshow('contours',img)
    cv2.waitKey(0)
