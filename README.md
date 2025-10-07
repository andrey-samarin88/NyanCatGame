Команда сборки::
pyinstaller --onefile --windowed `
  --name "Nyan_Cat_Game" `
  --add-data "images;images" `
  --add-data "sounds;sounds" `
  main.py

