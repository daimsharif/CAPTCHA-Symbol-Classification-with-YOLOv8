import os
import random
import shutil
import argparse

def main():

    parser = argparse.ArgumentParser(description='Move a specified number of images from training to validation directory.')
    parser.add_argument('--train_dir', type=str, required=True, help='Path to the training directory')
    parser.add_argument('--validation_dir', type=str, required=True, help='Path to the validation directory')
    parser.add_argument('--num_images', type=int, default=500, help='Number of images to move from each class (default is 500)')
    
    args = parser.parse_args()

    train_dir = args.train_dir
    validation_dir = args.validation_dir
    num_images_to_move = args.num_images
  

    # Number of images to move from each class
    num_images_to_move = 500

    # Ensure validation directory exists
    os.makedirs(validation_dir, exist_ok=True)

    # Loop over each class folder in the train directory
    for class_name in os.listdir(train_dir):
        class_train_folder = os.path.join(train_dir, class_name)
        
        # Ensure it is a directory
        if os.path.isdir(class_train_folder):
            # Create corresponding class folder in the validation directory
            class_validation_folder = os.path.join(validation_dir, class_name)
            os.makedirs(class_validation_folder, exist_ok=True)
            
            # Get list of all image files in the class folder
            images = os.listdir(class_train_folder)
            
            # Randomly select 500 images
            images_to_move = random.sample(images, num_images_to_move)
            
            # Move the selected images from train to validation
            for image in images_to_move:
                src_image_path = os.path.join(class_train_folder, image)
                dest_image_path = os.path.join(class_validation_folder, image)
                shutil.move(src_image_path, dest_image_path)

    print("500 images moved from each class folder to the validation folder.")

if __name__ == '__main__':
    main()