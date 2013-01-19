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
	$ pip install tornado 
	$ apt-get install git 
	$ apt-get install nginx 
	$ pip install supervisor 

###Make directories for your app:
	$ mkdir /srv/www

###Pull in source code:
	$ cd /srv/www/
	$ git clone git@github.com:gaolinjie/3n1b.com.git

###Create symbolic links to conf files:
	$ cd /etc/nginx 
	$ rm nginx.conf
	$ ln -s /srv/www/3n1b.com/conf/nginx.conf nginx.conf 
	$ cd
	$ ln -s /srv/www/3n1b.com/conf/supervisord.conf supervisord.conf  

###Create nginx user:
	$ adduser --system --no-create-home --disabled-login --disabled-password --group nginx 

###Create a logs directory:
	$ mkdir ~/logs 

###Start Supervisor and Nginx:
	$ supervisord
	$ /etc/init.d/nginx start

###Visit your public IP address.

###Update your web app:
	$ cd /srv/www/3n1b.com
	$ git pull
