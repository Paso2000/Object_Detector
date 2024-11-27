def iou(boxA, boxB):
    """
    Calculates the Intersection over Union (IoU) of two bounding boxes.

    The Intersection over Union is a metric used to evaluate the overlap 
    between two bounding boxes. It is defined as the area of overlap 
    divided by the area of union of the two boxes.

    Args:
        boxA (tuple): A tuple representing the first bounding box (x_min, y_min, x_max, y_max).
        boxB (tuple): A tuple representing the second bounding box (x_min, y_min, x_max, y_max).

    Returns:
        float: The IoU score, which is a value between 0 and 1. A score of 0 indicates no overlap, 
               while a score of 1 indicates complete overlap.

    """
    # Calculate the coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])  # Maximum of x_min values
    yA = max(boxA[1], boxB[1])  # Maximum of y_min values
    xB = min(boxA[2], boxB[2])  # Minimum of x_max values
    yB = min(boxA[3], boxB[3])  # Minimum of y_max values

    # Calculate the area of intersection
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    
    # Calculate the area of both bounding boxes
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    # Calculate the IoU
    return interArea / float(boxAArea + boxBArea - interArea)
