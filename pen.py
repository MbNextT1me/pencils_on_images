import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as scnd
from skimage.filters import threshold_triangle
from skimage.measure import label, regionprops


def to_bin(image, l_min, l_max):
    B = image.copy()
    B[B <= l_min] = 0
    B[B >= l_max] = 0
    B[B > 0] = 1
    return B


def circularity(region, label = 1):
    return (region.perimeter ** 2) / region.area


def toGray(img):
    return (0.2989 * img[:,:,0] + 0.587 * img[:,:,1] + 0.114 * img[:,:,2]).astype("uint8")


if __name__ == "__main__":
    pencils = 0

    for i in range(1,13):
        print(f"Scaning image number: {i}")
        img = plt.imread("images/img ("+str(i)+").jpg")
        gray_img = toGray(img)
        thr_img = threshold_triangle(gray_img)
        br = to_bin(gray_img, 0, thr_img)
        br = scnd.binary_dilation(br, iterations = 1)
        lab = label(br)
        areas = []
    
        for r in regionprops(lab):
            areas.append(r.area)
        
        for r in regionprops(lab):
            if r.area < np.mean(areas):
                lab[lab == r.label] = 0
            bbox = r.bbox
            if bbox[0] == 0 or bbox[1] == 0:
                lab[lab == r.label] = 0
            
        lab[lab > 0] = 1
        lab = label(lab)
    
        c = 0 
        pencil = 0 

        for reg in regionprops(lab):
            c = c + 1
            if (((circularity(reg, c) > 100) and (300000 < reg.area < 450000))):
                pencil += 1

        pencils = pencils + pencil

        print(f"Amount of pencils on image number {i}: {pencil}\n")

    print(f"Amount of pencils in all images:{pencils}")
