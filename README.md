Web app created by following a tutorial in Head First Python.

# Summary

This project started with the tutorial using Flask from Head First Python with the final outcome saved as vsearch4web.py. I then created vsearch4web_extended.py to add more functionality to the existing web app.

The web app is designed to search for given letters in a given phrase and report back which letters were found. In the extended version, only signed-in users can see the contents of the log. The resutls, users and passwords are stored with MySQL.



# Set up

```
git clone https://github.com/Jess-G95/Head-First-Web-App
cd Head-First-Web-App/
python vsearch4web_extended.py

browse to http://127.0.0.1:5000/
```

# Requirements

* Python 3
* Flask
* MySQL


# Ubuntu set up

```
sudo apt install git
git clone https://github.com/Jess-G95/Head-First-Web-App
cd Head-First-Web-App/
sudo apt install python3-pip
pip install flask
sudo apt install mysql-server
sudo apt install libmysqlclient-dev
pip install mysql-connector-python
python vsearch4web_extended.py
```

# MySQL set up

```
sudo mysql
create database vsearchlogDB;
CREATE USER 'vsearch'@'localhost' IDENTIFIED BY 'vsearchpasswd';
GRANT ALL PRIVILEGES ON * . * TO 'vsearch'@'localhost';
FLUSH PRIVILEGES;
exit # exit and log in with the below
sudo mysql -u vsearch -p vsearchlogDB # use vsearchpasswd when prompted for password
create table log (id int auto_increment primary key, ts timestamp default current_timestamp, phrase varchar(128) not null, letters varchar(32) not null, ip varchar(16) not null, browser_string varchar(256) not null, results varchar(64) not null);
describe log; # confirm table has been created and is correct
CREATE TABLE users (username varchar(255), password varchar(255));
INSERT INTO users VALUES ('me', 'testing'); # optional
mysql> SELECT * FROM users; # view all entries in users table
exit

```
