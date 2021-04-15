# face

This repo has two server-client pairs. The servers are dockerized flask api.

1. **video2frames**

    Client: Sends binary video (e.g. mp4 encoded) data to the server.
    
    Server: Receives binary video, decode it with ffmpeg, extract frames, and return them. The returned format is a json-pickled dictionary. The dictionary has two key-value pairs. This dictionary is json-pickle encoded before sending and therefore the client has to json-pickle decode it.

1.  **insightface**

    This repo is from https://github.com/deepinsight/insightface. I submoduled it in my repo and added server / client to it.

    Client: Sends json-pickle encoded PIL Image object (one RGB image)

    Server: Receives json-pickle encoded PIL Image object, json-pickle decode it, extract age, bounding box, face detection probability, gender, five landmarks, and 512-dimensional arcface embedding vector. The returned format is a json-pickled list. The number of elements in the list is the number of faces detected. Each element is a dictionary with the mentioned attributes. The client has to json-pickle decode it to retrieve them.

You might wonder why there are so many encoding / decoding going on, but if you see the examples, they are actually pretty simple. Take a look at the documentation of jsonpickle (https://jsonpickle.github.io/)


## video2frames

Server is a flask app that accepts a video and returns extracted frames with metadata.

### Server-side

You can either run the `app.py` directly with Python3 or in a docker container.

#### Run directly

1. Go to the video2frames directory (i.e. `cd video2frames`) 

1. Install the requirements
    ```bash
    pip3 install -r requirements.txt
    ```

2. Run the app
    ```bash
    python3 app.py
    ```

#### Run in a docker container (recommended)

1. Go to the video2frames directory (i.e. `cd video2frames`) 

2. Build the container.
    ```bash
    docker build -t video2frames .
    ```
3. Run the container.
    ```bash
    docker run -it --rm -p 10001:10001 video2frames 
    ```

### Client-side

1. Go to the video2frames directory (i.e. `cd video2frames`)


1. Install the requirements
    ```bash
    pip3 install -r requirements-client.txt
    ```

1. Run the client in python. Below is just an example. See `client.py` for the full code.
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

## insightface

Server is a flask app that accepts a PIL image object and returns extracted face features.

### Server-side

You can either run the `app.py` directly with Python3 or in a docker container.

#### Run directly (CPU only)

1. Go to the insightface directory (i.e. `cd insightface`)

1. Install the requirements.
    ```bash
    pip3 install -r requirements.txt
    ```

1. Install the insightface python package.

    ```bash
    cd python-package && pip install . && cd ..
    ```

2. Run both apps.
    ```bash
    python3 app.py --gpu-id -1
    ```

#### Run in a docker container (recommended)

- Run on CPU

  1. Go to the insightface directory (i.e. `cd insightface`)

  2. Build the container.
      ```bash
      docker build -t face-analysis .  
      ```

  3. Run both containers.
      ```bash
      docker run -it --rm -p 10001:10001 video2frames 
      docker run -it --rm -p 10002:10002 face-analysis
      ```

- Run on GPU

  1. Go to the insightface directory (i.e. `cd insightface`)

  2. Build the container.
      ```bash
      docker build -f Dockerfile-cuda11 -t face-analysis-cuda .  
      ```

  3. Run both containers.
      ```bash
      docker run -it --rm -p 10001:10001 video2frames 
      docker run -it --rm -p 10002:10002 --gpus all face-analysis-cuda
      ```

### Client-side

1. Go to the insightface directory (i.e. `cd insightface`)

1. Install the requirements.
    ```bash
    pip3 install -r requirements-client.txt
    ```

2. Run the client in python. See `client.py` for the full code.