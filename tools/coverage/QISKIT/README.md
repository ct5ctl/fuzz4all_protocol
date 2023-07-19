## Usage

Build the docker image (if not already done before):
```shell
docker build -t qiskit-driver .
```

Enter in the image mounting the current directory (the root of the repository):
```shell
docker run -it --rm -v $(pwd):/home qiskit-driver bash
```

To compute the coverage of the Qiskit project, run the two following commands:
```bash
# [IN THE DOCKER CONTAINER]
cd /home
python -m tools.coverage.QISKIT.collect_coverage --target-folder Results/qiskit/v02_basic --output-folder Results/qiskit/v02_basic/cumulative_coverage -n 100 --timeout 10 --file-extension .fuzz
```
The input folder is the folder with `*.fuzz` files and in the output folder you will find a csv with the final cumulative coverage.
Note that the coverage is aggregated every `-n` files, and the files are expected to be in the format `1.fuzz`, `2.fuzz`, etc.
In this example, it will generate a series coverage reports in the `Results/v02_basic/cumulative_coverage` directory. The reports are generated using the `coverage.py` tool in `xml` format compatible with Cobertura.
Moreover a `cumulative_coverage.csv` file is generated in the output folder, which contains the cumulative coverage of the campaign, together with a diagram image `cumulative_coverage.png` showing the coverage trend.

Note that by default we track the coverage on all the packages in the `site-packages` folder starting with `qiskit`, if you want to change this behavior you can do that by setting the `--packages-to-track` argument, for example:
```bash
# [IN THE DOCKER CONTAINER]
python -m tools.coverage.QISKIT.collect_coverage --target-folder Results/qiskit/v02_basic --output-folder Results/qiskit/v02_basic/cumulative_coverage -n 100 --timeout 10 --file-extension .fuzz --packages-to-track qiskit_aer --packages-to-track qiskit_ibmq_provider-0.20.2.dist-info
```






