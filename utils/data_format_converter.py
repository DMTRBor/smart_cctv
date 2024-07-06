import cv2
import os
from datetime import datetime


def frames_to_video(images_path,
                    img_format='.jpg',
                    video_format='mp4',
                    video_file_path=None,
                    fourcc='X264',
                    fps=20.0):
    images = [os.path.join(images_path, img) for img in os.listdir(images_path) if img.endswith(img_format)]
    images.sort(key=os.path.getctime)
    frame = cv2.imread(images[0])
    height, width, _ = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*fourcc)

    video = cv2.VideoWriter(
        f'{video_file_path}/video_{datetime.now().strftime("%d-%b-%Y_%H_%M_%S")}.{video_format}',
        fourcc,
        fps,
        (width,height))

    for image in images:
        video.write(cv2.imread(image))

    cv2.destroyAllWindows()
    video.release()


def video_to_frames(video_path, images_path, image_format='jpg'):
    count = 0
    cap = cv2.VideoCapture(video_path)
    success, image = cap.read()
    success = True

    while success:
        cap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
        success, image = cap.read()
        print ('Read a new frame: ', success)
        try:
            cv2.imwrite(f'{images_path}/frame{count}.{image_format}', image)
        except:
            print(f'Failed to read frame: {count}') 
        count = count + 1      


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()

    choice = int(input('1. Convert images to video file\n2. Convert video to images\n>'))

    if choice == 1:
        frames_path = filedialog.askdirectory(title='Select Images Folder To Convert')
        data_format = '.jpg'
        video_format = 'mp4'
        video_path = filedialog.askdirectory(title='Save Video To')

        frames_to_video(frames_path, data_format, video_format, video_path)
    else:
        video_path = filedialog.askopenfile(title='Select Video File')
        frames_path = filedialog.askdirectory(title='Select Folder To Save Images')

        video_to_frames(video_path.name, frames_path)
