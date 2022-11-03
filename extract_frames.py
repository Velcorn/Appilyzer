import cv2
import numpy as np


def Vid2Frames(path):
    cap = cv2.VideoCapture(path)
    if (cap.isOpened() == False):
        print("Error opening video file")

    count=0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            train_name = './test/' + 'test' + str(count).zfill(12) + '.jpg'
            print('Creating...' + str(count))
            cv2.imwrite(train_name, frame)
            count += 1

def cleanText(chunk):
    frame_ann = {}
    frameID,_,_,_,metadata = np.asarray(chunk.split("\n"))
    iso, shutter, fnum,_,_,_, focal_len,latitude,longitude, altitude = np.asarray(metadata.split("] ["))
    latitude = latitude.split('],[')[-1].split(' ')[-1]
    _,relalt,_,absalt = altitude.split(']')[0].split(' ')
    iso = iso.split(': ')[-1]
    longitude = longitude.split(': ')[-1]
    focal_len = focal_len.split(': ')[-1]
    fnum = fnum.split(': ')[-1]

    frame_ann[frameID]={}
    frame_ann[frameID]['latitide'] = float(latitude)
    frame_ann[frameID]['rel_alt'] = float(relalt)
    frame_ann[frameID]['abs_alt'] = float(absalt)
    frame_ann[frameID]['longitude'] = float(longitude)
    frame_ann[frameID]['iso'] = int(iso)
    frame_ann[frameID]['focal_len'] = int(focal_len)
    frame_ann[frameID]['fnum'] = int(fnum)
    return frame_ann

def loadMetadata(path):
    metadata_dict = {}
    file = open(path, "r").read()
    chunks = np.asarray(file.split("\n\n"))
    for chunk in chunks:
        try:
            ann = cleanText(chunk)
            metadata_dict.update(ann)
        except:
            print("smt wrong with chunk")
            print(chunk)
    return metadata_dict

def calc_displacement(metadata):
#rauscutten wenn sich die höhe länger nicht verändert

if __name__ == '__main__':
    filename = "Videos Test/DJI_0068.MP4"
    metadata = "Videos Test/DJI_0068.SRT"
    metadata_dict = loadMetadata(metadata)
    #Vid2Frames(filename)
    print("hi")