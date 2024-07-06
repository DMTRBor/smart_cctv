from smart_cctv_core import *


def main(images_data_path=None,
         path_to_save=None,
         min_frames_detected=5,
         conn_comp_thr=1000,
         is_show=True,
         frames_delay=30,
         is_run_yolo=True,
         window_size=(600,400)):
    foreground_model = background_subtractor()
    idx = []
    filtered_frames = []
    frame_counter = 0

    print('Start data processing...')

    for im_name in os.listdir(images_data_path):
        frame_counter += 1
        frame = cv2.imread(os.path.join(images_data_path, im_name))
        frame = cv2.resize(frame, dsize=window_size)

        foreground_mask = foreground_model.apply(frame)

        denoised_frame = noise_filtering(foreground_mask)

        filtered_frame = filter_connected_components(denoised_frame, conn_comp_thr)

        if np.sum(filtered_frame) > 0:
            idx.append(frame_counter)
            filtered_frames.append(frame)

        if len(idx) >= 2 and idx[-1] > idx[-2] + 1:
            save_frames(filtered_frames, frame_counter, min_frames_detected, path_to_save, is_run_yolo)
            idx = []
            filtered_frames = []

        filtered = np.zeros(frame.shape, np.uint8)
        filtered[:,:,0], filtered[:,:,1], filtered[:,:,2] = filtered_frame, filtered_frame, filtered_frame
        original_and_filtered = np.hstack((frame, filtered))

        if is_show:
            cv2.imshow('Frames', original_and_filtered)
            k = cv2.waitKey(frames_delay) & 0xFF
            if k == 27:  # ESC key press
                break

    save_frames(filtered_frames, frame_counter, min_frames_detected, path_to_save, is_run_yolo)  # save last frames
    cv2.destroyAllWindows()
    print('Data processing finished!')


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()

    load_data_path = filedialog.askdirectory(title='Load Data')
    save_data_path = filedialog.askdirectory(title='Save Results To')

    # parameters configurations
    min_frames_detected = 5
    conn_comp_thr = 1000
    frames_delay = 5
    # flags
    is_show = True
    is_run_yolo = True

    main(load_data_path,
         save_data_path,
         min_frames_detected,
         conn_comp_thr,
         is_show,
         frames_delay,
         is_run_yolo)
