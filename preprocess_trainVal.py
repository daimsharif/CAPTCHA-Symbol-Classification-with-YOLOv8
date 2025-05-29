import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import argparse


def main():
    parser = argparse.ArgumentParser(description='Process training images.')
    parser.add_argument('--train_dir', type=str, required=True, help='Directory containing the training images')
    parser.add_argument('--output_dir', type=str, required=True, help='Base directory to save segmented images')
    parser.add_argument('--log_file', type=str, default='execution_time_log.txt', help='Path to log execution time')

    args = parser.parse_args()
    train_dir = args.train_dir
    base_save_path = args.output_dir
    log_path=args.log_file
    
    start_time = time.time()

        
    char_files = os.listdir(train_dir)
    os.makedirs(base_save_path, exist_ok=True)
       
        
    for char in char_files:
        # print(char)
        char_dir=os.path.join(train_dir,char)
        image_files = os.listdir(char_dir)
        # print(image_files)
        for i,pic in enumerate(image_files):
            image_path = os.path.join(char_dir,pic)

            image = cv2.imread(image_path)
            
            segmented_dir = os.path.join(base_save_path, f'{char}')
            os.makedirs(segmented_dir, exist_ok=True)
            #HERE
            gray_image= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
            bw_img=cv2.dilate(gray_image, kernel, iterations=1)
            _, clean = cv2.threshold(bw_img, 0, 255, cv2.THRESH_BINARY+ cv2.THRESH_OTSU )
            
            background = np.ones((100, 100), dtype=np.uint8) * 255

            x_offset = 10  
            y_offset = 10  

            height, width = clean.shape
            if x_offset + width <= 100 and y_offset + height <= 100:
                # Paste the input image onto the background
                background[y_offset:y_offset + height, x_offset:x_offset + width] = clean
            else:
                print("Input image is too large to paste onto the background.")
            
            # cv2.imwrite(segmented_dir, f'{background}.png')
            filename = os.path.join(segmented_dir, f'{char}_{i}.png')  # Create a unique filename
            cv2.imwrite(filename, background)  # Save the image
            
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Log the execution time to a file
    with open(log_path, 'w') as log_file:
        log_file.write(f'Execution time: {elapsed_time:.4f} seconds\n')

            
     
                    
       
                
if __name__ == '__main__':
    main()
    
    


