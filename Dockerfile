FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

MAINTAINER Sebastian Ramirez <tiangolo@gmail.com>

# Add app configuration to Nginx
COPY nginx.conf /etc/nginx/conf.d/

# Add requirements and install
ADD . /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt


# expose port(s)
EXPOSE 80


# Copy sample app
COPY ./app /app