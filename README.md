## Getting Started

# weather-app-django-on-ec2

Follow these 2 step to up the backend server:

First create .env in the root directory and paste your api key from [openweathermap.org](openweathermap.org) with contents of .env.template

and install libraries with the following command:
```bash
pip install -r requirements
```

Second change directory to the file settings.py:
```bash
cd weather_project
```

and run the following command:
```bash
python manage.py runserver
```