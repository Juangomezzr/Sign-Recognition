import argparse
import os
from pathlib import Path
import cv2
import numpy as np
import detectors.detector_mser 

# Jugar con el filtrado de imagenes
delta = 1 # Mantener
min_area = 5000
max_area = 200000
max_variation=0.01
top_ratio = 9.0 # Mantener
bottom_ratio = 0.2 # Mantener
resize_percentage = 0.05
alto = 50
ancho = 100
azul_bajos = np.array([90, 60, 40], dtype=np.uint8) # Mantener
azul_altos = np.array([150, 255, 255], dtype=np.uint8) # Mantener
mascara_ideal = np.ones((alto, ancho), dtype=np.float32)
umbral_score = 0.55
umbral_iou = 0.5
interpolation = cv2.INTER_NEAREST


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Trains and executes a given detector over a set of testing images"
    )
    parser.add_argument(
        "--detector", type=str, nargs="?", default="", help="Detector string name"
    )
    parser.add_argument(
        "--train_path", default="train_detection", help="Select the training data dir"
    )
    parser.add_argument(
        "--test_path", default="test_detection", help="Select the testing data dir"
    )
    args = parser.parse_args()

    # Paso 1: preparar rutas y salida.
    os.makedirs("resultado_imgs", exist_ok=True)
    test_path = Path(args.test_path)
    
    match args.detector:
        case "mser":
            detectors.detector_mser.detectar_mser(test_path)
        case _ : 
            detectors.detector_mser.detectar_mser(test_path)
