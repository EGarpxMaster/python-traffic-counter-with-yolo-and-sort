@echo off
echo Installing Python Traffic Counter dependencies for YOLOv11x with BoTSORT...
echo.

echo Checking Python version...
python --version
echo.

echo Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo To run the updated version with YOLOv11x and BoTSORT tracking:
echo python main.py --input input/highway.mp4 --output output/highway.mp4 --confidence 0.5 --threshold 0.3
echo.
echo The YOLOv11x model and BoTSORT tracker will be automatically downloaded on first run.
echo BoTSORT provides improved tracking with appearance-based re-identification.
echo.
pause