import argparse
import requests
import jsonpickle
import logging
import json
import os
from tqdm import tqdm
from PIL import Image

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def main(url, video_path, width_max, height_max, fps_max, save_dir):
    os.makedirs(save_dir, exist_ok=True)

    with open(video_path, 'rb') as stream:
        binary_video = stream.read()

    data = {'fps_max': fps_max,
            'width_max': width_max,
            'height_max': height_max,
            'video': binary_video}
    data = jsonpickle.encode(data)
    response = requests.post(url, json=data)
    response = jsonpickle.decode(response.text)

    frames = response['frames']
    metadata = response['metadata']

    logging.info(f"metadata of the video is {metadata}")

    with open(os.path.join(save_dir, f"{os.path.basename(video_path)}.metadata.json"), 'w') as stream:
        json.dump(metadata, stream, indent=4)

    assert len(frames) == len(metadata['frame_idx_original'])

    for frame, idx in tqdm(zip(frames, metadata['frame_idx_original'])):
        fp = os.path.join(save_dir, os.path.basename(
            video_path)) + f".{str(idx).zfill(5)}.jpg"
        frame.save(fp)
        logging.info(f"{fp} saved")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='send a video to the client and get back the frames.')
    parser.add_argument('--url', type=str,
                        default='http://127.0.0.1:10001/extract-frames')
    parser.add_argument('--video-path', type=str)
    parser.add_argument('--width-max', type=int, default=1280)
    parser.add_argument('--height-max', type=int, default=720)
    parser.add_argument('--fps-max', type=int, default=1)
    parser.add_argument('--save-dir', type=str, default='./data/')

    args = parser.parse_args()
    args = vars(args)

    logging.info(f"arguments given to {__file__}: {args}")

    main(**args)
