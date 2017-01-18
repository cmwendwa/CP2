[![Build Status](https://travis-ci.org/clementm916/CP2.svg?branch=develop)](https://travis-ci.org/clementm916/CP2[![Coverage Status](https://coveralls.io/repos/github/clementm916/CP2/badge.svg?branch=develop)](https://coveralls.io/github/clementm916/CP2?branch=develop)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Bucketlist API

Bucketlist API is a Restful API written in python. It let's you create a bucketlist to which you can add items of thing you wan to do and mark the as done once complete. To access this functionalities you have to register with the app and login to get a token which you use for authentication. 

## Getting Started

To get started you need to clone this github repo or download the zip file and unzip it in your directory of choice.
```
#cloning the repo
$ git clone https://github.com/clementm916/CP2.git
```
### Prerequisites
To run this program you need to have python installed and farmiliar with virtual environments. 
```
$ pip install virtualenv               #install virtualenv
$ virtualenv bucketlist-api            #create a virtual environment    
$ source bucketlist-api/bin/activate   #activating python environment

```

### Installing requirement

The application requires several dependencies to work. To install this run the command below. Make sure your environments are activated so as to install dependencies will be installed here.

```
$ cd CP2
$ pip install -r  requirements.txt
```

### Running
Now after this we run the server.
```
$ python manage.py runserver
```

Examples of how to consume the API

```
#adding a user
$ curl -d "username=imani&password=imani123" -X POST  http://127.0.0.1:5000/api/v1/auth/register
{
    "message": "User successfully added"
}

#loggin in a user
curl -d "username=imani&password=imani123" -X POST  http://127.0.0.1:5000/api/v1/auth/login
{
    "Authorization": "eyJpYXQiOjE0ODQ3NTk3ODQsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDg0NzYxNTg0fQ.eyJpZCI6M30.gFzqf3UhYc8C4ra1AbKsgDV5-pANKwxL4YPY02I-sQQ"
}

```

Creating a bucketlist.
```
$ curl -H "Authorization:Token eyJpYXQiOjE0ODQ3NTk3ODQsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDg0NzYxNTg0fQ.eyJpZCI6M30.gFzqf3UhYc8C4ra1AbKsgDV5-pANKwxL4YPY02I-sQQ" -d "name=shop" http://127.0.0.1:5000/api/v1/bucketlists/
{
    "successfully created: ": {
        "created_by": 3,
        "date_created": "Wed, 18 Jan 2017 17:19:51 -0000",
        "date_modified": "Wed, 18 Jan 2017 17:19:51 -0000",
        "id": 5,
        "items": [],
        "name": "shop"
    }
}
```
End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Running the tests ensures the code is not broken. Below are commands to do it
```
#run tests without coverage
$ nosetests
#run particular test file or folder
$ nosetstests <path to a given tests file or folder>
# run tests with coverage
$ nosetests tests/ --with-coverage --cover-package app
```







## Built With

* [Flask](http://www.flask.pocoo.org/) - The web framework used
* [Flask-restful](https://github.com/flask-restful/) - Rest framework used
Other dependencie can be found in the *requirements.txt*
## Authors

* **Clement Mwendwa** - *Initial work* - [Github](https://github.com/clementm916)



## License
The MIT License
Copyright (c) 2016 clement mwendwa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE




