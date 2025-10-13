# MIGRATION GUIDE: Python Traffic Counter to YOLOv11x and Python 3.11

## Summary of Changes

This project has been successfully migrated from YOLOv3 to YOLOv11x with Python 3.11 support while **maintaining the original file names**.

## Files Updated (Original Names Preserved):

### Updated Files:
1. **`main.py`** - Completely updated to use YOLOv11x from Ultralytics
2. **`sort.py`** - Updated with modern dependencies and Python 3.11 compatibility
3. **`README.md`** - Updated documentation
4. **`requirements.txt`** - Updated dependency list for Python 3.11

### New Files:
1. **`install.bat`** - Installation script for Windows
2. **`MIGRATION.md`** - This migration guide

## Key Changes

### 1. YOLO Framework Migration
- **From:** OpenCV DNN with YOLOv3 weights/config files
- **To:** Ultralytics YOLOv11x with automatic model downloading
- **Benefits:** Better accuracy, easier setup, no manual weight file downloads

### 2. Updated main.py Features:
- ✅ **No more --yolo parameter** - model downloads automatically
- ✅ **No manual weight file downloads** required
- ✅ **Better object detection** with YOLOv11x
- ✅ **Vehicle-specific filtering** (cars, motorcycles, buses, trucks)
- ✅ **Modern video codecs** (mp4v instead of MJPG)

### 3. Updated sort.py Features:
- ✅ **Fixed deprecated imports** (scipy.optimize.linear_sum_assignment)
- ✅ **Python 3.11 compatibility**
- ✅ **Optional numba support** with graceful fallback
- ✅ **Better error handling**

### 4. Dependency Updates
- **Python:** 3.7 → 3.11
- **Added:** ultralytics, torch, torchvision
- **Updated:** scipy, numpy, opencv-python, scikit-learn, filterpy

## Usage (Simplified)

### New Usage (Same file names):
```bash
# Install dependencies
pip install -r requirements.txt

# Run with automatic model download
python main.py --input input/highway.mp4 --output output/highway.mp4 --confidence 0.5 --threshold 0.3
```

### Old Usage (for reference):
```bash
# Required manual weight download
python main.py --input input/highway.mp4 --output output/highway.avi --yolo yolo-coco
```

## Installation

### Method 1: Automated (Windows)
```bash
install.bat
```

### Method 2: Manual
```bash
pip install -r requirements.txt
```

## Backward Compatibility

- **File names preserved:** `main.py` and `sort.py` maintain their original names
- **Functionality enhanced:** Same interface, better performance
- **No breaking changes:** Same command-line arguments (except --yolo removed)

## Performance Improvements

### YOLOv11x Benefits:
- 🔥 **Better Detection Accuracy**
- 🚀 **Automatic Model Management**
- ⚡ **Improved Speed** on modern hardware
- 🎯 **Vehicle-Specific Detection**
- 📱 **Easier Setup** (no manual downloads)

### SORT Tracker Benefits:
- 🔧 **Modern Dependencies**
- 🐍 **Python 3.11 Compatible**
- ⚡ **Better Performance** with updated algorithms
- 🛡️ **Better Error Handling**

## Testing

Verify the migration works:

```bash
# Test with a video file
python main.py --input input/your_video.mp4 --output output/result.mp4

# The YOLOv11x model will download automatically on first run
```

## What's New

1. **Automatic Model Download**: No more manual weight file management
2. **Better Object Detection**: YOLOv11x provides superior accuracy
3. **Modern Python Support**: Full Python 3.11 compatibility
4. **Simplified Usage**: Fewer required parameters
5. **Better Video Support**: Modern codecs and formats

## Troubleshooting

### Common Issues:

1. **Import errors:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Model download issues:**
   - Ensure internet connection
   - Model downloads automatically on first run

3. **GPU/CUDA:**
   - YOLOv11x automatically detects and uses GPU if available
   - Falls back to CPU if CUDA unavailable

This migration maintains the familiar interface while providing significant improvements in accuracy, ease of use, and modern Python compatibility.