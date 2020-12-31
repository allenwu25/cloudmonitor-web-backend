FROM python:3.7
WORKDIR /app
ADD . /app

# Install dependencies for PyODBC
RUN apt-get update \
 && apt-get install --reinstall build-essential -y \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install tdsodbc -y \
 && apt-get install gcc -y \
 && apt-get install musl-dev -y \
 && apt-get install postgresql-server-dev-11 -y \
 && apt-get clean -y


# Install requirements
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 5000

ENV NAME OpentoAll

CMD ["python", "app.py"]
