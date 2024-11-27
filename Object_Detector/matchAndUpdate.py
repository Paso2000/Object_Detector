from interctionOverUnion import iou
import time

def match_and_update(detections, tracked_objects, last_seen_times, object_id):
    threshold = 0.3
    updated_tracked_objects = {}
    for det in detections:
        x1, y1, x2, y2, conf, cls = det
        best_iou = 0
        best_id = None

        for obj_id, tracked_box in tracked_objects.items():
            iou_score = iou((x1, y1, x2, y2), tracked_box['box'])
            if iou_score > best_iou:
                best_iou = iou_score
                best_id = obj_id

        if best_iou > threshold:
            updated_tracked_objects[best_id] = {'box': (x1, y1, x2, y2), 'class': cls, 'conf': conf}
            last_seen_times[best_id] = time.time()  # Aggiorna il tempo di ultima vista
        else:
            object_id += 1
            updated_tracked_objects[object_id] = {'box': (x1, y1, x2, y2), 'class': cls, 'conf': conf}
            last_seen_times[object_id] = time.time()

    return updated_tracked_objects



