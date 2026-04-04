## Diagrama de Flujo del Detector

```mermaid
flowchart TD
    A["<b>IMAGEN DE ENTRADA (Test/Train)</b>"] --> B["<b>1. PREPROCESAMIENTO MSER</b><br>• Convertir la imagen a niveles de gris [cite: 70].<br>• (Opcional) Mejorar el contraste[cite: 70]."]
    
    B --> C["<b>2. DETECCIÓN DE REGIONES</b><br>• Aplicar mser.detectRegions [cite: 69].<br>• Encontrar zonas de alto contraste[cite: 69]."]
    
    C --> D["<b>3. CONVERSIÓN A RECTÁNGULOS</b><br>• Usar cv2.boundingRect para encapsular píxeles detectados [cite: 73].<br>• Agrandar el rectángulo para incluir el borde blanco exterior del panel[cite: 77]."]
    
    D --> E["<b>4. FILTRADO GEOMÉTRICO BÁSICO</b><br>• Calcular relación de aspecto (ancho/alto) [cite: 74].<br>• Eliminar regiones excesivamente alargadas (falsos positivos)[cite: 75]."]
    
    E --> F["<b>5. NORMALIZACIÓN DE TAMAÑO</b><br>• Recortar cada ventana detectada [cite: 83].<br>• Cambiar el tamaño a uno fijo (ej. 40x80) usando cv2.resize[cite: 83]."]
    
    F --> G["<b>6. EXTRACCIÓN DE COLOR (MÁSCARA HSV)</b><br>• Pasar el recorte al espacio de color HSV [cite: 79].<br>• Localizar píxeles de color azul muy saturado [cite: 79].<br>• Crear matriz (ej. 40x80) donde Azul=1, Resto=0[cite: 80]."]
    
    G --> H["<b>7. SCORING POR CORRELACIÓN</b><br>• Correlar (multiplicar y sumar) la máscara extraída con una máscara ideal de panel [cite: 86].<br>• Si el valor no supera un umbral, descartar la ventana ('no es panel') [cite: 88].<br>• Si lo supera, ese valor será el 'score'[cite: 90]."]
    
    H --> I["<b>8. ELIMINACIÓN DE DUPLICADOS (NMS)</b><br>• Filtrar detecciones repetidas sobre el mismo panel [cite: 141, 142].<br>• Criterios: Solapamiento (IoU), quedarse con el de mayor score, o promediar[cite: 145, 146, 147]."]
    
    I --> J["<b>9. SALIDA DE DATOS</b><br>• Guardar imagen en 'resultado_imgs' con cajas rojas y el score en amarillo [cite: 163].<br>• Escribir 'resultado.txt' con formato: fichero;x1;y1;x2;y2;1;score[cite: 164, 165]."]

    %% Estilos opcionales para destacar el inicio y fin
    style A fill:#f4f4f4,stroke:#333,stroke-width:2px
    style J fill:#d4edda,stroke:#28a745,stroke-width:2px