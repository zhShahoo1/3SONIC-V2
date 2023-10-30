import os
import numpy as np

def dicom_write_slice(arr, dicom_file, idx, filename, e_r):
    # Flip the array vertically
    arr = np.flip(arr, axis=0)
    
    # Convert array to uint16 format (assuming arr is in the range [0, 1])
    arr = np.uint16(65535 * arr)  # 65535 is the maximum value for uint16
    
    # Update the DICOM header with the array properties
    dicom_file.Rows = arr.shape[0]
    dicom_file.Columns = arr.shape[1]
    
    # Convert the array to bytes and assign it to PixelData
    dicom_file.PixelData = arr.tobytes()
    
    # Convert idx to an integer before using it for multiplication
    idx = int(idx)  # Convert idx to an integer
 
    image_position = [0, 0, e_r * idx]
    dicom_file.ImagePositionPatient = image_position

    # Save the DICOM slice
    result = 1
    while result is not None:
        try:
            result = dicom_file.save_as(os.path.join(filename, f'slice{idx}.dcm'))
        except:
            pass
