# Use an official Python runtime as the base image
FROM python:3.9.17-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Install wkhtmltopdf dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    fontconfig \
    libjpeg-dev \
    libpng-dev \
    libxrender1 \
    libx11-dev \
    xfonts-75dpi \
    xfonts-base \
    libxext6\
    curl

# Install wkhtmltopdf
RUN curl -LJO "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb" \
    && dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb \
    && apt-get -f install \
    && rm wkhtmltox_0.12.6-1.buster_amd64.deb

# Copy the requirements.txt file to the working directory
COPY script/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory to the working directory
COPY script/ .

# Create a directory for the output file
RUN mkdir /app/input
RUN mkdir /app/output

# Define the command to run your Python script
#CMD ["python", "dateScript.py"]
#CMD python script/dateScript.py && sleep 3600
CMD python script/dateScript.py

