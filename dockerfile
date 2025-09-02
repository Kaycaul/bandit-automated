FROM python:slim
RUN apt-get -y update && \ 
    apt-get -y upgrade && \
    apt-get -y install xxd bzip2 sshpass

WORKDIR /bandit
RUN mkdir -p cache

COPY requirements.txt .
ENV VENV=/opt/venv
ENV PATH="$VENV/bin:$PATH"
RUN python3 -m venv $VENV && pip install -r requirements.txt

COPY . .
ENTRYPOINT ["python3", "-u", "src/main.py"]
