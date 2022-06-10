FROM continuumio/miniconda3
WORKDIR TRCLab/ICH
COPY requirements.txt .
RUN pip install -r requirements.txt
