#postgresql and pgadmin 4 should be installed first .
#use the vscode terminal to input the following command lines


#use these 2 commands to create and activate the virtual environment
python -m venv venv
.\venv\Scripts\Activate



#use this command to install the neccessary things 
pip install -r requirements.txt



#use this command to enter into the postgresql. when prompted for password, Enter the password for postgresql application . in my case "postgres".
psql -U postgres




#run these commands inside the postgresql 
CREATE DATABASE seagrass_db;
CREATE USER seagrass_admin WITH PASSWORD 'wasana13'; 
ALTER ROLE seagrass_admin SET client_encoding TO 'utf8'; 
ALTER ROLE seagrass_admin SET default_transaction_isolation TO 'read committed'; 
ALTER ROLE seagrass_admin SET timezone TO 'UTC'; 
ALTER USER seagrass_admin WITH PASSWORD 'wasana13';
GRANT ALL PRIVILEGES ON DATABASE seagrass_db TO seagrass_admin; 
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO seagrass_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO seagrass_admin;
ALTER ROLE seagrass_admin 
  WITH 
    CREATEDB        
    CREATEROLE      
    REPLICATION     
    BYPASSRLS       
    LOGIN;         
ALTER USER seagrass_admin WITH SUPERUSER;
\q




#use this command to enter into seagrass_admin account, when prompted for password , enter "wasana13" as the password.
psql -U seagrass_admin -d seagrass_db 




#use this command line to restore the database backup. replace the path to database with your database backup file. this is my path 
#do not import this backup unless necessary. this will have conflicts in the future when doing migrations. 
#if you can , make your own migrations.
pg_restore -U seagrass_admin -d seagrass_db -v "D:\Project 2\Seagrass_SriLanka-Backend\seagrass_db.backup"
