import random

import cv2
from tqdm import tqdm
import shutil

#videos = ["DJI_0060", "DJI_0064", "DJI_0075", "DJI_0076", "DJI_0077", "DJI_0079"]
#
#for video in tqdm(videos):
#
#    capture = cv2.VideoCapture(f'S:/data/Appilyzer/Appilyzer/Videos_train/{video}.mp4')
#    frameNr = 0
#
#    while (True):
#
#        success, frame = capture.read()
#
#        if success:
#            cv2.imwrite(f'S:/data/Appilyzer/dataset/healthy_train/frame_{video}_{frameNr}.jpg', frame)
#
#        else:
#            break
#
#        frameNr = frameNr + 1
#
#    capture.release()
#
#
# ----------------------------
base_path  = "S:/data/Appilyzer/dataset/"
mypath = base_path + "unhealthy_train"
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

test_nbr = int(0.1 * len(onlyfiles))
print("Size test set: {}".format(test_nbr))

for i in range(test_nbr):
    index = random.randint(0, len(onlyfiles))
    filename = onlyfiles[index]
    #print("File Name: {}".format(onlyfiles[index]))
    #print("File Type: {}".format(type(onlyfiles[index])))
    shutil.move(base_path + f"unhealthy_train/{filename}", base_path + f"unhealthy_test/{filename}", copy_function=shutil.copy2)
    onlyfiles.remove(filename)
