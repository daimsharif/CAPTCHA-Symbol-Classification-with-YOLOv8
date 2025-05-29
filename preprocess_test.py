import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
import time

def overlap(box1, box2, threshold=0.3):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    
    xx1 = max(x1, x2)
    yy1 = max(y1, y2)
    xx2 = min(x1 + w1, x2 + w2)
    yy2 = min(y1 + h1, y2 + h2)
    
    if xx2 - xx1 > 0 and yy2 - yy1 > 0:  # If there is an intersection
        inter_area = (xx2 - xx1) * (yy2 - yy1)
        # Calculate the area of both boxes
        box1_area = w1 * h1
        box2_area = w2 * h2
        # Calculate the overlap ratio
        overlap_ratio = inter_area / float(box1_area + box2_area - inter_area)
        return overlap_ratio > threshold
    return False

def pad_character(character, target_size=(100, 100)):
    h, w = character.shape
    target_h, target_w = target_size

    # Calculate padding sizes
    pad_top = (target_h - h) // 2
    pad_bottom = target_h - h - pad_top
    pad_left = (target_w - w) // 2
    pad_right = target_w - w - pad_left

    # Pad the character
    padded_character = np.pad(character, ((pad_top, pad_bottom), (pad_left, pad_right)), mode='constant', constant_values=255)  # Using 255 for white padding
    return padded_character

def calcMser(file,segmented_dir,rst):

    mser = cv2.MSER_create()
    mser.setDelta(1)
    mser.setMaxArea(1500)
    mser.setMinDiversity(0.1) 
    regions, _ = mser.detectRegions(rst)
    min_area = 200  # Adjust this value based on your images
    bounding_boxes = []
    # min_area = 100

    for region in regions:
        x, y, w, h = cv2.boundingRect(region)
        area = w * h
        if area > min_area:
            bounding_boxes.append((x, y, w, h))

    non_overlapping_boxes = []
    for i in range(len(bounding_boxes)):
        add_box = True
        for j in range(len(non_overlapping_boxes)):
            if overlap(bounding_boxes[i], non_overlapping_boxes[j]):
                add_box = False
                break
        if add_box:
            non_overlapping_boxes.append(bounding_boxes[i])
    
    non_overlapping_boxes.sort(key=lambda box: box[0])  # box[0] is the x-coordinate


    for i, (x, y, w, h) in enumerate(non_overlapping_boxes):
        character = rst[y:y + h, x:x + w]
        if (character.shape[0] == 1) or (character.shape[1] == 1):
            continue
        background = pad_character(character)
        cv2.imwrite(os.path.join(segmented_dir, f'{file[:-4]}_char_{i}.png'), background)

            

def main():
    parser = argparse.ArgumentParser(description='Process CAPTCHA images.')
    parser.add_argument('--image_dir', type=str, required=True, help='Directory containing the images')
    parser.add_argument('--output_dir', type=str, required=True, help='Base directory to save segmented images')
    parser.add_argument('--log_file', type=str, default='execution_time_log.txt', help='Path to log execution time')
    args = parser.parse_args()

    image_dir = args.image_dir
    base_save_path = args.output_dir
    log_path=args.log_file
    start_time = time.time()
        
    image_files = os.listdir(image_dir)
    os.makedirs(base_save_path, exist_ok=True)

    for idx,file in enumerate(image_files):
        # print(file)

        image_path = os.path.join(image_dir, file)

        image = cv2.imread(image_path)
        
        if image is None:
            print(f"Failed to load image: {image_path}")
            continue
        
        segmented_dir = os.path.join(base_save_path, f'{file}')
        os.makedirs(segmented_dir, exist_ok=True)

        #HERE
        gray_image= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
        bw_img=cv2.dilate(gray_image, kernel, iterations=1)
        filtered_img = cv2.GaussianBlur(bw_img, (5, 5), 0)
        _, clean = cv2.threshold(filtered_img, 0, 255, cv2.THRESH_BINARY+ cv2.THRESH_OTSU )

        rst=clean
        
        resized_image = cv2.resize(rst, (100, 100))

        calcMser(file,segmented_dir,resized_image)
        
    end_time = time.time()

    elapsed_time = end_time - start_time

    # Log the execution time to a file
    with open(log_path, 'w') as log_file:
        log_file.write(f'Execution time: {elapsed_time:.4f} seconds\n')
       
                
if __name__ == '__main__':
    main()
    
    


