import argparse
import os
from pathlib import Path

import cv2
import numpy as np


def crear_detector_mser():
    return cv2.MSER_create(
        delta=0,
        min_area=1000,
        min_diversity = 0.9,
        max_variation=0.1,
    )


def cargar_imagen(image_path):
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen: {image_path}")
    return image


# Equializacion por tiles
def preprocesar_imagen(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8, 8))
    equalized_image = clahe.apply(gray_image)
    return gray_image, equalized_image

# Filatrdoo de relacion aspecto
def obtener_candidatos(detector, equalized_image):
    _, bboxes = detector.detectRegions(equalized_image)

    candidatos = []
    for x, y, w, h in bboxes:
        ratio = w / float(h)
        if 0.2 < ratio < 4.0:
            candidatos.append((x, y, w, h))

    return bboxes, candidatos

# Configuracion filtro de color
def crear_configuracion_color():
    alto = 40
    ancho = 80
    azul_bajos = np.array([90, 200, 40], dtype=np.uint8)
    azul_altos = np.array([150, 255, 255], dtype=np.uint8)
    mascara_ideal = np.ones((alto, ancho), dtype=np.float32)
    umbral_score = 0.60

    return {
        "alto": alto,
        "ancho": ancho,
        "azul_bajos": azul_bajos,
        "azul_altos": azul_altos,
        "mascara_ideal": mascara_ideal,
        "umbral_score": umbral_score,
    }

# <------ Filtro de color -------->
def calcular_score_azul(recorte, config_color):
    if recorte.shape[0] == 0 or recorte.shape[1] == 0:
        return None

    recorte_resized = cv2.resize(
        recorte,
        (config_color["ancho"], config_color["alto"]),
    )

    hsv_image = cv2.cvtColor(recorte_resized, cv2.COLOR_BGR2HSV)

    #Mascara binaria de los azules si el pixel esta fuera del rango es 0
    mascara_azul = cv2.inRange(
        hsv_image,
        config_color["azul_bajos"],
        config_color["azul_altos"],
    )
    # Pasamos a 0.0 - 1.0 para calcular mas facilmente el calculo posterior
    mascara_normalizada = mascara_azul.astype(np.float32) / 255.0
    correlacion = np.sum(mascara_normalizada * config_color["mascara_ideal"])
    return correlacion / float(config_color["ancho"] * config_color["alto"])


def filtrar_detecciones_por_color(image, candidatos, config_color):
    detecciones_finales = []

    for x, y, w, h in candidatos:
        recorte = image[y : y + h, x : x + w]
        score = calcular_score_azul(recorte, config_color)

        if score is None:
            continue

        if score > config_color["umbral_score"]:
            detecciones_finales.append((x, y, x + w, y + h, score))

    return detecciones_finales


def dibujar_candidatos(image, candidatos):
    image_copy = image.copy()
    for x, y, w, h in candidatos:
        cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image_copy


def dibujar_detecciones_finales(image, detecciones_finales):
    image_copy = image.copy()

    for x1, y1, x2, y2, score in detecciones_finales:
        cv2.rectangle(image_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            image_copy,
            f"{score:.2f}",
            (x1, max(20, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 255),
            1,
            cv2.LINE_AA,
        )

    return image_copy


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
    train_path = Path(args.train_path)

    # Paso 2: crear detector y cargar imagen.
    mser = crear_detector_mser()
    img_path = train_path / "00001.png"
    img = cargar_imagen(img_path)

    # Paso 3: preprocesar para MSER.
    gray, eq = preprocesar_imagen(img)
    cv2.imshow("img", gray)
    cv2.waitKey(0)
    cv2.imshow("img", eq)
    cv2.waitKey(0)

    # Paso 4: detectar regiones y filtrar candidatos geometricos.
    bboxes, candidatos = obtener_candidatos(mser, eq)
    print("len boxes", len(bboxes))
    print("len candidatos", len(candidatos))

    img_viz = dibujar_candidatos(img, candidatos)
    cv2.imshow("img", img_viz)
    cv2.waitKey(0)

    # Paso 5: preparar la configuracion del filtro HSV y la mascara ideal.
    config_color = crear_configuracion_color()

    # Paso 6: calcular score por correlacion y quedarnos con los validos.
    detecciones_finales = filtrar_detecciones_por_color(
        img,
        candidatos,
        config_color,
    )
    print("len detecciones finales", len(detecciones_finales))

    # Paso 7: visualizar resultado final.
    img_blue = dibujar_detecciones_finales(img, detecciones_finales)
    cv2.imshow("img", img_blue)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
