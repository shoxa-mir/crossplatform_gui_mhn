import cv2
import pafy
import numpy as np

from model import MHN, simplified_model
from model.utils import get_horizon_points

# Initialize video
# cap = cv2.VideoCapture("test.mp4")

videoUrl = 'https://youtu.be/jvRDlJvG8E8'
videoPafy = pafy.new(videoUrl)
print(videoPafy.streams)
cap = cv2.VideoCapture(videoPafy.streams[-1].url)
start_time = 0 # skip first {start_time} seconds
cap.set(cv2.CAP_PROP_POS_FRAMES, start_time*30)

# Initialize road detector
model_path = "models/hybridnets_384x512/hybridnets_384x512.onnx"
anchor_path = "models/hybridnets_384x512/anchors_384x512.npy"
simplified_model(model_path) # Remove unused nodes
roadEstimator = MHN(model_path, anchor_path, conf_thres=0.5, iou_thres=0.5)

out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (1280+720,720))

cv2.namedWindow("Road Detections", cv2.WINDOW_NORMAL)	
while cap.isOpened():

	# Press key q to stop
	if cv2.waitKey(1) == ord('q'):
		break

	try:
		# Read frame from the video
		ret, new_frame = cap.read()
		if not ret:	
			break

		if horizon_points is None:
			horizon_points = get_horizon_points(new_frame)

	except:
		continue
	
	# Update road detector
	seg_map, filtered_boxes, filtered_scores = roadEstimator(new_frame)

	combined_img = roadEstimator.draw_all(new_frame, horizon_points)

	cv2.imshow("Road Detections", combined_img)
	out.write(combined_img)

out.release()