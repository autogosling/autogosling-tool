# AutoGosling: Automatic Interpretation and Generation of Genomic Visualizations using on Deep Learning

AutoGosling consists of an end-to-end pipeline that automatically interprets genomic visualization images, extracts visual encoding and view layouts, and generates Gosling (http://gosling-lang.org) visualization specifications that can be used to create similar interactive visualization for users’ own data.

This is the code repository for autogosling's webtool, consisting of the flask backend, frontend and model.

## Dataset

The script to generate the dataset to train the model is found [here](https://github.com/wangqianwen0418/gosling-boxes). The preprocessed dataset is available on [Harvard Dataverse](https://dataverse.harvard.edu/).

## Run Locally

1. Clone the project

```bash
  git clone https://github.com/autogosling/autogosling-tool
```

2. Go to the project directory

```bash
  cd autogosling-tool
```

3. Create a conda environment

```bash
  conda env create -f myenv.yml
  conda activate autogosling
```

4. Run the app (see [Flask folder](https://github.com/autogosling/autogosling-tool/tree/main/flask) and [React folder](https://github.com/autogosling/autogosling-tool/tree/main/frontend) for details):

```bash
  bash autogosling.sh
```

 **OR**

  Start the flask server and React app separately

  a) Start the flask server
  ```bash
    cd flask
    python main.py
  ```

  b) Start the React app
  ```bash
    cd frontend
    yarn start
  ```

  If working on a server, forward localhost:3000 to port 3000.

5. **Note**: if you add any packages to the conda environment: run (if you are on Mac or Linux)
```bash
conda env export | grep -v "^prefix: " > myenv.yml
```
If you are on Windows, run 
```bash
conda env export -f myenv.yml
```
and manually remove the "prefix:" line

## Team

- [@mnqng](https://www.github.com/mnqng)/[@mq-liang](https://github.com/mq-liang)
- [@katrina-liu](https://github.com/katrina-liu)
- [@wangqianwen0418](https://github.com/wangqianwen0418)
- [@ngehlenborg](https://github.com/ngehlenborg)

## Roadmap

## License

[MIT](https://choosealicense.com/licenses/mit/)
