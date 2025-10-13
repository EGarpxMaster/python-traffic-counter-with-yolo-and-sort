# import the necessary packages
import numpy as np
import argparse
import time
import cv2
import os
import glob
from ultralytics import YOLO

# Clean previous output files
files = glob.glob('output/*.png')
for f in files:
   os.remove(f)

# No need to import SORT separately as we'll use Ultralytics' built-in tracking
memory = {}
line = [(43, 543), (550, 655)]
counter = 0

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input video")
ap.add_argument("-o", "--output", required=True,
	help="path to output video")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applying non-maxima suppression")
args = vars(ap.parse_args())

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def ccw(A,B,C):
	return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Load YOLOv11x model with BoTSORT tracking
print("[INFO] loading YOLOv11x with BoTSORT from Ultralytics...")
model = YOLO('yolo11x.pt')  # This will automatically download the model if not present

# Vehicle classes from COCO dataset (cars, motorcycles, buses, trucks)
vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(200, 3), dtype="uint8")

# initialize the video stream, pointer to output video file, and frame dimensions
vs = cv2.VideoCapture(args["input"])
writer = None
(W, H) = (None, None)

frameIndex = 0

# try to determine the total number of frames in the video file
try:
	total = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
	print("[INFO] {} total frames in video".format(total))
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
	                     tracker="botsort.yaml", verbose=False, classes=vehicle_classes,
	                     persist=True)
	end = time.time()

	# Process tracking results
	boxes = []
	indexIDs = []
	previous = memory.copy()
	memory = {}

	# Extract tracking information from results
	if results[0].boxes is not None and results[0].boxes.id is not None:
		for i, (box, track_id) in enumerate(zip(results[0].boxes.xyxy, results[0].boxes.id)):
			x1, y1, x2, y2 = box.cpu().numpy().astype(int)
			track_id = int(track_id.cpu().numpy())
			
			boxes.append([x1, y1, x2, y2])
			indexIDs.append(track_id)
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
					counter += 1

			# Draw object ID
			text = "{}".format(indexIDs[i])
			cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
			i += 1

	# draw counting line
	cv2.line(frame, line[0], line[1], (0, 255, 255), 5)

	# draw counter
	cv2.putText(frame, str(counter), (100, 200), cv2.FONT_HERSHEY_DUPLEX, 5.0, (0, 255, 255), 10)

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
		writer.release()
		vs.release()
		exit()

# release the file pointers
print("[INFO] cleaning up...")
writer.release()
vs.release()