# import the necessary packages
import numpy as np
import argparse
import time
import cv2
import os
import glob
import sys

# Remove any conflicting ultralytics paths
paths_to_remove = []
for path in sys.path:
    if 'YOLOv8-DeepSORT-Object-Tracking' in path:
        paths_to_remove.append(path)
        
for path in paths_to_remove:
    sys.path.remove(path)

from ultralytics import YOLO
from coco_classes import filter_classes_by_category, get_class_name

# Clean previous output files
files = glob.glob('output/*.png')
for f in files:
   os.remove(f)

# Global variables
memory = {}
line = [(43, 543), (550, 655)]
# Total counter (all objects)
counter = 0
# Per-class counters
class_counts = {}
# Keep track of which track IDs have been counted to avoid double counting
counted_ids = set()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="path to input video")
ap.add_argument("-o", "--output", required=True, help="path to output video")
ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3, help="threshold when applying non-maxima suppression")
ap.add_argument("--classes", type=str, default="vehicles", help="classes to detect: 'vehicles', 'people', 'people_and_vehicles', 'transportation', 'traffic', 'all'")
ap.add_argument("--show-labels", action="store_true", help="show 'ID:X class_name' format instead of 'X class_name'")
args = vars(ap.parse_args())

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def ccw(A,B,C):
	return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Load YOLOv11x model with BoTSORT tracking
print("[INFO] loading YOLOv11x with BoTSORT from Ultralytics...")
model = YOLO('yolo11x.pt')  # This will automatically download the model if not present

# Get selected classes for detection
selected_classes = filter_classes_by_category(args["classes"])
print(f"[INFO] Detecting classes: {args['classes']}")
print(f"[INFO] Class IDs: {selected_classes}")
if args["classes"] != "all":
    class_names = [get_class_name(i) for i in selected_classes]
    print(f"[INFO] Class names: {class_names}")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(200, 3), dtype="uint8")

# initialize the video stream, pointer to output video file, and frame dimensions
vs = cv2.VideoCapture(args["input"])
if not vs.isOpened():
	print(f"[ERROR] Could not open video file: {args['input']}")
	exit()

writer = None
(W, H) = (None, None)

frameIndex = 0

# try to determine the total number of frames in the video file
try:
	total = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
	if total <= 0:
		print("[INFO] Could not determine frame count, processing until end of video")
		total = -1
	else:
		print(f"[INFO] {total} total frames in video")
except:
	print("[INFO] could not determine # of frames in video")
	print("[INFO] no approx. completion time can be provided")
	total = -1

# loop over frames from the video file stream
while True:
	# read the next frame from the file
	(grabbed, frame) = vs.read()

	# if the frame was not grabbed, then we have reached the end of the stream
	if not grabbed:
		break

	# if the frame dimensions are empty, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	# Run YOLOv11x inference with BoTSORT tracking
	start = time.time()
	results = model.track(frame, conf=args["confidence"], iou=args["threshold"], 
	                     tracker="botsort.yaml", verbose=False, classes=selected_classes,
	                     persist=True)
	end = time.time()

	# Process tracking results
	boxes = []
	indexIDs = []
	classIDs = []
	previous = memory.copy()
	memory = {}

	# Extract tracking information from results
	if results[0].boxes is not None and results[0].boxes.id is not None:
		for i, (box, track_id, class_id) in enumerate(zip(results[0].boxes.xyxy, results[0].boxes.id, results[0].boxes.cls)):
			x1, y1, x2, y2 = box.cpu().numpy().astype(int)
			track_id = int(track_id.cpu().numpy())
			class_id = int(class_id.cpu().numpy())
			
			boxes.append([x1, y1, x2, y2])
			indexIDs.append(track_id)
			classIDs.append(class_id)
			memory[track_id] = [x1, y1, x2, y2]

	if len(boxes) > 0:
		i = int(0)
		for box in boxes:
			# extract the bounding box coordinates (x1, y1, x2, y2)
			(x1, y1) = (int(box[0]), int(box[1]))
			(x2, y2) = (int(box[2]), int(box[3]))

			# draw a bounding box rectangle and label on the image
			color = [int(c) for c in COLORS[indexIDs[i] % len(COLORS)]]
			cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

			if indexIDs[i] in previous:
				previous_box = previous[indexIDs[i]]
				(px1, py1) = (int(previous_box[0]), int(previous_box[1]))
				(px2, py2) = (int(previous_box[2]), int(previous_box[3]))
				
				# Calculate center points for trajectory
				p0 = (int((x1 + x2) / 2), int((y1 + y2) / 2))
				p1 = (int((px1 + px2) / 2), int((py1 + py2) / 2))
				cv2.line(frame, p0, p1, color, 3)

				if intersect(p0, p1, line[0], line[1]):
					# Only count this track ID once when it crosses the line
					if indexIDs[i] not in counted_ids:
						counter += 1
						counted_ids.add(indexIDs[i])
						# increment per-class counter
						cls_name = get_class_name(classIDs[i])
						if cls_name not in class_counts:
							class_counts[cls_name] = 0
						class_counts[cls_name] += 1

			# Draw object ID and class label (always show class name)
			class_name = get_class_name(classIDs[i])
			if args["show_labels"]:
				text = f"ID:{indexIDs[i]} {class_name}"
			else:
				text = f"{indexIDs[i]} {class_name}"
			cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
			i += 1

	# draw counting line
	cv2.line(frame, line[0], line[1], (0, 255, 255), 5)

	# draw total counter
	cv2.putText(frame, str(counter), (100, 200), cv2.FONT_HERSHEY_DUPLEX, 5.0, (0, 255, 255), 10)

	# draw per-class totals on top-left corner
	start_y = 30
	for cls_name, cnt in class_counts.items():
		text = f"{cls_name}: {cnt}"
		cv2.putText(frame, text, (10, start_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
		start_y += 30

	# saves image file
	cv2.imwrite("output/frame-{}.png".format(frameIndex), frame)

	# check if the video writer is None
	if writer is None:
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*"mp4v")
		writer = cv2.VideoWriter(args["output"], fourcc, 30,
			(frame.shape[1], frame.shape[0]), True)

		# some information on processing single frame
		if total > 0:
			elap = (end - start)
			print("[INFO] single frame took {:.4f} seconds".format(elap))
			print("[INFO] estimated total time to finish: {:.4f}".format(
				elap * total))

	# write the output frame to disk
	writer.write(frame)

	# increase frame index
	frameIndex += 1

	# Optional: limit frames for testing
	if frameIndex >= 4000:
		print("[INFO] cleaning up...")
		if writer is not None:
			writer.release()
		vs.release()
		exit()

# release the file pointers
print("[INFO] cleaning up...")
if writer is not None:
	writer.release()
vs.release()

# Save counts to output/counts.txt
try:
	os.makedirs('output', exist_ok=True)
	with open('output/counts.txt', 'w', encoding='utf-8') as f:
		f.write(f"total:{counter}\n")
		for cls_name, cnt in class_counts.items():
			f.write(f"{cls_name}:{cnt}\n")
	print('[INFO] Saved counts to output/counts.txt')
except Exception as e:
	print(f"[WARN] Could not save counts: {e}")