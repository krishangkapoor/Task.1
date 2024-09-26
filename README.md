A simple Todo application built with Django that allows the user to create a new task, delete a task, mark a task as done, filter the list of tasks by their completion status, 
and send an email notification when a task is created (both from the API and Django Admin). 

Requirements:
Installation of Docker

How to run the application:
Step 1. Clone the repository or Download the zip file from this GitHub page by clicking code and then download zip.
Step 2. Open the command prompt and create an env.  file in the root directory of the project. 
Step 3. Use the below variables for email configuration. Change the configurations to your actual configurations. You can make your app password by going to Gmail security and 
enabling the 2-step verification. Then go to app passwords and create one.  
EMAIL_HOST_USER=your_gmail@gmail.com 
EMAIL_HOST_PASSWORD=your_app_password
You can also do the same by going to the settings.py and changing the credentials to your own.
Step 4. Build the docker images and run all the containers (Django app, PostgreSQL, Redis, and Celery) by applying the following command on your cmd. 
docker-compose up --build
Step 5. Access the application at http://localhost:8000/admin/ in your browser.
Step 6. To access the admin you can make a superuser by using the following command in your cmd.
docker-compose exec web python manage.py createsuperuser
Step 7. To stop the application use the following command in your cmd.
docker-compose down
