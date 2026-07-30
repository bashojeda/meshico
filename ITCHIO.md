# Publicar en itch.io

Sube `build/meshico-itchio.zip` como archivo de proyecto y marca la opción
**This file will be played in the browser**. No descomprimas el archivo antes
de subirlo: `index.html` ya está en la raíz del ZIP.

Configuración recomendada en itch.io:

- Tipo de proyecto: HTML.
- Tamaño de viewport: 1000 × 700 (o *Fullscreen*).
- Activa *Mobile friendly* solo después de añadir controles táctiles.

Para generar una nueva versión, primero ejecuta las pruebas y luego vuelve a
empaquetar los archivos web. `pygbag.ini` evita que los entornos, pruebas y
cachés formen parte de la exportación.
