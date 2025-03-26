FROM python:3.8.6-slim
ENV PYTHONIOENCODING utf-8

# install gcc to be able to build packages - e.g. required by regex, dateparser, also required for pandas
RUN apt-get update && apt-get install -y build-essential

RUN pip install --upgrade pip

RUN pip install flake8

# Copy and install requirements first to leverage Docker cache
COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

# Copy the rest of the code
COPY . /code/

WORKDIR /code/

CMD ["python", "-u", "/code/src/component.py"]
