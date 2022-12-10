import numpy as np
import cv2
from os import listdir
from os.path import isfile, join
import os
import json


def main():
    #print('test')
    current_dir = 'C:/data/Appilyzer/healthy_green_labeled'
    output_dir = 'C:/data/Appilyzer/healthy_green_labeled/dataset/'
    healthy_img_counter = 0
    healthy_img_test_counter = 0

    onlyfiles = [f.path for f in os.scandir(current_dir + '/') if f.is_file()]
    print(onlyfiles)
    img_names = []
    for file_dir in onlyfiles:
        file_name = os.path.splitext(os.path.basename(os.path.normpath(file_dir)))[0]
        if file_name not in img_names:
            img_names.append(file_name)
    for img_name in img_names:
        print(current_dir + '/' + img_name + '.jpg')
        cv_img = cv2.imread(current_dir + '/' + img_name + '.jpg')
        data = json.load(open(current_dir + '/' + img_name + '.json'))
        for entry in data['shapes']:
            label, bb = entry['label'], entry['points']
            print(bb)
            print("BB: {0} {1} {2} {3}".format(int(bb[0][1]), int(bb[1][1]), int(bb[0][0]), int(bb[1][0])))
            print("IMG shape: {0}".format(cv_img.shape))
            print(cv_img[int(bb[0][1]):int(bb[1][1]), int(bb[0][0]):int(bb[1][0])].shape)
            bb_img = None
            if label == 'healthy' and (healthy_img_counter < 500 or healthy_img_test_counter < 100):
                if bb[0][0] > bb[1][0]:
                    if bb[0][1] > bb[1][1]:
                        bb_img = cv_img[int(bb[1][1]):int(bb[0][1]), int(bb[1][0]):int(bb[0][0])]
                    else:
                        bb_img = cv_img[int(bb[0][1]):int(bb[1][1]), int(bb[1][0]):int(bb[0][0])]
                else:
                    if bb[0][1] > bb[1][1]:
                        bb_img = cv_img[int(bb[1][1]):int(bb[0][1]), int(bb[0][0]):int(bb[1][0])]
                    else:
                        bb_img = cv_img[int(bb[0][1]):int(bb[1][1]), int(bb[0][0]):int(bb[1][0])]
                if healthy_img_counter < 500:
                    cv2.imwrite(output_dir + 'healthy_train/img_{0}.jpg'.format(healthy_img_counter), bb_img)
                    healthy_img_counter += 1
                elif healthy_img_test_counter < 100:
                    cv2.imwrite(output_dir + 'healthy_test/img_{0}.jpg'.format(healthy_img_test_counter), bb_img)
                    healthy_img_test_counter += 1
            print("Label: {0}, BB: {1}".format(label, bb))


if __name__ == '__main__':
    main()
