# Python Traffic Counter

Vehicle detection and tracking system using YOLOv11x and BoTSORT for counting objects crossing a defined line.

![highway.gif](highway.gif)

## Features

* **YOLOv11x** - State-of-the-art object detection
* **BoTSORT** - Advanced multi-object tracking with appearance-based re-identification  
* **GPU Acceleration** - Automatic NVIDIA CUDA support for 5-10x faster processing
* **Interactive Line Setup** - Draw multiple counting lines with mouse
* **COCO Classes** - Support for 80 object classes with flexible filtering
* **Python 3.11** - Modern Python compatibility
* **Performance Metrics** - Real-time FPS and GPU utilization monitoring

## Installation

### Basic Installation

1. Install Python 3.11
2. Install dependencies:
```bash
pip install -r requirements.txt
```
Or run: `install.bat` (Windows)

### GPU Acceleration (Recommended for NVIDIA GPUs)

Para aprovechar la aceleración por GPU (5-10x más rápido):

1. Verifica que tienes una GPU NVIDIA con drivers actualizados:
```powershell
nvidia-smi
```

2. Instala PyTorch con soporte CUDA:
```bash
# Para CUDA 12.1 (recomendado para GPUs modernas como RTX 4060)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Para CUDA 11.8 (GPUs más antiguas)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

3. Verifica la instalación:
```bash
python -c "import torch; print('CUDA disponible:', torch.cuda.is_available())"
```

El script detectará automáticamente la GPU y la usará para procesamiento acelerado.

## Usage

### Interactive Line Setup

Al ejecutar el script, se mostrará el primer frame del video donde puedes:

1. **Dibujar líneas de conteo**: Haz clic en dos puntos para crear cada línea
2. **Múltiples líneas**: Puedes agregar tantas líneas como necesites para diferentes direcciones
3. **Deshacer**: Presiona 'u' para eliminar la última línea
4. **Reiniciar**: Presiona 'r' para borrar todas las líneas
5. **Confirmar**: Presiona ENTER cuando termines
6. **Cancelar**: Presiona 'q' o ESC para salir

### Basic Usage (GPU Automatic):
```bash
# El script detecta y usa GPU automáticamente
python main.py --input input/highway.mp4 --output output/highway.mp4
```

### Advanced Options:
```bash
# People and vehicles (shows as "5 car", "12 person", etc.)
python main.py --input input/video.mp4 --output output/result.mp4 --classes people_and_vehicles

# All transportation with detailed IDs (shows as "ID:5 car", "ID:12 person", etc.)
python main.py --input input/video.mp4 --output output/result.mp4 --classes transportation --show-labels

# All 80 COCO classes with detailed format
python main.py --input input/video.mp4 --output output/result.mp4 --classes all --show-labels

# Force CPU usage (for testing or systems without GPU)
python main.py --input input/video.mp4 --output output/result.mp4 --cpu
```

### GPU vs CPU Performance

Con una **NVIDIA GeForce RTX 4060**:
- **GPU**: ~30-50 FPS (20-33 ms por frame) ⚡
- **CPU**: ~3-5 FPS (200-333 ms por frame) 🐌
- **Aceleración**: 8-10x más rápido con GPU

El script mostrará métricas de rendimiento al finalizar.

### Output

El sistema genera:
- Video procesado con todas las líneas de conteo visibles
- Conteos en tiempo real por línea y por clase en el video
- Archivo `output/counts.txt` con estadísticas detalladas:
  - Total general de objetos contados
  - Totales por clase (car, truck, bus, etc.)
  - Totales por línea individual
  - Desglose de clases por cada línea

### Parameters:
- `--input`: Input video path
- `--output`: Output video path  
- `--confidence`: Detection confidence (default: 0.5)
- `--threshold`: NMS threshold (default: 0.3)
- `--classes`: Object categories to detect
  - `vehicles`: Cars, trucks, motorcycles, buses, bicycles, trains
  - `people`: People only
  - `people_and_vehicles`: People and all vehicles
  - `transportation`: All transportation (vehicles, planes, boats)
  - `traffic`: Traffic infrastructure (lights, signs, meters)
  - `all`: All 80 COCO classes
- `--show-labels`: Show detailed format "ID:X class_name" instead of "X class_name"

## Requirements

- Python 3.11
- YOLOv11x model (auto-downloaded)
- See `requirements.txt` for dependencies
```

## Citation

### YOLO :

    @article{redmon2016yolo9000,
      title={YOLO9000: Better, Faster, Stronger},
      author={Redmon, Joseph and Farhadi, Ali},
      journal={arXiv preprint arXiv:1612.08242},
      year={2016}
    }

### SORT :

    @inproceedings{Bewley2016_sort,
      author={Bewley, Alex and Ge, Zongyuan and Ott, Lionel and Ramos, Fabio and Upcroft, Ben},
      booktitle={2016 IEEE International Conference on Image Processing (ICIP)},
      title={Simple online and realtime tracking},
      year={2016},
      pages={3464-3468},
      keywords={Benchmark testing;Complexity theory;Detectors;Kalman filters;Target tracking;Visualization;Computer Vision;Data Association;Detection;Multiple Object Tracking},
      doi={10.1109/ICIP.2016.7533003}
    }