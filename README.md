# autogosling-tool

This is the code repository for autogosling webtool, consisting of the flask backend, frontend and model.


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

- [@mnqng](https://www.github.com/mnqng)


## Features


    
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


## Roadmap


## License

[MIT](https://choosealicense.com/licenses/mit/)
