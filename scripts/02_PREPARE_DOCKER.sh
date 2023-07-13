#/bin/sh

# This scrip creates a safe environment for running generated Python code.

# Move to repository root
cd ../

# Build the docker image
docker build -t qiskit-driver .
