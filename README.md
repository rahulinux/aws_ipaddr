## AWS Get IP

To get AWS EC2 IP, we need to configure ec2.py and ec2.ini i.e ansible dynamic inventory, but the problem here is we need to do this on every machine where we need to use IP address. instead of configuring aws keys on each nodes we have created one api server which will use exising ansible configuration 


#### Setup 

This service require following module to be install

````
pip install uWSGI==2.0.12
pip install virtualenv==13.1.2
````

Once you Install module, download service from Stash repo and run below command which will setup this application

````
mkdir /opt/
git clone https://github.com/rahulinux/aws_ipaddr
cd aws_ipaddr 
virtualenv env
source env/bin/activate
pip install -r requirement.txt
cp init_script /etc/init.d/aws_ipaddr
chmod +x /etc/init.d/aws_ipaddr
chkconfig --level 35 aws_ipaddr on 
````

##### Start service and test api calls 

````
/etc/init.d/aws_ipaddr restart
````

Check logs 
````
tail -f /var/log/aws_ipaddr.log
````

Test API call
````
curl -s  'http://server_ip:8000/ip?host=Web&env=UAT&eip=True'
````

It will return all Public IP of Web nodes. 

Note: all is based on AWS Name Tags, so whatever you mentioned in `host=Name` 
