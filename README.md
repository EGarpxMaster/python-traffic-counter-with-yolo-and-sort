# Python Traffic Counter

The purpose of this project is to detect and track vehicles on a video stream and count those going through a defined line. 

![highway.gif](highway.gif)

## Updated for 2025
This project has been updated to use:

* **YOLOv11x** from [Ultralytics](https://github.com/ultralytics/ultralytics) for state-of-the-art object detection
* **BoTSORT** tracking algorithm for improved multi-object tracking with appearance-based association
* **Python 3.11** compatibility
* **Improved performance** and accuracy

It uses:
* **YOLOv11x** for object detection on each video frame (automatically downloads model)
* **BoTSORT** algorithm to track objects over different frames with appearance-based re-identification

**BoTSORT Advantages over SORT:**
- Better handling of occlusions
- Appearance-based re-identification 
- Improved long-term tracking
- Reduced identity switches
- Better performance in crowded scenes

Once the objects are detected and tracked over different frames, a simple mathematical calculation is applied to count the intersections between the vehicles' previous and current frame positions with a defined line.

## Requirements

- Python 3.11
- Dependencies listed in `requirements.txt`

## Installation

1. Clone or download this repository
2. Install Python 3.11
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The updated version automatically downloads the YOLOv11x model on first run:

```bash
python main.py --input input/highway.mp4 --output output/highway.mp4 --confidence 0.5 --threshold 0.3
```

### Parameters:
- `--input`: Path to input video file
- `--output`: Path to output video file  
- `--confidence`: Minimum confidence threshold for detections (default: 0.5)
- `--threshold`: IoU threshold for non-maximum suppression (default: 0.3)

## Quick Start with Windows

Run the installation script:
```bash
install.bat
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