# Python Traffic Counter

Vehicle detection and tracking system using YOLOv11x and BoTSORT for counting objects crossing a defined line.

![highway.gif](highway.gif)

## Features

* **YOLOv11x** - State-of-the-art object detection
* **BoTSORT** - Advanced multi-object tracking with appearance-based re-identification  
* **COCO Classes** - Support for 80 object classes with flexible filtering
* **Python 3.11** - Modern Python compatibility

## Installation

1. Install Python 3.11
2. Install dependencies:
```bash
pip install -r requirements.txt
```
Or run: `install.bat` (Windows)

## Usage

### Basic (vehicles only):
```bash
python main.py --input input/highway.mp4 --output output/highway.mp4
```

### With class selection:
```bash
# People and vehicles (shows as "5 car", "12 person", etc.)
python main.py --input input/video.mp4 --output output/result.mp4 --classes people_and_vehicles

# All transportation with detailed IDs (shows as "ID:5 car", "ID:12 person", etc.)
python main.py --input input/video.mp4 --output output/result.mp4 --classes transportation --show-labels

# All 80 COCO classes with detailed format
python main.py --input input/video.mp4 --output output/result.mp4 --classes all --show-labels
```

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