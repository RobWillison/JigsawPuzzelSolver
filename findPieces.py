#!/usr/bin/python

# Standard imports
import cv2
import numpy as np
import imutils
from isolatePiece import isolatePeice

def area(box):
    return box[2] * box[3]

def calculate_overlap(box1, box2):
    b1x, b1y, b1w, b1h = box1
    b2x, b2y, b2w, b2h = box2
    x_overlap = max(0, min(b1x + b1w, b2x + b2w) - max(b1x, b2x));
    y_overlap = max(0, min(b1y + b1h, b2y + b2h) - max(b1y, b2y));
    max_area = max(area(box1), area(box2))
    return (x_overlap * y_overlap) / float(max_area)



# Read image
img = cv2.imread("images/puzzle.jpg")
img = imutils.resize(img, width=600)
kernel = np.ones((3,3), np.uint8)

img = cv2.erode(img, kernel, iterations=1)
edges = cv2.Canny(img, 100, 200)

im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
boxes = []
for cnt in contours:
    boxes.append(cv2.boundingRect(cnt))

biggest_box = max(boxes, key=area)
biggest_area = area(biggest_box)
filtered_boxes = [box for box in boxes if area(box) > biggest_area * 0.3]
filtered_boxes = sorted(filtered_boxes, key=area, reverse=True)
not_overlapping = []
# merge Boxes
for box1 in filtered_boxes:
    overlap = False
    for box2 in not_overlapping:
        if calculate_overlap(box1, box2) > 0.3:
            overlap = True
    if not overlap:
        not_overlapping.append(box1)

# Draw boxes
# for x,y,w,h in not_overlapping:
#     cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
isolatePeice(img, not_overlapping[0])



# # cv2.imshow('contours',piece1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
