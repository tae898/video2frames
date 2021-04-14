# video2frames

This server-side flask app accepts a video and returns extracted frames with metadata.

## Server-side

You can either run the `app.py` directly with Python3 or in a docker container.

### Run directly

In this current directory where `README.md` is located,

1. Install the requirements
    ```bash
    pip3 install -r requirements.txt
    ```

1. Run the app
    ```bash
    python3 app.py
    ```

### Run in a docker container (recommended)

In this current directory where `README.md` is located,

1. Build the container.
    ```bash
    docker build -t video2frames .
    ```
1. Run the container.
    ```bash
    docker run -p 10001:10001 video2frames 
    ```

## Client-side

In this current directory where `README.md` is located,


1. Install the requirements
    ```bash
    pip3 install -r requirements-client.txt
    ```
1. Run the server 

1. Run the client in python. Below is just an example.
    ```python
    import requests
    import jsonpickle
    url = 'http://127.0.0.1:10001/extract-frames'
    files = {'video': open('../data/Tae.mp4', 'rb')}
    data = {'fps_max':10, 'width_max':640, 'height_max': 480}
    response = requests.post(url, files=files, data=data)
    response = jsonpickle.decode(response.text)

    frames = response['frames']
    metadata = response['metadata']
    ```

   - `fps_max` is your target maximum fps.
   - `width_max` is your target maximum width.
   - `height_max` is your target maximum height.
   - `frames` will give you a list of of PIL Image images.
   - `metadata` will give you metadata of the video and extracted frames. Below is an example.
        ```
        {'num_frames_original': 555, 'num_frames': 93, 'duration_seconds': 9.25, 'fps_original': 60.0, 'fps': 10.054054054054054, 'width_original': 1280, 'height_original': 720, 'width': 640, 'height': 360, 'frame_idx_original': [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96, 102, 108, 114, 120, 126, 132, 138, 144, 150, 156, 162, 168, 174, 180, 186, 192, 198, 204, 210, 216, 222, 228, 234, 240, 246, 252, 258, 264, 270, 276, 282, 288, 294, 300, 306, 312, 318, 324, 330, 336, 342, 348, 354, 360, 366, 372, 378, 384, 390, 396, 402, 408, 414, 420, 426, 432, 438, 444, 450, 456, 462, 468, 474, 480, 486, 492, 498, 504, 510, 516, 522, 528, 534, 540, 546, 552]}
        ```
