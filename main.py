import cv2
import numpy as np
import time

def create_background(cap, num_frames=30):
    """
    Captures the background frames from a video stream.

    Parameters:
    - cap (cv2.VideoCapture): The video capture object.
    - num_frames (int): The number of frames to capture for the background.

    Returns:
    - np.ndarray: The median background frame.

    Raises:
    - ValueError: If no frames are captured for the background.
    """
    print("Capturing background. Please move out of frame.")
    backgrounds = []
    for i in range(num_frames):
        ret, frame = cap.read()
        if ret:
            backgrounds.append(frame)
        else:
            print(f"Warning: Could not read frame {i+1}/{num_frames}")
        time.sleep(0.1)
    if backgrounds:
        return np.median(backgrounds, axis=0).astype(np.uint8)
    else:
        raise ValueError("Could not capture any frames for background")

def create_mask(frame, lower_color, upper_color):
    """
    Creates a mask for a given frame using the specified lower and upper color thresholds.

    Parameters:
    - frame: The input frame to create the mask from.
    - lower_color: The lower color threshold in HSV format.
    - upper_color: The upper color threshold in HSV format.

    Returns:
    - mask: The created mask.

    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)
    return mask

def apply_cloak_effect(frame, mask, background):
    """
    Applies the invisibility cloak effect to the given frame.

    Args:
        frame (numpy.ndarray): The input frame.
        mask (numpy.ndarray): The mask representing the cloak.
        background (numpy.ndarray): The background image.

    Returns:
        numpy.ndarray: The frame with the invisibility cloak effect applied.
    """
    mask_inv = cv2.bitwise_not(mask)
    fg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    bg = cv2.bitwise_and(background, background, mask=mask)
    return cv2.add(fg, bg)

def main():
    print("OpenCV version:", cv2.__version__)

    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    try:
        background = create_background(cap)
    except ValueError as e:
        print(f"Error: {e}")
        cap.release()
        return

    # Change the HSV values to the desired color
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])

    print("Starting main loop. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            time.sleep(1)
            continue

        mask = create_mask(frame, lower_black, upper_black)
        result = apply_cloak_effect(frame, mask, background)

        cv2.imshow('Invisible Cloak', result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()