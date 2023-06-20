# Fuzz Everything, Everywhere, All At Once

### Developer Setup

1. Create a virtual environment (Python 3.10) and install the requirements.
    ```shell
    conda create -n fuzz-everything python=3.10
    ```

2. Activate the environment.
    ```shell
    conda activate fuzz-everything
    ```

3. Install the requirements.
    ```shell
    pip install -r requirements.txt
    pre-commit install
    pip install -e .
    ```

Note: to save the conda environment, run `conda env export > environment.yml` and to load it, run `conda env create -f environment.yml`.

### Usage

1. To run the approach you need to use a `.env` file among those provided as template in the `envs` folder. The `.env` file contains the configuration for the approach.
Copy one of them in the root directory and rename it `.env`.

1. Change the global variable `SELECTED_OPTION` to match the environment you want to use. For example, if you want to use the environment `envs/.env.from_hf`, you need to set:
```python
...
SELECTED_OPTION = CACHESETUP.MODEL_CACHED_LOCALLY
...
```

1. Then, you can run the approach with the following command:

```shell
python fuzz.py \
--language cpp --num 10 --evaluate --otf --level 3 \
--template cpp_expected \
--bs 1 --temperature 1.0 --prompt_strategy 0 --use_hw
```



### Little things to implement
- setup chroot jail, at least have some scripts that can set it up
