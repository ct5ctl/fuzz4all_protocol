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

### Little things to implement
- setup chroot jail, at least have some scripts that can set it up
