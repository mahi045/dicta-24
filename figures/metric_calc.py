import sys
import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity

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
METHODS_TO_COMPARE = ["hc_trap_split", "ga_elitist", "agcwd", "dual"]

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

def mod_HE(original_frame):
    dst = cv2.equalizeHist(cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY))
    dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    return dst

def calc_SSIM(original_frame, modified_frame):
    before_gray = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(modified_frame, cv2.COLOR_BGR2GRAY)
    (score, diff) = structural_similarity(before_gray, after_gray, full=True)
    return score

if __name__ == '__main__':
    # we are assuming corresponding to original frame output frame is present
    for filename in os.listdir(os.path.join(FOLDER_ROOT, ORIGINAL_FOLDER)):
        basename, ext = os.path.splitext(filename)
        if not ext in [".jpg", ".png"]:
            continue

        original_frame = cv2.imread(os.path.join(os.path.join(FOLDER_ROOT, ORIGINAL_FOLDER), filename))
        # HE equalized frame
        he_frame = mod_HE(original_frame)
        original_contrast = calc_contrast_michelson(original_frame)
        he_contrast = calc_contrast_michelson(he_frame)
        he_psnr = calc_psnr(original_frame=original_frame, modified_frame=he_frame)
        he_ssim = calc_SSIM(original_frame=original_frame, modified_frame=he_frame)
        # save he image
        cv2.imwrite(os.path.join(os.path.join(FOLDER_ROOT, "he"), basename + "_output.jpg"), he_frame, [cv2.IMWRITE_JPEG_QUALITY, 100])

        data_list = [filename, original_contrast, he_contrast, he_psnr, he_ssim]
        for method in METHODS_TO_COMPARE:
            # get the method corresponding out image
            out_frame = cv2.imread(os.path.join(os.path.join(FOLDER_ROOT, method), basename + "_output.jpg"))
            
            # print(os.path.join(os.path.join(FOLDER_ROOT, method), basename + "_output.jpg"))
            psnr = calc_psnr(original_frame=original_frame, modified_frame=out_frame)
            contrast = calc_contrast_michelson(out_frame)
            ssim = calc_SSIM(original_frame=original_frame, modified_frame=out_frame)
            data_list.append(contrast)
            data_list.append(psnr)
            data_list.append(ssim)
        # print(data_list)
        # print for latex tabular contrast & hc mod contrast & ga mod contrast & hc mod psnr & ga mod psnr
        print(data_list[0], " & ".join(["{0:.3f}".format(data) for data in [data_list[1], data_list[2],data_list[4],data_list[6], data_list[3],data_list[5],data_list[7], data_list[8], data_list[9], data_list[10], data_list[11]]]))
        print(round(data_list[4], 2), "&", round(data_list[13], 2), "&", round(data_list[16], 2), "&", round(data_list[7], 2), "&", round(data_list[10], 2))