# AutoGosling: Automatic Interpretation and Generation of Genomic Visualizations using on Deep Learning

AutoGosling consists of an end-to-end pipeline that automatically interprets genomic visualization images, extracts visual encoding and view layouts, and generates Gosling (http://gosling-lang.org) visualization specifications that can be used to create similar interactive visualization for users’ own data.

This is the code repository for autogosling's webtool, consisting of the flask backend, frontend and model.

## Dataset

The script to generate the dataset to train the model is found [here](https://github.com/wangqianwen0418/gosling-boxes). The preprocessed dataset is available on [Harvard Dataverse](https://dataverse.harvard.edu/).

## Run Locally

Clone the project

```bash
  git clone https://github.com/autogosling/autogosling-tool
```

Go to the project directory

```bash
  cd autogosling-tool
```

Create a conda environment using the following command:

```bash
  conda env create -f myenv.yml
  conda activate autogosling
```

Run any file

```bash
  python main.py
```

Note: if you add any packages to the conda environment: run (if you are on Mac or Linux)
```bash
conda env export | grep -v "^prefix: " > myenv.yml
```
If you are on Windows, run 
```bash
conda env export -f myenv.yml
```
and manually remove the "prefix:" line

## Authors

- [@mnqng](https://www.github.com/mnqng)/[@mq-liang](https://github.com/mq-liang)
- [@katrina-liu](https://github.com/katrina-liu)
- [@wangqianwen0418](https://github.com/wangqianwen0418)
- [@ngehlenborg](https://github.com/ngehlenborg)

## Roadmap


## License

[MIT](https://choosealicense.com/licenses/mit/)
