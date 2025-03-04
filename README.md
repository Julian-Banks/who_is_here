# who_is_here
A library to scan your local network and display a list of people present on a simple web interface with a first and last seen. 

A Flask app running on a WSGI server using built-in HTTP capabilities.  

## Enviornment
Running on a Raspberry Pi 5. 
Debian version: 12 (bookworm), 64-bit

## Getting started

Clone the repo onto your Pi: [Git Docs for cloning](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

Create your Python Virtual environment:
$ python -m venv venv
Activate it:
$ source venv/bin/activate \

Install uWSGI: \
pip install uwsgi \

Quick start: \
This should get the app up and running on your local network. Access it from any other device by going to PIs_IP_ADDRESS:8000. \
$ uwsgi --http 0.0.0.0:8000 --master wsgi:app 

Getting the Webserver up and running on startup and crash:
To do:





## References:

[Flask Documentation](https://flask.palletsprojects.com/en/stable/)
[uWSGI Documentation](https://flask.palletsprojects.com/en/stable/deploying/uwsgi/)
Not currently used for Reverse Proxy: [Nginx with uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/Nginx.html)
