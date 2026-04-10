# Práctica 1 - Datos de Alumnos

Proyecto de detección y evaluación de paneles azules en imágenes.

## Rama: `multi-detectors`

Esta rama introduce una arquitectura modular preparada para soportar múltiples detectores.

## Resultados

### IoU > 0.5

![IoU Greater 0.5](img/iou_greater_0_5.png)

### IoU > 0.7

![IoU Greater 0.7](img/iou_greater_0_7.png)

## Estructura del proyecto

```
├── main.py                    # Punto de entrada, selecciona el detector
├── evaluar_resultados.py      # Evaluación de resultados (IoU)
├── gt.py                      # Ground truth utilities
├── detectors/
│   └── detector_mser.py       # Implementación del detector MSER
├── img/                       # Imágenes de resultados y gráficas
├── resultado_imgs/            # Imágenes procesadas con detecciones
├── train_detection/           # Datos de entrenamiento
└── test_detection/            # Datos de test
```

## Archivos principales

- `main.py` - Script principal que selecciona y ejecuta el detector
- `detectors/detector_mser.py` - Implementación completa del detector MSER
- `evaluar_resultados.py` - Evaluación de resultados (cálculo de IoU)

## Uso

```bash
# Ejecutar el detector MSER por defecto
python main.py --detector mser

# Especificar ruta de test personalizada
python main.py --detector mser --test_path test_detection

# Especificar ruta de train personalizada
python main.py --detector mser --train_path train_detection --test_path test_detection
```

### Opciones

| Argumento | Descripción | Valor por defecto |
|-----------|-------------|-------------------|
| `--detector` | Nombre del detector a usar | `""` (usa MSER) |
| `--train_path` | Directorio de entrenamiento | `train_detection` |
| `--test_path` | Directorio de test | `test_detection` |

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
   - Rango azul: [90, 60, 40] - [150, 255, 255]
   - Score de correlación con máscara ideal (100x50)
   - Umbral de score: 0.55

6. **Non-Maximum Suppression (NMS)**: 
   - Eliminación de detecciones solapadas (IoU > 0.5)
   - Ordenación por score descendente

7. **Salida**: 
   - `resultado.txt`: `<nombre>;<x1>;<y1>;<x2>;<y2>;<tipo>;<score>`
   - `resultado_imgs/`: Imágenes con rectángulos verdes y score

## Parámetros del detector

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `delta` | 1 | Variación máxima en MSER |
| `min_area` | 5000 | Área mínima de región |
| `max_area` | 200000 | Área máxima de región |
| `max_variation` | 0.01 | Variación máxima permitida |
| `bottom_ratio` | 0.2 | Límite inferior de relación de aspecto |
| `top_ratio` | 9.0 | Límite superior de relación de aspecto |
| `resize_percentage` | 0.05 | Expansión del bounding box (5%) |
| `umbral_score` | 0.55 | Umbral mínimo de score de color |
| `umbral_iou` | 0.5 | Umbral máximo de solapamiento (NMS) |

