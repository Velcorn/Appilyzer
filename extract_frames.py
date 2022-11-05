import os
import cv2
import numpy as np
from glob import glob
from geopy.distance import distance

path = "Videos Train"


def video2frames(p: str, md: dict):
    # Create folder
    folder = f'{p.split("/")[0].replace(".MP4", "")}'
    os.makedirs(folder, exist_ok=True)

    # Open video
    cap = cv2.VideoCapture(p)
    if not cap.isOpened():
        print("Error opening video file")

    # Threshold and previous lat, lon, alt
    threshold = 0.5
    prev = None
    # Tiling and overlap
    tiling = True
    overlap = .25
    # Counter to keep track of frame number
    count = 1
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            # Calculate 3D displacement from current and previously saved frame
            # Save frame when displacement greater than threshold
            try:
                lat, lon, alt = md[str(count)]['latitude'], md[str(count)]['longitude'], md[str(count)]['abs_alt']
            except KeyError:
                continue
            if prev is None:
                dist3d = threshold + 1
                prev = (lat, lon, alt)
            else:
                dist2d = distance((lat, lon), (prev[:2])).m
                dist3d = np.sqrt((alt - prev[2]) ** 2 + dist2d ** 2)
            if dist3d > threshold:
                print(f"Extracting frame {count}...")
                prev = (lat, lon, alt)
                if tiling:
                    # Split image into 4x4 tiles with overlap
                    # Apply zero padding around the image according to the overlap
                    h, w, _ = frame.shape
                    tile_h = int(h / 4)
                    tile_w = int(w / 4)
                    overlap_h = int(tile_h * overlap)
                    overlap_w = int(tile_w * overlap)
                    frame = np.pad(frame, ((overlap_h, overlap_h), (overlap_w, overlap_w), (0, 0)), 'constant')
                    for i in range(4):
                        for j in range(4):
                            tile = frame[i * tile_h:i * tile_h + tile_h + 2 * overlap_h,
                                         j * tile_w:j * tile_w + tile_w + 2 * overlap_w, :]
                            cv2.imwrite(f'{folder}/{str(count).zfill(6)}_{i}{j}.png', tile)
                else:
                    name = f'{folder}/{str(count).zfill(6)}.jpg'
                    cv2.imwrite(name, frame)
            count += 1
        else:
            cap.release()


def clean_text(chunk: str):
    frame_ann = {}
    frameID, _, _, _, metadata = np.asarray(chunk.split('\n'))
    iso, shutter, fnum, _, _, _, focal_len, latitude, longitude, altitude = np.asarray(metadata.split('] ['))
    latitude = latitude.split('],[')[-1].split(' ')[-1]
    _, relalt, _, absalt = altitude.split(']')[0].split(' ')
    iso = iso.split(': ')[-1]
    longitude = longitude.split(': ')[-1]
    focal_len = focal_len.split(': ')[-1]
    fnum = fnum.split(': ')[-1]

    frame_ann[frameID] = {}
    frame_ann[frameID]['latitude'] = float(latitude)
    frame_ann[frameID]['longitude'] = float(longitude)
    frame_ann[frameID]['rel_alt'] = float(relalt)
    frame_ann[frameID]['abs_alt'] = float(absalt)
    frame_ann[frameID]['iso'] = int(iso)
    frame_ann[frameID]['focal_len'] = int(focal_len)
    frame_ann[frameID]['fnum'] = int(fnum)
    return frame_ann


def load_metadata(p: str):
    metadata_dict = {}
    file = open(p, 'r').read()
    chunks = np.asarray(file.split('\n\n'))
    for chunk in chunks:
        try:
            ann = clean_text(chunk)
            metadata_dict.update(ann)
        except ValueError:
            pass
    return metadata_dict


def calc_displacement(md):
    # Rauscutten, wenn sich die Höhe länger nicht verändert
    pass


if __name__ == '__main__':
    filenames = glob(f'{path}/*.MP4')
    for f in filenames:
        print(f'Extracting frames from {f}')
        metadata = load_metadata(f.replace('.MP4', '.SRT'))
        video2frames(f, metadata)
