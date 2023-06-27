FROM continuumio/miniconda3
RUN conda create -n fuzz-everything python=3.10
RUN echo "source activate fuzz-everything" > ~/.bashrc
ENV PATH /opt/conda/envs/fuzz-everything/bin:$PATH
RUN pip install qiskit==0.43.1

ENTRYPOINT ["python"]
