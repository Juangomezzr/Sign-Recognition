## Diagrama de Flujo del Detector

```mermaid
flowchart TD
    A["<b>IMAGEN DE ENTRADA (Test/Train)</b>"] --> B["<b>1. PREPROCESAMIENTO MSER</b><br>• Convertir la imagen a niveles de gris.<br>• (Opcional) Mejorar el contraste."]
    
    B --> C["<b>2. DETECCIÓN DE REGIONES</b><br>• Aplicar mser.detectRegions.<br>• Encontrar zonas de alto contraste."]
    
    C --> D["<b>3. CONVERSIÓN A RECTÁNGULOS</b><br>• Usar cv2.boundingRect para encapsular píxeles detectados.<br>• Agrandar el rectángulo para incluir el borde blanco exterior del panel."]
    
    D --> E["<b>4. FILTRADO GEOMÉTRICO BÁSICO</b><br>• Calcular relación de aspecto (ancho/alto).<br>• Eliminar regiones excesivamente alargadas (falsos positivos)."]
    
    E --> F["<b>5. NORMALIZACIÓN DE TAMAÑO</b><br>• Recortar cada ventana detectada.<br>• Cambiar el tamaño a uno fijo (ej. 40x80) usando cv2.resize."]
    
    F --> G["<b>6. EXTRACCIÓN DE COLOR (MÁSCARA HSV)</b><br>• Pasar el recorte al espacio de color HSV.<br>• Localizar píxeles de color azul muy saturado.<br>• Crear matriz (ej. 40x80) donde Azul=1, Resto=0."]
    
    G --> H["<b>7. SCORING POR CORRELACIÓN</b><br>• Correlar (multiplicar y sumar) la máscara extraída con una máscara ideal de panel.<br>• Si el valor no supera un umbral, descartar la ventana ('no es panel').<br>• Si lo supera, ese valor será el 'score'."]
    
    H --> I["<b>8. ELIMINACIÓN DE DUPLICADOS (NMS)</b><br>• Filtrar detecciones repetidas sobre el mismo panel.<br>• Criterios: Solapamiento (IoU), quedarse con el de mayor score, o promediar."]
    
    I --> J["<b>9. SALIDA DE DATOS</b><br>• Guardar imagen en 'resultado_imgs' con cajas rojas y el score en amarillo.<br>• Escribir 'resultado.txt' con formato: fichero;x1;y1;x2;y2;1;score."]

    %% Colores modificados para el primer y último nodo
    style A fill:#bbdefb,stroke:#1976d2,stroke-width:2px,color:#000000
    style J fill:#ffe0b2,stroke:#f57c00,stroke-width:2px,color:#000000