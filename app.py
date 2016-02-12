#!/usr/local/bin/python2.7

import json
import glob
import ansible.runner
from  ansible.inventory import Inventory
from flask import Flask, render_template, request, make_response

app = Flask(__name__)

ec2_inventory_path = '/path/env/'

## environment like dev,uat etc
envs = [ i.split('/')[3] for i in glob.glob( ec2_inventory_path + '*/ec2.py') ]


@app.route("/")
def main():
   return render_template("index.html")


@app.route("/ip")
def get_ip():
     tag = "tag_Name_" + request.args.get('host')
     env = request.args.get('env')
     eip = request.args.get('eip').capitalize() if 'eip' in request.url else False
     inventory_file = ec2_inventory_path + env + "/ec2.py"

     if env not in envs:
        return make_response(json.dumps({'error': env + ' Environment not found'}),400)

     inv = Inventory(inventory_file)
     if len(inv.get_hosts(tag)) == 0:
        msg = "No Host match for {} in {}".format(request.args.get('host'), env)
        return make_response(json.dumps({'error': msg}),400) 

     if eip == False:
         #print "Checking IP of {} for Env: {}".format(tag,env)
         ipaddr = ','.join([ ip.name for ip in inv.get_hosts(tag)])
     else:
         #print "Checking EIP of {} for Env: {}".format(tag,env)
         data = ansible.runner.Runner(
                        module_name='debug', 
                        pattern=tag, 
                        inventory = inv, 
                        transport = 'local', 
                        module_args="var=hostvars['{{ inventory_hostname }}']['ec2_ip_address']"
         ).run()
         element = data['contacted'].keys()
         ipaddr = ','.join([ ''.join(data['contacted'][e]['var'].values()) for e in element])
         if len(ipaddr) == 0:
            msg = "No EIP Found for {} in {}".format(request.args.get('host'), env)
            return make_response(json.dumps({'error': msg}),400) 
 
     return  ipaddr
