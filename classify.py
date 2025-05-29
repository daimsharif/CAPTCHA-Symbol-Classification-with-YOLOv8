import os
import pandas as pd
from tqdm import tqdm
from ultralytics import YOLO
import argparse

# import torch
# import cv2
def main():
    parser = argparse.ArgumentParser(description='Run YOLO inference on segmented images and save results to a CSV file.')
    parser.add_argument('--model_path', type=str, required=True, help='Path to the YOLO model weights file')
    parser.add_argument('--input_dir', type=str, required=True, help='Path to the directory containing segmented test images')
    parser.add_argument('--output_csv', type=str, required=True, help='Path to save the output CSV file')

    args = parser.parse_args()

    model = YOLO(args.model_path)

    # Define your class name dictionary
    class_dict = {
        0: '%', 1: '+', 2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6',
        8: '7', 9: '8', 10: '9', 11: 'B', 12: 'C', 13: 'F', 14: 'M',
        15: 'P', 16: 'Q', 17: 'R', 18: 'T', 19: 'U', 20: 'V', 21: 'Y',
        22: 'Z', 23: 'a', 24: '}', 25: ']',
        26: 'd', 27: '-', 28: 'e', 29: 'g', 30: 'h', 31: '#',
        32: 'j', 33: 'k', 34: 'n', 35: 'o', 36: '{',
        37: '[', 38: '|', 39: 's', 40: 'w', 41: 'x'
    }

    csvFile=[]
    parent_folder_path = args.input_dir
    parent_folder=os.listdir(parent_folder_path)

    for subfolder in tqdm(parent_folder):
        print(subfolder)
        subfolder_path = os.path.join(parent_folder_path, subfolder)
        captcha="" 

    
        for filename in os.listdir(subfolder_path):
            image_path = os.path.join(subfolder_path, filename)
            # Run inference
            results = model(image_path)
            captcha=captcha+ class_dict[results[0].probs.top1]

        csvFile.append((subfolder,captcha))
        # print(f'\n\n\nImage: {subfolder}, Predicted captcha: {captcha}\n\n\n\n')

    df = pd.DataFrame(csvFile)
    df.to_csv(args.output_csv, columns=None,index=False)

if __name__ == '__main__':
    main()