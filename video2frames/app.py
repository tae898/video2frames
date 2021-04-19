from flask import Flask, request, jsonify
import jsonpickle
import logging
import av
import io

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

app = Flask(__name__)


@app.route("/", methods=["POST"])
def extract_frames():
    """
    Receive everything in json!!!

    """
    app.logger.debug(f"Receiving data ...")
    data = request.json
    data = jsonpickle.decode(data)

    video = data['video']
    fps_max = data['fps_max']
    width_max = data['width_max']
    height_max = data['height_max']

    app.logger.debug(f"fps_max: {fps_max}, width_max: {width_max}, "
                     f"height_max: {height_max}")

    video = io.BytesIO(video)

    container = av.open(video)
    app.logger.info(f"{container} opened")

    metadata = {}
    fps_original = float(container.streams.video[0].average_rate)
    every_N = int(round(fps_original / fps_max))
    every_N = max(1, every_N)

    app.logger.info(f"Every {every_N} th frame will be processed.")

    frames = []
    indexes = []
    for idx, frame in enumerate(container.decode(video=0)):
        if idx % every_N != 0:
            continue

        indexes.append(idx)
        app.logger.info(f"processing {idx} th frame ...")

        image = frame.to_image()
        app.logger.info(f"original width height {image.size}")

        width_original, height_original = image.size
        image.thumbnail(size=(width_max, height_max))

        app.logger.info(f"resized to {image.size}")

        frames.append(image)
    container.close()

    num_frames_original = idx + 1
    num_frames = len(frames)
    duration_seconds = num_frames_original / fps_original

    metadata['num_frames_original'] = num_frames_original
    metadata['num_frames'] = num_frames

    metadata['duration_seconds'] = duration_seconds
    metadata['fps_original'] = fps_original
    metadata['fps'] = len(frames) / duration_seconds

    metadata['width_original'] = width_original
    metadata['height_original'] = height_original
    metadata['width'], metadata['height'] = image.size

    metadata['frame_idx_original'] = indexes

    app.logger.info(f"metadata: {metadata}")

    response = {'frames': frames,
                'metadata': metadata}
    response_pickled = jsonpickle.encode(response)

    return response_pickled


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10001)
