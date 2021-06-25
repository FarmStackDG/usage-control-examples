#!/bin/bash
import os
import subprocess
import sys

def start_setup():

    python_version = None
    pip_version = None
    # get os
    os_name = sys.platform
    print("os is %s" % (os_name))
    if os_name.startswith("win"):
        raise Exception("Try on linux system")
    else:
        try:
            python_version = subprocess.check_output(["python3", "-V"]).decode("utf-8")
        except:
            python_version = ""
        if python_version.startswith('Python'):
            python_version = "python3"
            pip_version = "pip3"
        else:
            try:
                python_version = subprocess.check_output(["python", "-V"]).decode("utf-8")
            except:
                print("No python found please install Python3.5 or greater")
            if python_version.startswith('Python 3'):
                python_version = "python"
            else:
                raise Exception("Required Python 3, found %s" % (sys.version_info))
    
    print("Proceeding with python - %s and pip - %s" % (python_version, pip_version))
    
    # install virtualenv
    subprocess.call(["%s" % (pip_version), "install", "virtualenv"])

    init_command = "%s -m venv venv" % (python_version)

    if not os_name.startswith('win'):
        activator_string = '''source venv/bin/activate ;'''
    
    requirements = [" --upgrade pip","bcrypt", "certifi", "cffi", 
                    "chardet", "cryptography", "Django==2.2", "python_on_whales",
                    "django-rest-swagger==2.2.0", "djangorestframework==3.12.4", 
                    "idna==2.10", "paramiko==2.7.2", "pycparser", 
                    "PyNaCl", "pytz", "PyYAML", "requests", "six", 
                    "sqlparse", "uritemplate==3.0.1", "urllib3==1.26.4", 
                    "django-cors-headers"]

    subprocess.call(["pwd"])
    print("path is above")
    
    os.system(init_command)

    for req in requirements:
        if not os_name.startswith('win'):
            activator_string += "%s install %s;" % (pip_version, req)
    
    os.system(activator_string)

    #start server
    if not os.name.startswith('win'):
        os.system("source venv/bin/activate;python connector/manage.py makemigrations;python connector/manage.py migrate;python connector/manage.py runserver 127.0.0.1:8000;")

if __name__ == "__main__":
    start_setup()