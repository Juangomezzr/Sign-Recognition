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


    os.makedirs("resultado_imgs", exist_ok=True)

    test_path = Path("test_detection")
    train_path = Path("train_detection")
   

    img = train_path / "00000.png"

    # Cargar img
    img = cv2.imread(img)

    # Escala de grises
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("vista",img)
    cv2.waitKey(0)

    # Equalizacion para aumentar contraste
    eq = cv2.equalizeHist(img)
    cv2.imshow("vista", eq)
    cv2.waitKey(0)

    cv2.destroyAllWindows()