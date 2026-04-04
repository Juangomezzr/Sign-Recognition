┌────────────────────────────────────────────────────────┐
│             IMAGEN DE ENTRADA (Test/Train)             │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 1. PREPROCESAMIENTO MSER                               │
│  • Convertir la imagen a niveles de gris[cite: 70].   │
│  • (Opcional) Mejorar el contraste[cite: 70].         │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 2. DETECCIÓN DE REGIONES                               │
│  • Aplicar mser.detectRegions[cite: 69].              │
│  • Encontrar zonas de alto contraste[cite: 69].       │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 3. CONVERSIÓN A RECTÁNGULOS                            │
│  • Usar cv2.boundingRect para encapsular píxeles       │
│    detectados[cite: 73].                               │
│  • Agrandar el rectángulo para incluir el borde        │
│    blanco exterior del panel[cite: 77].                │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 4. FILTRADO GEOMÉTRICO BÁSICO                          │
│  • Calcular relación de aspecto (ancho/alto) [cite: 74]│
│  • Eliminar regiones excesivamente alargadas           │
│    (falsos positivos)[cite: 75].                      │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 5. NORMALIZACIÓN DE TAMAÑO                             │
│  • Recortar cada ventana detectada[cite: 83].         │
│  • Cambiar el tamaño a uno fijo (ej. 40x80) usando     │
│    cv2.resize[cite: 83].                              │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 6. EXTRACCIÓN DE COLOR (MÁSCARA HSV)                   │
│  • Pasar el recorte al espacio de color HSV[cite: 79].│
│  • Localizar píxeles de color azul muy saturado        │
│   [cite: 79].                                         │
│  • Crear matriz (ej. 40x80) donde Azul=1, Resto=0      │
│   [cite: 80].                                         │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 7. SCORING POR CORRELACIÓN                             │
│  • Correlar (multiplicar y sumar) la máscara extraída  │
│    con una máscara ideal de panel[cite: 86].          │
│  • Si el valor no supera un umbral, descartar la       │
│    ventana ("no es panel")[cite: 88].                 │
│  • Si lo supera, ese valor será el "score"[cite: 90]. │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 8. ELIMINACIÓN DE DUPLICADOS (NMS)                     │
│  • Filtrar detecciones repetidas sobre el mismo        │
│    panel[cite: 141, 142].                             │
│  • Criterios: Solapamiento (IoU), quedarse con el de   │
│    mayor score, o promediar[cite: 145, 146, 147].     │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 9. SALIDA DE DATOS                                     │
│  • Guardar imagen en "resultado_imgs" con cajas rojas  │
│    y el score en amarillo[cite: 163].                 │
│  • Escribir "resultado.txt" con formato:               │
│    fichero;x1;y1;x2;y2;1;score[cite: 164, 165].       │
└────────────────────────────────────────────────────────┘