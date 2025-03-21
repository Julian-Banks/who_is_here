# who_is_here
A library to scan your local network and display a list of people present on a simple web interface with a first and last seen. 

A Flask app running on a WSGI server using built-in HTTP capabilities.  

## Environment
Running on a Raspberry Pi 5.  \
Debian version: 12 (bookworm), 64-bit

## Getting started

Clone the repo onto your Pi: [Git Docs for cloning](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

Create your Python Virtual environment: \
$ python -m venv venv \
Activate it: \
$ source venv/bin/activate 

Install uWSGI: \
pip install uwsgi 

Quick start: \
This should get the app up and running on your local network. Access it from any other device by going to PIs_IP_ADDRESS:8000. \
$ uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi:app \
(Note: I have not been able to get the uwsgi_config.ini file to work as expected)

Getting the Webserver up and running on startup and crash: \

Run this command to make the start_app.sh file executable \
$ chmod +x start_uwsgi.sh \ 
//Copy the service from the service_resources folder to the systemd system folder \
sudo cp start_app_service.service /etc/systemd/system \
//reload the daemon \
sudo systemctl daemon-reload \
// Enable the service \
sudo systemctl enable start_app_service \
//start the service \
sudo systemctl start start_app_service \


[Systemd](https://github.com/thagrol/Guides/blob/main/boot.pdf)





## References:

[Flask Documentation](https://flask.palletsprojects.com/en/stable/) \
[uWSGI Documentation](https://uwsgi-docs.readthedocs.io/en/latest/index.html#quickstarts) \
Not currently used for Reverse Proxy: [Nginx with uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/Nginx.html)
[Systemd](https://github.com/thagrol/Guides/blob/main/boot.pdf)
