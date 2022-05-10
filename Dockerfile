FROM continuumio/miniconda3
MAINTAINER S.W.-Chen (swchen357951@gmail.com)
WORKDIR TRCLab/ICH
COPY requirements.txt .
RUN pip install -r requirements.txt
