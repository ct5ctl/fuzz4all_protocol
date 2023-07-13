#/bin/sh

# This scrip creates a safe environment for running generated Python code.

# Build the docker image
docker build -t qiskit-driver .
