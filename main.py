import argparse
import os
from pathlib import Path
import cv2
import numpy as np
import detectors.detector_mser
import detectors.detector_color_distribucion


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Trains and executes a given detector over a set of testing images"
    )
    parser.add_argument(
        "--detector", type=str, nargs="?", default="mser", help="Detector string name"
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
        case "c_d":
            detectors.detector_color_distribucion.detectar_color_distribucion(test_path)
        case _:
            print("Detector no reconocido. Usando mser por defecto.")
            detectors.detector_mser.detectar_mser(test_path)
