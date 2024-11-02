from importlib.resources import files

import cv2
import numpy as np
from time import sleep as zzz
import eris.stream

def overlay_image(background, overlay, x_offset=0, y_offset=0):
    """
    Overlay one image on top of another with transparency.
    
    Parameters:
    background: numpy array of shape (h, w, c) - The base image
    overlay: numpy array of shape (h, w, c) - The image to overlay
    x_offset: int - Horizontal offset for overlay placement
    y_offset: int - Vertical offset for overlay placement
    
    Returns:
    numpy array - The combined image
    """
    # Create a copy of the background to avoid modifying the original
    result = background.copy()
    
    # Get dimensions
    h1, w1 = background.shape[:2]
    h2, w2 = overlay.shape[:2]
    
    # Calculate the valid overlay region
    x1 = max(0, x_offset)
    y1 = max(0, y_offset)
    x2 = min(w1, x_offset + w2)
    y2 = min(h1, y_offset + h2)
    
    # Calculate overlay image bounds
    x1_overlay = max(0, -x_offset)
    y1_overlay = max(0, -y_offset)
    x2_overlay = min(w2, x2 - x_offset)
    y2_overlay = min(h2, y2 - y_offset)
    
    # Get the overlay region
    overlay_region = overlay[y1_overlay:y2_overlay, x1_overlay:x2_overlay]
    
    # Create a mask for non-zero pixels
    if overlay.ndim == 3:
        mask = (overlay_region != 0).any(axis=2)
    else:
        mask = overlay_region != 0
        
    # Apply the overlay only where mask is True
    result[y1:y2, x1:x2][mask] = overlay_region[mask]
    
    return result

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
       # draw circle here (etc...)
       print('x = %d, y = %d'%(x, y))

track_pos = [(90,310), (96,320), (102,327),
    (113, 329), (123, 330), (129, 324), (137, 319), (143, 309),
    (143, 302), (137, 290), (132, 283), (130, 278), (122, 269),
    (119, 263), (116, 257), (113, 252), (110, 249), (105, 242),
    (102, 236), (99, 227), (96, 222), (92, 210), (90, 208),
    (85, 200), (82, 196), (79, 189), (80, 181), (80, 173),
    (84, 168), (91, 163), (91, 163), (96, 160), (105, 160),
    (111, 160), (118, 165), (122, 169), (126, 176), (126, 181),
    (126, 187), (126, 192), (125, 199), (119, 201), (116, 205),
    (113, 209), (102, 213), (92, 219), (85, 223), (77, 228),
    (69, 233), (64, 242), (61, 250), (60, 256), (61, 264),
    (67, 270), (71, 279), (75, 285), (81, 293), (85, 299),
    (88, 307), (88, 308)
]

class FormulaCamera:
    def __init__(self):

        # Initialize lap count and driver positions
        self.lap_count = 0
        self.driver_positions = ["M.Stapper", "Magic Alonso"]
        self.driver_color = [(200, 50, 0), (20, 200, 20)]

    # Function to increment the lap counter
    def increment_lap(self):
        self.lap_count += 1

    # Function to swap driver positions
    def swap_positions(self):
        
        self.driver_positions[0], self.driver_positions[1] = self.driver_positions[1], self.driver_positions[0]

    @staticmethod
    def main():
        this = FormulaCamera()
        # Font settings for display text
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 0.7
        font_color = (255, 255, 255)
        font_thickness = 1

        # Open video capture (webcam)
        cap = cv2.VideoCapture(0)
        time = 0

        while True:
            time += 0.8
            zzz(0.1)

            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                break
            
            track = cv2.imread(files(eris.stream).joinpath("track.png"))
            track = cv2.resize(track, (0, 0), fx=0.7, fy=0.7)
            track = rotate_image(track, 30)

            frame = overlay_image(frame, track, -70, 120)


            # Draw the lap counter and position board
            cv2.rectangle(frame, (10, 10), (210, 120), (0, 0, 0), -1)  # Background for the sidebar

            # Display lap counter
            lap_text = f"Lap: {this.lap_count}"
            cv2.putText(frame, lap_text, (20, 40), font, font_scale, font_color, font_thickness)
            
            cv2.rectangle(frame, (10, 45), (210, 46), (0, 0, 255), -1)
            cv2.rectangle(frame, (10, 10), (210, 15), (255, 0, 0), -1) 
            cv2.rectangle(frame, (10, 10), (15, 120), (255, 0, 0), -1) 
            # Display driver positions
            for i, driver in enumerate(this.driver_positions, start=1):
                position_text = f"{i}. {driver}"
                cv2.putText(frame, position_text, (20, 40 + i * 30), font, font_scale, this.driver_color[i-1], font_thickness)

            
            
            cv2.circle(frame, track_pos[int(time % len(track_pos))], 3, (200, 0, 200), -1)

            # Display the resulting frame

            cv2.imshow('Durhack Grand Prix', frame)
            cv2.setMouseCallback('Durhack Grand Prix', onMouse)
            


            # Keyboard controls
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break  # Quit on 'q'
            elif key == ord('l'):
                this.increment_lap()  # Increment lap count on 'l'
            elif key == ord('s'):
                this.swap_positions()  # Swap positions on 's'

        # Release the capture and close windows
        cap.release()
        cv2.destroyAllWindows()