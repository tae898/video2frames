# video2frames

This repo includes a light-weight Flask API server that receives a binary video (e.g. mp4) and returns JPEG-encoded frames.

[Watch a demo video](https://youtu.be/dnmE42q61VY).


## Pull and run in a docker container (recommended)

1. Make sure you are at the root directory of this repo.

1. Pull the image.
    ```bash
    docker pull tae898/video2frames:latest
    ```
1. Run the container.
    ```bash
    docker run -it --rm -p 10001:10001 tae898/video2frames:latest
    ```
1. Build the image (optional).

    For whatever reason you want to build it from scratch, you can do so by
    ```bash
    docker build -t video2frames .
    ```

## Run directly

1. Make sure you are at the root directory of this repo.

1. Install the requirements
    ```bash
    pip3 install -r requirements.txt
    ```

1. Run the app
    ```bash
    python3 app.py
    ```

## Client-side

Let's test the flask api server if it's running okay.

1. Make sure you are at the root directory of this repo.

1. Install the requirements. I recommend you to run this in a virtual python environment.
    ```bash
    pip3 install -r requirements-client.txt
    ```

1. Run the client in python (i.e. `python3 client.py --video-path data/Tae.mp4`). Below is just an example. See `client.py` for the full code.
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

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact

Feel free to contact me.

* [Taewoon Kim](https://taewoonkim.com/)

