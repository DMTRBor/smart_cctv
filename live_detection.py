from smart_cctv_core import *


def main(is_show=True, frames_delay=1):
    print('Start live object detection...')

    video_source = cv2.VideoCapture(0)

    while True:
        _, frame = video_source.read() 

        original_and_filtered = run_yolo(frame)

        if is_show:
            cv2.imshow('Frames', original_and_filtered)
            k = cv2.waitKey(frames_delay) & 0xFF
            if k == 27:  # ESC key press
                break

    video_source.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    frames_delay = 1
    is_show = True

    main(is_show, frames_delay)
