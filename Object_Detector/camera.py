import cv2 
import torch
import numpy as np
from playSound import playSound, stop_sound
import time
from matchAndUpdate import match_and_update
import os

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5m', pretrained=True)

# Set up the video source (use "0" for the webcam)
cap = cv2.VideoCapture(0)

# Initial configurations
object_number = 2
started = False
is_red = False
canBeRed = False
object_id = 0
tracked_objects = {}  # Dictionary to track objects with their ID and position
last_seen_times = {}  # Dictionary to track the last seen time of each object
alert_triggered = False  # Flag to indicate if the alert has been triggered
start_alert_timer = None
active_objects = {}  # Dictionary of active objects and their time of addition
initial_objects = set()  # Set to store the first two detected objects

# Create a folder to save images, if it doesn't exist
output_folder = "detected_objects"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def save_object_snapshot(frame, obj_id, label):
    """Saves an image of the frame when a new object is detected.

    Args:
        frame (numpy.ndarray): The current video frame.
        obj_id (int): The ID of the detected object.
        label (str): The label of the detected object.
    """
    filename = os.path.join(output_folder, f"{label}_{obj_id}.jpg")
    cv2.imwrite(filename, frame)
    if os.path.exists(filename):
        print(f"Saved image: {filename}")
    else:
        print(f"Error saving image: {filename}")

def check_for_alert(active_objects):
    """Checks if the alert conditions are met based on the active objects.

    Args:
        active_objects (list): List of currently active objects.
    """
    global alert_triggered, start_alert_timer, started, object_number, canBeRed
    
    current_time = time.time()
    
    # Start detection if the number of active objects meets the threshold
    if len(active_objects) >= object_number:
        started = True

    # Check if the number of active objects is below the threshold
    if (len(active_objects) < object_number) and started:
        if start_alert_timer is None:
            start_alert_timer = current_time
        elif current_time - start_alert_timer >= 5:
            canBeRed = True
            if current_time - start_alert_timer >= 10:
                if not alert_triggered:
                    playSound()
                    alert_triggered = True
    else:
        # Reset the alert
        start_alert_timer = None
        alert_triggered = False
        canBeRed = False
        stop_sound()

# Detection and visualization loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect objects in the frame
    results = model(frame)
    detections = results.pred[0].cpu().numpy()

    # Filter detections based on confidence
    filtered_detections = [detection for detection in detections if detection[4] > 0.5]

    # Update tracking
    tracked_objects = match_and_update(filtered_detections, tracked_objects, last_seen_times, object_id)

    # Draw bounding boxes and save images
    for obj_id, data in tracked_objects.items():
        x1, y1, x2, y2 = map(int, data['box'])
        label = model.names[int(data['class'])]
        conf = data['conf']

        # Save a photo if a new object is detected
        if label != "person" and label != "dog":
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID {obj_id}: {label} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            save_object_snapshot(frame, obj_id, label)

    # Update or add `time_added` for detected objects
    current_time = time.time()
    for obj_id, data in tracked_objects.items():
        label = model.names[int(data['class'])]
        if len(initial_objects) < 2:
            # Add the object to the first two monitored objects
            initial_objects.add(obj_id)
            active_objects[obj_id] = {'data': data, 'time_added': current_time}
        elif obj_id in initial_objects:
            # If the object is one of the first two, update `time_added`
            active_objects[obj_id] = {'data': data, 'time_added': current_time}

    # Remove objects that haven't been detected for over 10 seconds
    active_objects = {
        obj_id: obj_data
        for obj_id, obj_data in active_objects.items()
        if current_time - obj_data['time_added'] < 10
    }

    # Display the number of active objects
    active_objects_len = len(active_objects)
    cv2.putText(frame, f"Object Detected: {active_objects_len}", (70, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

    # Check for alerts
    check_for_alert(list(active_objects.values()))

    if is_red and canBeRed:
        # Apply a red filter
        red_frame = frame.copy()
        red_frame[:, :, 1] = 0  # Remove the green channel
        red_frame[:, :, 0] = 0  # Remove the blue channel
        cv2.imshow('Object Detector', red_frame)
    else:
        # Show the normal video
        cv2.imshow('Object Detector', frame)

    # Toggle `is_red` state every 500ms
    if int(time.time() * 2) % 2 == 0:
        is_red = not is_red

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()
