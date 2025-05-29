# CAPTCHA Symbol Classification with YOLOv8

This project presents a scalable, deep-learning-based solution to recognize CAPTCHA characters using YOLOv8, with full preprocessing, segmentation, training, and deployment workflows. Developed as part of the **Scalable Computing** module at Trinity College Dublin, the system achieves high classification accuracy across stylized and distorted fonts, and was successfully deployed to a **Raspberry Pi** using ONNX for real-world inference.

---

## 🧠 Project Overview

- **Model**: YOLOv8 pretrained classifier (`yolov8n-cls.pt`) fine-tuned on synthetic CAPTCHA images
- **Architecture**: Custom training with grayscale/morphological preprocessing and MSER-based segmentation
- **Deployment**: Model exported to ONNX and deployed on Raspberry Pi (via remote access under VPN)
- **Result**: Achieved ~95.6% validation accuracy on diverse CAPTCHA fonts with no overfitting


