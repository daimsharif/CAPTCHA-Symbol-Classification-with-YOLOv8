from ultralytics import YOLO
import argparse

def main():
    parser = argparse.ArgumentParser(description='Export a YOLO model to a format.')
    parser.add_argument('--model_path', type=str, required=True, help='Path to the YOLO model weights file')
    args = parser.parse_args()

    model = YOLO(args.model_path)
    model.export(format='onnx', imgsz=640, simplify=True)


if __name__ == '__main__':
    main()