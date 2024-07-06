import os
import cv2


def play_frame_sequence(frames_path, frames_delay=30, window_size=(600,400)):
    # reorder images in sequence by frame number
    images = [os.path.join(frames_path, im_name) for im_name in os.listdir(frames_path)]
    images.sort(key=os.path.getctime)

    print('Press <ESC> key to stop the player...')

    # play frames sequence
    for im_name in images:
        frame = cv2.imread(im_name)
        frame = cv2.resize(frame, dsize=window_size)
        cv2.imshow('Player', frame)
        k = cv2.waitKey(frames_delay) & 0xFF
        if k == 27:  # ESC key press
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()

    load_data_path = filedialog.askdirectory(title='Load Data To Display')

    frames_delay = 200

    play_frame_sequence(load_data_path, frames_delay=frames_delay)
