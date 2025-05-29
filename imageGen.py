from captcha.image import ImageCaptcha
import os
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate single character CAPTCHA images.')
    parser.add_argument('--font1', type=str, required=True, help='Path to the first font file')
    parser.add_argument('--font2', type=str, required=True, help='Path to the second font file')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save generated CAPTCHA images')
    parser.add_argument('--num_samples', type=int, default=2500, help='Number of samples per character (default is 2500)')
    parser.add_argument('--log_file', type=str, required=True, help='Path to the log file')
    args = parser.parse_args()
    
    

    characters = "123456789aBCdeFghjkMnoPQRsTUVwxYZ+%|#][{}-"

    # Create a main folder named "epoch(1)"
    os.makedirs(args.output_dir, exist_ok=True)

    symbol_folders = {
        '|': 'pipe',
        '#': 'hash',
        ']': 'close_square_bracket',
        '[': 'open_square_bracket',
        '{': 'open_curly_brace',
        '}': 'close_curly_brace',
        '-': 'dash'
    }


    def generate_captcha_for_characters(num_samples_per_character):
        # Start time
        start_time = time.time()
        
        with open(args.log_file, 'w') as log_file:
            log_file.write(f"Start time: {time.ctime(start_time)}\n")
            
            for character in characters:
                character_folder = os.path.join(args.output_dir, symbol_folders.get(character, character))
                os.makedirs(character_folder, exist_ok=True)

                for i in range(num_samples_per_character):
               
                    image_captcha = ImageCaptcha(width=80, height=80,fonts=[args.font1, args.font2])
                    captcha_image = image_captcha.generate_image(character)
                    filename = f"{symbol_folders.get(character, character)}_{i}.png"
                    captcha_image.save(os.path.join(character_folder, filename))

            # End time
            end_time = time.time()
            log_file.write(f"End time: {time.ctime(end_time)}\n")
            log_file.write(f"Total time taken: {end_time - start_time:.2f} seconds\n")

    generate_captcha_for_characters(num_samples_per_character=args.num_samples)

if __name__ == '__main__':
    main()