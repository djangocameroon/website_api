# website_api

## Installation
1. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies  
```bash
pip3 install -r requirements.txt
```  

3. Setup a new postgres database
Assuming postgresql is installed in your computer, follow what's next:
   - ```bash
      # accessing the postgres CLI
      sudo -u postgres psql
      ```
   - ```bash
   
     -- Create a database
     CREATE DATABASE django_website_db;
     
     -- create a new user with the details below
     CREATE USER 'db_username' WITH ENCRYPTED PASSWORD 'password';
     -- Grant all priviledges
     GRANT ALL PRIVILEGES ON DATABASE django_website_db TO 'db_username'@'host';
       ```

    If postgreSQL is not installed in the computer, get to the tutorial [for Linux](https://www.cherryservers.com/blog/how-to-install-and-setup-postgresql-server-on-ubuntu-20-04) or [for Windows](https://www.microfocus.com/documentation/idol/IDOL_12_0/MediaServer/Guides/html/English/Content/Getting_Started/Configure/_TRN_Set_up_PostgreSQL.htm).

4. Copy the .env.example file to .env and fill in the values in the .env file.  
```bash
cp -r .env.example .env
```

5. Apply database migrations 
```bash
python3 manage.py migrate
```

6. Run the server
```bash
python3 manage.py runserver
```

## Contributing
Contributions are always welcome! If you have any bug reports, feature requests, or pull requests, please feel free to submit them.