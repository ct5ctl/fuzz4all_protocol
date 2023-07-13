## Usage
To compute the coverage of the Qiskit project, run the following command from the root of the repository:
```bash
python tools/coverage/QISKIT/collect_coverage.py \
    --folder=Results/qiskit_basic \
    --output=Results/qiskit_basic/coverage \
    --every-n-files=15
```
The script will generate a coverage report in the `Results/qiskit_basic/coverage` directory. The reports are generated using the `coverage.py` tool in `xml` format compatible with Cobertura.

The input folder is the folder with `*.fuzz` files and the output is where you will find all the single file results and also the csv with the final coverage.

The coverage is computed in a cumulative fashion, and you can choose to check the coverage every n files instead of every new file to speed up, via `every-n-files` argument.


