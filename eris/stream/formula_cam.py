from importlib.resources import files

import cv2
import numpy as np
from time import sleep as zzz
import eris.stream

TUNNELCAM = 1
STARTCAM = 2
LOOPCAM = 3

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
    
    # Create a mask for pixels that are neither 0 nor 255
    if overlay.ndim == 3:
        mask = ((overlay_region > 5) & (overlay_region < 245)).any(axis=2)
    else:
        mask = ((overlay_region > 5) & (overlay_region < 245))
        
    # Apply the overlay only where mask is True
    result[y1:y2, x1:x2][mask] = overlay_region[mask]
    
    return result

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
       # draw circle here (etc...)
       print('x = %d, y = %d'%(x, y))

track_pos = [(90,310), (96,320), (102,327), (113, 329), (123, 330), 
             (129, 324), (137, 319), (143, 309), (143, 302), (137, 290), 
             (132, 283), (130, 278), (122, 269), (119, 263), (116, 257), 
             (113, 252), (110, 249), (105, 242), (102, 236), (99, 227), 
             (96, 222), (92, 210), (90, 208), (85, 200), (82, 196), 
             (79, 189), (80, 181), (80, 173), (84, 168), (91, 163), 
             (91, 163), (96, 160), (105, 160), (111, 160), (118, 165), 
             (122, 169), (126, 176), (126, 181), (126, 187), (126, 192), 
             (125, 199), (119, 201), (116, 205), (113, 209), (102, 213), 
             (92, 219), (85, 223), (77, 228), (69, 233), (64, 242), 
             (61, 250), (60, 256), (61, 264), (67, 270), (71, 279), 
             (75, 285), (81, 293), (85, 299), (88, 307), (88, 308)
]

class FormulaCamera:
    def __init__(self):

        # Initialize lap count and driver positions
        self.lap_count = 0
        self.driver_names = ["M.Stapper", "Magic Alonso"]
        self.driver_positions = [0, 1]
        self.driver_color = [(200, 90, 0), (20, 200, 20)]
        self.driver_charge = [0.5, 0.9]
        self.driver_progress = [0, 20]


        self.maxlaps = 5

        self.track = cv2.imread(files(eris.stream).joinpath("track.png"))
        self.track = cv2.resize(self.track, (0, 0), fx=0.7, fy=0.7)
        self.track = rotate_image(self.track, 30)

        self.cameras = []
        for i in range(10):
            cam = cv2.VideoCapture(i)
            if cam.isOpened():
                self.cameras.append(cam)

        self.font = cv2.FONT_HERSHEY_DUPLEX
        self.font_scale = 0.7
        self.font_color = (255, 255, 255)
        self.font_thickness = 1

    # Function to increment the lap counter
    def increment_lap(self):
        self.lap_count += 1

    # Function to swap driver positions
    def swap_positions(self):
        self.driver_positions[0], self.driver_positions[1] = self.driver_positions[1], self.driver_positions[0]

    def update_progress_all(self, data):
        self.driver_progress = data
        if data[1] > data[0]:
            self.driver_positions = [1, 0]
        else:
            self.driver_positions = [0, 1]
            

    def updateProgress(self, car, delta):
        self.driver_progress[car] += delta
        if self.driver_progress[car] > 100:
            self.driver_progress[car] -= 100

    def updateCharge(self, car, delta):
        self.driver_charge[car] += delta

    @staticmethod
    def main():
        this = FormulaCamera()
        # Font settings for display text
        # Open video capture (webcam)
        while this.display():
            pass
    
        this.releaseCams()

    def display(self):
        
        # Capture frame-by-frame
        cam = 0
        maxP = max(self.driver_progress)
        if maxP < 20:
            cam = STARTCAM
        elif maxP < 30:
            cam = TUNNELCAM
        elif maxP < 65:
            cam = LOOPCAM
        else:
            cam = STARTCAM

        ret, frame = self.cameras[cam].read()

        frame = overlay_image(frame, self.track, -70, 120)
        # Draw the lap counter and position board
        cv2.rectangle(frame, (10, 10), (220, 120), (60, 60, 60), -1)  # Background for the sidebar
        # Display lap counter
        lap_text = f"Lap: {self.lap_count}/{self.maxlaps}"
        cv2.putText(frame, lap_text, (40, 40), self.font, self.font_scale, self.font_color, self.font_thickness)
        cv2.rectangle(frame, (10, 45), (220, 46), (0, 0, 255), -1)
        cv2.rectangle(frame, (10, 10), (220, 15), (255, 0, 0), -1) 
        cv2.rectangle(frame, (10, 10), (15, 120), (255, 0, 0), -1) 

        # Display driver positions
        for i, driver in enumerate(self.driver_positions, start=1):

            position_text = f"{i}. {self.driver_names[driver]}"
            cv2.putText(frame, position_text, (20, 50 + i * 16), self.font, self.font_scale-0.2, self.driver_color[driver-1], self.font_thickness)
            # Charge Bar
            cv2.rectangle(frame, (153, 40+i*16), (153 + 60, 50+i*16), (0,0,0), -1)
            cv2.rectangle(frame, (153, 40+i*16), (153 + int((self.driver_charge[driver] * 60)), 50+i*16), (0,255,0), -1)

            cv2.circle(frame, track_pos[int(self.driver_progress[driver] % len(track_pos))], 3, self.driver_color[driver], -1)

        # Display the resulting frame

        #cv2.namedWindow('custom window', cv2.WINDOW_KEEPRATIO)
        cv2.imshow('custom window', frame)
        cv2.resizeWindow('custom window', 1000, 1000)
        #cv2.setMouseCallback('Durhack Grand Prix', onMouse)

        # Keyboard controls
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            return False  # Quit on 'q'
        elif key == ord('l'):
            self.increment_lap()  # Increment lap count on 'l'
        elif key == ord('s'):
            self.swap_positions()  # Swap positions on 's'
        
        return True

    def releaseCams(self):
        # Release the capture and close windows
        self.cameras[0].release()
        cv2.destroyAllWindows()