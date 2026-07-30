# Publicar en itch.io para Windows

La versión recomendada es `dist/ASCII-Mines.exe`. Es un ejecutable de Windows
autocontenido: abre la ventana del juego directamente y no muestra terminal.

En itch.io, sube el archivo y configúralo como descarga para **Windows**. No
marques **This file will be played in the browser**, porque esta versión no es
HTML.

Para crear una nueva versión, activa el entorno virtual y ejecuta:

```powershell
python -m PyInstaller --noconfirm --onefile --windowed --name ASCII-Mines main.py
```
