# Use an official Python runtime as a parent image
FROM python:3.10.12

LABEL authors="elisha.joy@entri.me"

# Install system dependencies

RUN apt-get update && \
    apt-get -y install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0 vim git \
                       libpq-dev  

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file initially to leverage Docker cache
COPY requirements.txt .

# Install virtualenv and dependencies
RUN pip install -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy the application code
COPY . .

EXPOSE 8000

# Run Django app when the container launches
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn -b 0.0.0.0:8000 lunch_app.wsgi:application"]
