
# autogosling-model
This is the code repository for any modeling required for autogosling.

## 1. Data processing and utilities
- `a0_config.py`: Config file that specifies dataset train-test-valid split and input and output folders
- `a1_generate_split.py`: Generates train-test-valid datasets
- `a2_generate_classlist.py`: 
- `a3_generate_yolov7.py`: 
- `u0_display_image.py`: Utility script to debug images generated from a3_generate_yolov7.py.
- `u1_test_labels.py`: Utility script to count the number of labels generated from a3_generate_yolov7.py
## 2. Model
- `yolov7_trained_model.ipynb`:
- `yolov7_demo.ipynb`:

## Authors

- [@mnqng](https://www.github.com/mnqng)

## Notes


## Features

- To do

## Installation

    
## Run Locally

Go to the project directory

```bash
  cd model
```

Download Yolo-v4 weights through the following command:
```bash
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
```

Run any file

```bash
  python main.py
```


## Roadmap


## License

[MIT](https://choosealicense.com/licenses/mit/)

