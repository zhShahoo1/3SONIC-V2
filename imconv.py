import os
import numpy as np
from PIL import Image
import pydicom
import pandas as pd
from dicomwritevolume import dicom_write_slice
from multiprocessing import Pool

def tiff_force_8bit(image, **kwargs):
    if image.format == 'TIFF' and image.mode == 'I;16':
        array = np.array(image)
        normalized = (array.astype(np.uint16) - array.min()) * 255.0 / (array.max() - array.min())
        image = Image.fromarray(normalized.astype(np.uint8))
    return image

# Modified the function to accept a tuple (file, processdir)
def process_file(args):
    file, processdir = args  # Unpack the tuple
    configurations = pd.read_csv(os.path.join(processdir, "config.txt"), header=None)
    y_res = float(configurations.iloc[:, 0][11].split(":")[1][:-1])
    x_res = float(configurations.iloc[:, 0][10].split(":")[1][:-1])
    e_r = float(configurations.iloc[:, 0][2].split(":")[1][:-1])

    dicom_file = pydicom.dcmread('dcmimage.dcm')
    dicom_file.PhotometricInterpretation = "MONOCHROME2"
    dicom_file.SamplesPerPixel = 1
    dicom_file.BitsStored = 16
    dicom_file.BitsAllocated = 16
    dicom_file.HighBit = 15
    dicom_file.PixelRepresentation = 0
    dicom_file.WindowCenter = 0
    dicom_file.WindowWidth = 1000
    dicom_file.SOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
    dicom_file.RescaleIntercept = -1024
    dicom_file.RescaleSlope = 1
    dicom_file.RescaleType = 'HU'
    dicom_file.SliceThickness = e_r
    dicom_file.ImagerPixelSpacing = [x_res, y_res]
    dicom_file.PixelSpacing = [x_res, y_res]

    try:
        tfile = np.load(os.path.join(processdir, file))
        dicom_write_slice(tfile, dicom_file, file.split(".")[0], os.path.join(processdir, "dicom_series"), e_r)
        tfile = np.flipud(tfile)
        im = Image.fromarray(tfile)
        im2 = tiff_force_8bit(im)
        os.rename(os.path.join(processdir, file), os.path.join(processdir, "raws", file))
        im2.convert('P').save(os.path.join(processdir, "frames", file.split(".")[0] + ".png"))
    except PermissionError:
        pass

if __name__ == "__main__":
    processdir = ""
    with open("recdir", 'r') as f:
        processdir = f.readlines()[0].split("\n")[0]
    print(processdir)

    if not os.path.exists(processdir + os.sep + "processed"):
        try:
            os.mkdir(processdir + os.sep + "frames")
            os.mkdir(processdir + os.sep + "raws")
            os.mkdir(processdir + os.sep + "dicom_series")
        except FileExistsError:
            pass

    all_files = [f for f in os.listdir(processdir) if f.endswith(".npy")]
    all_files.sort()

    total_files = len(all_files)
    start_index = total_files // 4
    end_index = 3 * total_files // 4

    # Package each file name together with the processdir into a tuple
    args_for_map = [(file, processdir) for file in all_files[start_index:end_index]]
    with Pool() as p:
        p.map(process_file, args_for_map)

    with open("scanning", "w") as fs:
        fs.write("0")