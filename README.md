# Test-Task
Simple newspaper web application built with Django

# Requirements
```
- Docker
- Docker Compose
```

# Installation

```
$ git clone https://github.com/Allirey/test_task212
$ cd test_task212/
$ sudo docker-compose up --build 
```

# Usage

- The Django server: http://localhost:8000/

# To run locally
Register at [Sendgrid](https://sendgrid.com/) and get your API key ([details](https://app.sendgrid.com/guide/integrate/langs/smtp))

Set up [broker](https://docs.celeryproject.org/en/latest/getting-started/brokers/) you like for celery to use

Configure required environment variables:
+ EMAIL_HOST_PASSWORD (get via sendgrid)


