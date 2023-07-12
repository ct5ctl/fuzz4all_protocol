#/bin/sh

# This script from the repo directory. with: ./scripts/01_FUZZ_QISKIT.sh

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

# Run the fuzzing session
python FuzzAll/fuzz.py --config=config/v02_qiskit_untargetted_crash.yaml main_with_config
