HOWTO deploy on Linode
======================

###Build Ubuntu 12.10 on Linode and access the server
	$ ssh root@106.187.37.xxx
	# ssh to server
	# if encounter 'Host key verification failed', just delete ~/.ssh/known_hosts file

###Install Mysql
	$ apt-get update
	$ apt-get install mysql-server mysql-client

###Installing tools and dependencies
	$ apt-get install python-setuptools 
	$ easy_install pip 
	$ apt-get install git 
	$ apt-get install nginx 
	$ pip install supervisor 

###Config Git
	$ ssh-keygen -t rsa -C "3n1b.com@gmail.com"
	$ cat ~/.ssh/id_rsa.pub
	# copy and paste the RSA key to the Deploy keys setting
	$ git config --global user.name "3n1b.com"  
	$ git config --global user.email 3n1b.com@gmail.com  

###Make directories for your app
	$ mkdir /srv/www

###Pull in source code
	$ cd /srv/www/
	$ git clone git@github.com:gaolinjie/3n1b.com.git
	$ cd 3n1b.com

###Install web app required modules
	$ pip install -r requirements.txt

###Install python mysql
	$ easy_install -U distribute
	$ apt-get install libmysqld-dev libmysqlclient-dev
	$ pip install mysql-python
	$ apt-get install python-MySQLdb

###Install PIL
	$ apt-get build-dep python-imaging 
	$ apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
	$ ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
	$ ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
	$ ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib
	$ pip install -U PIL
	# pip install http://effbot.org/downloads/Imaging-1.1.7.tar.gz

###Create database and then execute sql file in dbstructure/
	$ mysql -u root -p
	mysql> CREATE DATABASE 3n1b;
	mysql> GRANT ALL PRIVILEGES ON 3n1b.* TO '3n1b'@'localhost' IDENTIFIED BY '3n1b';
	mysql> exit
	$ mysql -u 3n1b -p --database=3n1b < dbstructure/3n1b.sql
	$ mysql -u 3n1b -p --database=3n1b < dbstructure/node.sql
	$ mysql -u 3n1b -p --database=3n1b < dbstructure/college.sql
	$ mysql -u 3n1b -p --database=3n1b < dbstructure/plane.sql
	$ mysql -u 3n1b -p --database=3n1b < dbstructure/province.sql
	$ mysql -u 3n1b -p --database=3n1b < dbstructure/interest.sql
	$ mysql -u 3n1b -p --database=3n1b < dbstructure/follow.sql
	$ mysql -u 3n1b -p --database=3n1b < dbstructure/message.sql

###Create symbolic links to conf files
	$ cd /etc/nginx 
	$ rm nginx.conf
	$ ln -s /srv/www/3n1b.com/conf/nginx.conf nginx.conf 
	$ cd
	$ ln -s /srv/www/3n1b.com/conf/supervisord.conf supervisord.conf  

###Create nginx user
	$ adduser --system --no-create-home --disabled-login --disabled-password --group nginx 

###Create a logs directory:
	$ mkdir ~/logs 

###Start Supervisor and Nginx
	$ supervisord
	$ /etc/init.d/nginx start

###Visit your public IP address and enjoy!

###Update your web app
	$ cd /srv/www/3n1b.com
	$ git pull
