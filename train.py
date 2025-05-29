from ultralytics import YOLO
import argparse

def main():
    parser = argparse.ArgumentParser(description='Train a YOLO model.')
    parser.add_argument('--model_path', type=str, required=True, help='Path to the YOLO model weights file')
    parser.add_argument('--data', type=str, required=True, help='Path to the training data directory')
    parser.add_argument('--epochs', type=int, default=10, help='Number of epochs for training (default is 10)')
    parser.add_argument('--imgsz', type=int, default=640, help='Image size for training (default is 640)')
    parser.add_argument('--project', type=str, required=True, help='Project directory to save the model results')

    args = parser.parse_args()

    # Load the YOLO model
    model = YOLO(args.model_path).to('cuda')

    # Train the model
    results = model.train(
        data=args.data, 
        epochs=args.epochs, 
        imgsz=args.imgsz,
        project=args.project
    )

    print("Training completed.")

if __name__ == '__main__':
    main()