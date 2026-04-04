import argparse
import cv2
import os
from pathlib import Path
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Trains and executes a given detector over a set of testing images')
    parser.add_argument(
        '--detector', type=str, nargs="?", default="", help='Detector string name')
    parser.add_argument(
        '--train_path', default="", help='Select the training data dir')
    parser.add_argument(
        '--test_path', default="", help='Select the testing data dir')

    args = parser.parse_args()

    # Load training data

    # Create the detector

    # Load testing data

    # Evaluate detections

    # Ensure output folder exists


# Realizar script con una sola imagen de prueba posteriormente implementar las pruebas para todas las imagenes
    os.makedirs("resultado_imgs", exist_ok=True)

    test_path = Path("test_detection")
    train_path = Path("train_detection")
   




