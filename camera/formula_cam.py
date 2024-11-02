import cv2
import numpy as np

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

class FormulaCamera:
    def __init__(self):

        # Initialize lap count and driver positions
        self.lap_count = 0
        self.driver_positions = ["M.Stapper", "Magic Alonso"]

        self.main()

    # Function to increment the lap counter
    def increment_lap(self):
        self.lap_count += 1

    # Function to swap driver positions
    def swap_positions(self):
        
        self.driver_positions[0], self.driver_positions[1] = self.driver_positions[1], self.driver_positions[0]

    def main(self):

        # Font settings for display text
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 0.7
        font_color = (255, 255, 255)
        font_thickness = 1

        # Open video capture (webcam)
        cap = cv2.VideoCapture(0)

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                break
            
            track = cv2.imread("track.png")
            track = cv2.resize(track, (0, 0), fx=0.7, fy=0.7)
            track = rotate_image(track, 30)

            frame = overlay_image(frame, track, -70, 120)


            # Draw the lap counter and position board
            cv2.rectangle(frame, (10, 10), (210, 120), (0, 0, 0), -1)  # Background for the sidebar

            # Display lap counter
            lap_text = f"Lap: {self.lap_count}"
            cv2.putText(frame, lap_text, (20, 40), font, font_scale, font_color, font_thickness)
            
            cv2.rectangle(frame, (10, 45), (210, 46), (0, 0, 255), -1)
            cv2.rectangle(frame, (10, 10), (210, 15), (255, 0, 0), -1) 
            cv2.rectangle(frame, (10, 10), (15, 120), (255, 0, 0), -1) 
            # Display driver positions
            for i, driver in enumerate(self.driver_positions, start=1):
                position_text = f"{i}. {driver}"
                cv2.putText(frame, position_text, (20, 40 + i * 30), font, font_scale, font_color, font_thickness)

            # Display the resulting frame
            cv2.imshow('Live Feed with Lap Counter and Position Board', frame)

            # Keyboard controls
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break  # Quit on 'q'
            elif key == ord('l'):
                increment_lap()  # Increment lap count on 'l'
            elif key == ord('s'):
                swap_positions()  # Swap positions on 's'

        # Release the capture and close windows
        cap.release()
        cv2.destroyAllWindows()

FormulaCamera()