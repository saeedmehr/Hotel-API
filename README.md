# Hotel-API
Case: Integrating third parties
integrating third parties in a piece of software. These third parties expose data or API’s which are used in the services that we offer our clients.
In this case, to keep the exercise small, an application has to be built that imports CSV hotel data. Of course CSV data is flat, while in the case of data models in Django one wants to make use of relations. So during the import of the data those relations have to be restored.
Then in the end a small front- end application has to be built that allows users to lookup hotel data. 

## Run server 
To run the website follow the steps mentioned below:
1. Install 'python3' from [Python Website]
2. To start with, you should install 'virtualenv' (for installation guide visit [virtualenv]) 
3. Create a virtual environment in the project directory using the following command :
             virtualenv venv
4. Activate your environment using this command :
             source venv/bin/activate
5. It’s time to install needed libraries : (including Django itself)
             pip install -r requirements.txt
6. Now we need to make the database. Use the two command bellow to make schema and the database
             python manage.py makemigrations
             python manage.py migrate
7. You should create a superuser to manage the website. You should provide a username, password, and an email (as it’s for a demonstration purpose email is not necessary)
             python manage.py createsuperuser
8. Now you can run the server using this command
             Python manage.py runserver
9. Finally, you need to open your browser and go to “127.0.0.1.:8080”
Keep in mind as it’s a proof-of-concept, the debugging mode is still on and you must turn it off in the real-world deployment. Furthermore, you should take care of SECERT_KEY in production.

## Run Tests
To run the unit tests, go through steps 1-5 from the above instruction (if you haven’t done it yet) and run ​py.test​ in the your terminal. This command will run every provided unit tests and shows the results of its success or failure.
In order to see the unit test coverage, you can open ​index.html​ file in ​htmlcov​ directory located in the project directory via your browser. It’s will show the percentage of the unit test coverage per file.

## Crontab daily import automation
For importing data over authenticated http protocol on daily basis, do the following steps:
1. open your terminal and run the this command
crontab -e
2. place this rule in provided text file and save it
             0 1 * * * python <PATH_TO_PROJECT>/manage.py checkurl
  
By placing the above rule the system will automatically import data from saved URLs on daily basis at 1 a.m.
Make sure you have changed ​<PATH_TO_PROJECT>​ to the correct path.
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
