import sys
import os
import cv2
import numpy as np

"""
<ROOT>
|---original--- 
|             | <contains jpg format image>
|---<method 1>---
.               | <contains same name jpg format image, name is suffixed with _output>
.
.
|---<method n>
"""
FOLDER_ROOT = "."
ORIGINAL_FOLDER = "original"
METHODS_TO_COMPARE = ["hc_trap_split", "ga_elitist"]

def calc_contrast_michelson(frame):
    # print(frame)
    Y = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)[:,:,0]

    # compute min and max of Y
    min = float(np.min(Y))
    max = float(np.max(Y))
    # print(min, max, max-min, max+min, (max-min)/(max+min))
    # compute contrast
    contrast = (max-min)/(max+min)
    return contrast

def calc_psnr(original_frame, modified_frame):
    return cv2.PSNR(original_frame, modified_frame)

if __name__ == '__main__':
    # we are assuming corresponding to original frame output frame is present
    for filename in os.listdir(os.path.join(FOLDER_ROOT, ORIGINAL_FOLDER)):
        basename, ext = os.path.splitext(filename)
        if not ext in [".jpg", ".png"]:
            continue

        original_frame = cv2.imread(os.path.join(os.path.join(FOLDER_ROOT, ORIGINAL_FOLDER), filename))
        original_contrast = calc_contrast_michelson(original_frame)

        data_list = [filename, original_contrast]
        for method in METHODS_TO_COMPARE:
            # get the method corresponding out image
            out_frame = cv2.imread(os.path.join(os.path.join(FOLDER_ROOT, method), basename + "_output.jpg"))
            # print(os.path.join(os.path.join(FOLDER_ROOT, method), basename + "_output.jpg"))
            psnr = calc_psnr(original_frame=original_frame, modified_frame=out_frame)
            contrast = calc_contrast_michelson(out_frame)
            data_list.append(contrast)
            data_list.append(psnr)
        # print(data_list)
        # print for latex tabular contrast & hc mod contrast & ga mod contrast & hc mod psnr & ga mod psnr
        print(data_list[0], " & ".join(["{0:.3f}".format(data) for data in [data_list[1],data_list[2],data_list[4],data_list[3],data_list[5]]]))
