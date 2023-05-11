# AutoGosling: Enabling Multimodal User Interactions for Genomics Visualization Creation

AutoGosling consists of an end-to-end pipeline that automatically interprets genomic visualization images, extracts visual encoding and view layouts, and generates Gosling (http://gosling-lang.org) visualization specifications that can be used to create similar interactive visualization for users’ own data.

This is the code repository for autogosling's webtool, consisting of the flask backend, frontend and model.


## Run Locally

### GitHub Repository

1. Clone this repository

```bash
  git clone https://github.com/autogosling/autogosling-tool.git
  cd autogosling-tool
```

2. Go to the flask folder and download AutoGosling Yolo v7 pre-trained weights [here](https://drive.google.com/file/d/1x_e4V9LDgjsZhMWCnONbiQXK4Zfw6t27/view?usp=share_link):

```bash
  cd flask
  wget -O best.onnx https://drive.google.com/file/d/1x_e4V9LDgjsZhMWCnONbiQXK4Zfw6t27/view?usp=share_link
```

3. Get a GPT API key [here](https://platform.openai.com/account/api-keys)

After getting the key, store in a .env file at project root directory.

```.env
#.env
OPENAI_API_KEY=<paste your key here>
```

4. Create a conda environment
```bash
  conda create --name autogosling --file requirements.txt
  conda activate autogosling
```

5. Start the app with script at project root

```bash
chmod 777 autogosling.sh
./autogosling.sh
```
The front end of the app automatically runs on port 3000 with the backend on port 7777.

### Python Web-App Tar

1. Download the AutoGosling Python web-app [here](https://drive.google.com/file/d/1mAjrZMpZe2nAPcGiRd9KpguJvzWLKvGm/view?usp=share_link).

```bash
  wget -O autogosling.tar.gz  https://drive.google.com/file/d/1mAjrZMpZe2nAPcGiRd9KpguJvzWLKvGm/view?usp=share_link
  tar -xvf autogosling.tar.gz
```

2. Go to the project directory

```bash
  cd autogosling
```

3. Create a conda environment

```bash
  conda create --name autogosling --file requirements.txt
  conda activate autogosling
```
4. Download AutoGosling Yolo v7 pre-trained weights [here](https://drive.google.com/file/d/1x_e4V9LDgjsZhMWCnONbiQXK4Zfw6t27/view?usp=share_link):

```bash
  wget -O best.onnx https://drive.google.com/file/d/1x_e4V9LDgjsZhMWCnONbiQXK4Zfw6t27/view?usp=share_link
```


4. Get a GPT API key [here](https://platform.openai.com/account/api-keys)

After getting the key, store in a .env file at project root directory.

```.env
#.env
OPENAI_API_KEY=<paste your key here>
```

5. Run the app:

```bash
  python main.py
```

The app automatically runs on port 7777.

## Supplementary Files

1. [Video Demo](https://drive.google.com/file/d/1KfC3IATrGmj8feMbF09oMJc6NXNQikOd/view?usp=share_link)
2. [AutoGosling Yolov7 Training Dataset Information](https://docs.google.com/document/d/1Zd55MC6InFuckOTaCiU5Wsq8zo1G2UTcj8m-n2vY_VE/edit?usp=share_link)
3. [AutoGosling GPT-3.5 Finetuning Messages](https://docs.google.com/document/d/1Eu0zP-56RxGRXsYn2OT19s9sg-2oeLckn68200RmaX0/edit?usp=share_link)

## Team

- [@mnqng](https://www.github.com/mnqng)/[@mq-liang](https://github.com/mq-liang)
- [@katrina-liu](https://github.com/katrina-liu)
- [@wangqianwen0418](https://github.com/wangqianwen0418)
- [@ngehlenborg](https://github.com/ngehlenborg)

## Roadmap

## License

[MIT](https://choosealicense.com/licenses/mit/)
