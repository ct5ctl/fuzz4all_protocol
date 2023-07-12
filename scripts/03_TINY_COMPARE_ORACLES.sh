#/bin/sh

# This script runs a fuzzing session on the Qiskit backend.

# get conda path
CONDA_PATH=$(which conda)
# replace condabin/conda with bin/activate
CONDA_PATH=${CONDA_PATH%/condabin/conda}
CONDA_PATH=${CONDA_PATH%/bin/conda}
CONDA_PATH=${CONDA_PATH}/bin/activate

echo "Conda path: $CONDA_PATH"

# Activate the conda environment
source $CONDA_PATH fuzz-everything

# Run python and check the version
python --version

# print the filename
filename=$(basename -- "$0")
echo "Running $filename"


# Run the fuzzing sessions

# current directory
echo "Current directory: $(pwd)"

echo "Running crash oracle session"
screen -d -S qiskit_crash -m python FuzzAll/fuzz.py --config=config/v02_qiskit_untargetted_crash.yaml main_with_config

echo "Running metamorphic oracle session"
screen -d -S qiskit_meta -m python FuzzAll/fuzz.py --config=config/v03_qiskit_untargetted_metamorphic.yaml main_with_config
