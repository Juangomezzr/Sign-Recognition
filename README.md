# Práctica 1 - Datos de Alumnos

Proyecto de detección y evaluación de paneles azules en imágenes.

## Rama: `multi-detectors`

Esta rama introduce una arquitectura modular preparada para soportar múltiples detectores.

## Detectores disponibles

| Detector | Descripción | Archivo |
|----------|-------------|---------|
| `mser` | Detector MSER original | `detectors/detector_mser.py` |
| `c_d` | Color + Distribución espacial (connectedComponents) | `detectors/detector_color_distribucion.py` |

## Resultados

### IoU > 0.5

![IoU Greater 0.5](img/iou_greater_0_5.png)

### IoU > 0.7

![IoU Greater 0.7](img/iou_greater_0_7.png)

## Estructura del proyecto

```
├── main.py                    # Punto de entrada, selecciona el detector
├── evaluar_resultados.py      # Evaluación de resultados (IoU)
├── gt.py                     # Ground truth utilities
├── detectors/
│   ├── detector_mser.py       # Detector MSER
│   └── detector_color_distribucion.py  # Detector por color y distribución espacial
├── img/                      # Imágenes de resultados y gráficas
├── resultado_imgs/           # Imágenes procesadas con detecciones
├── train_detection/          # Datos de entrenamiento
└── test_detection/           # Datos de test
```

## Uso

```bash
# Ejecutar detector MSER (por defecto)
python main.py --detector mser

# Ejecutar detector por color y distribución espacial
python main.py --detector c_d
```

### Opciones

| Argumento | Descripción | Valor por defecto |
|-----------|-------------|-------------------|
| `--detector` | Nombre del detector a usar | `mser` |
| `--train_path` | Directorio de entrenamiento | `train_detection` |
| `--test_path` | Directorio de test | `test_detection` |

---

## Pipeline de detección (MSER)

El detector en `detectors/detector_mser.py` implementa un pipeline de 7 pasos:

1. **Preprocesamiento**:
   - Conversión a escala de grises
   - Desenfoque Gaussiano (kernel 3x3)
   - Ecualización CLAHE (clipLimit=0.5, tileGridSize=10x10)

2. **Detección de regiones MSER**:
   - delta=1, min_area=5000, max_area=200000, max_variation=0.01

3. **Filtrado geométrico**:
   - Eliminación por relación de aspecto (0.2 < ratio < 9.0)

4. **Agrandado de bounding boxes**:
   - Expansión del 5% manteniendo el centro

5. **Filtrado por color (HSV)**:
   - Rango azul: [90, 50, 40] - [150, 255, 255]
   - Score de correlación con máscara ideal (100x50)
   - Umbral de score: 0.6

6. **Non-Maximum Suppression (NMS)**:
   - Eliminación de detecciones solapadas (IoU > 0.5)
   - Ordenación por score descendente

7. **Salida**:
   - `resultado.txt`: `<nombre>;<x1>;<y1>;<x2>;<y2>;<tipo>;<score>`
   - `resultado_imgs/`: Imágenes con rectángulos verdes y score

### Parámetros MSER

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `delta` | 1 | Variación máxima en MSER |
| `min_area` | 5000 | Área mínima de región |
| `max_area` | 200000 | Área máxima de región |
| `max_variation` | 0.01 | Variación máxima permitida |
| `bottom_ratio` | 0.2 | Límite inferior de relación de aspecto |
| `top_ratio` | 9.0 | Límite superior de relación de aspecto |
| `resize_percentage` | 0.05 | Expansión del bounding box (5%) |
| `umbral_score` | 0.6 | Umbral mínimo de score de color |
| `umbral_iou` | 0.5 | Umbral máximo de solapamiento (NMS) |

---

## Pipeline de detección (c_d - Color y Distribución Espacial)

El detector en `detectors/detector_color_distribucion.py` usa detección de color azul por HSV y análisis de distribución espacial con `connectedComponents`.

1. **Detección de píxeles azules (HSV)**:
   - Rango azul: [75, 40, 40] - [180, 255, 255]
   - Conversión BGR → HSV → máscara binaria

2. **Análisis de distribución espacial**:
   - `cv2.connectedComponentsWithStats` para etiquetar blobs
   - Extracción de área, bounding box y centroide de cada blob

3. **Filtrado de candidatos**:
   - Por área: min_area_pixels=500, max_area_pixels=200000
   - Por relación de aspecto: 0.15 < ratio < 10.0

4. **Filtrado por color**:
   - Score de correlación con máscara ideal
   - Umbral de score: 0.3

5. **Agrandado de bounding boxes**:
   - Expansión del 10% manteniendo el centro

6. **Non-Maximum Suppression (NMS)**:
   - Eliminación de detecciones solapadas (IoU > 0.6)

7. **Salida**:
   - `resultado.txt`: `<nombre>;<x1>;<y1>;<x2>;<y2>;<tipo>;<score>`
   - `resultado_imgs/cd_*.png`: Imágenes con detecciones
   - `resultado_imgs/cd_mask_*.png`: Máscara de azules (debug)

### Parámetros c_d

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `azul_bajos` | [75, 40, 40] | Límite inferior HSV |
| `azul_altos` | [180, 255, 255] | Límite superior HSV |
| `min_area_pixels` | 500 | Área mínima de blob |
| `max_area_pixels` | 200000 | Área máxima de blob |
| `bottom_ratio` | 0.15 | Límite inferior de relación de aspecto |
| `top_ratio` | 10.0 | Límite superior de relación de aspecto |
| `resize_percentage` | 0.10 | Expansión del bounding box (10%) |
| `umbral_score` | 0.3 | Umbral mínimo de score de color |
| `umbral_iou` | 0.6 | Umbral máximo de solapamiento (NMS) |

---

## Archivos principales

- `main.py` - Script principal que selecciona y ejecuta el detector
- `detectors/detector_mser.py` - Detector MSER
- `detectors/detector_color_distribucion.py` - Detector por color y distribución
- `evaluar_resultados.py` - Evaluación de resultados (cálculo de IoU)
