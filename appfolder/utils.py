import cv2
import numpy as np
from .models import ColorResult
import base64

def process_image(image_data):
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValueError("Error: Unable to decode image data")
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    segment_positions = [
        (20, 90), (120, 180), (210, 270), (300, 350),
        (390, 450), (470, 530), (560, 620), (650, 720),
        (740, 800), (830, 900)
    ]
    box_width = 60
    rgb_values = []

    for (y1, y2) in segment_positions:
        center_y = (y1 + y2) // 2
        start_x = (image_rgb.shape[1] - box_width) // 2
        end_x = start_x + box_width
        start_y = center_y - box_width // 2
        end_y = center_y + box_width // 2
        segment = image_rgb[start_y:end_y, start_x:end_x]
        mean_color = segment.mean(axis=(0, 1))
        rgb_values.append(mean_color.astype(int).tolist())

    labels = ['URO', 'BIL', 'KET', 'BLD', 'PRO', 'NIT', 'LEU', 'GLU', 'SG', 'PH']
    results = {label: rgb for label, rgb in zip(labels, rgb_values)}

    # image to base64 string
    _, image_encoded = cv2.imencode('.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    image_base64 = base64.b64encode(image_encoded)

    return results, image_base64
