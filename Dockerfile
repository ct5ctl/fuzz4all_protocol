FROM continuumio/miniconda3
RUN conda create -n fuzz-everything python=3.10
RUN echo "source activate fuzz-everything" > ~/.bashrc
ENV PATH /opt/conda/envs/fuzz-everything/bin:$PATH
RUN pip install qiskit==0.43.1
RUN pip install coverage==7.2.7
RUN pip install click==8.1.4
RUN pip install rich==13.4.2
RUN pip install pandas==2.0.3
RUN pip install matplotlib==3.7.2

CMD ["python"]
