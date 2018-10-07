# Chef Recommender

A simple problem recommendation system for CodeChef.

## Instructions to run locally

- Install Python and some dev tools for Python 
  - `$ sudo apt-get install python3-pip python-dev build-essential`
  - `$ apt install Python3.6`
  
- Then install **virtualenv** using pip3
  - `$ sudo pip3 install virtualenv`

- Now create a virtual environment 
  - `$ virtualenv venv --python=python3.6` you can use any name insted of **venv**

- Active your virtual environment 
  - `$ source venv/bin/activate`

- Install other requirements given in requirements.txt file
  - `$ pip install -r requirements.txt`

- Runserver
  - `$ python app.py`
  - `$ visit http://0.0.0.0:5000/`
