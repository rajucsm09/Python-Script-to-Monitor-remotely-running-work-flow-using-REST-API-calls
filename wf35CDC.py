#!/usr/bin/python

'''
Oracle Corp Sep, 2018
'''

import base64
import urllib2
import time
import json
import os, subprocess, socket, sys
from email.mime.text import MIMEText

def statusWF35():
    
    start_time = time.time()

    ###Credential Encoding###
    user = 'dataloading'
    passwd = '0at9i0!6l%Tt'
    base64string = base64.encodestring('%s:%s' % (user, passwd))[:-1]

    ###URI & Header details - Configurable###
    url=r'https://datainternalservice1-datainternaldomain1.data.em2.oraclecloud.com/data/admin/curator/workflowinstance/1242/stepdetails' 
    req=urllib2.Request(url)
    req.add_header("Authorization", "Basic %s" % base64string)
   
    ###EMail recipient###
    emailrecipients = "raju.borkakoty@oracle.com, siddharth.mohapatra@oracle.com, rammohan.patel@oracle.com"
    #outfile = 'wfOut.txt'

    ###REST call triggering and response parsing###
    content = urllib2.urlopen(req)
    jsonstring = content.read()
    try:
        parsedjson = jsonstring.split("\n")[-1]
        data = json.loads(parsedjson)
    except ValueError:
        print "Failed to parse the json file"
    
    ###Get Status and Write to File###
    with open('outfile.txt','a+') as f:
        wfStatus = data["currentStatus"]
        print "Current status of the WF35 in CDC:", wfStatus
        f.write('Current Status of Wf35:\t' + wfStatus)

        wfStepDetails = data["instanceSteps"]
        prettyStepDetails = json.dumps(wfStepDetails, sort_keys = True, indent = 6)
        
        fp = open("json.txt", 'w')
        fp.write(prettyStepDetails)
        
        f.write("\n\n\n")
        f.write("Progress Details of the WF35 in CDC:")
        
        status = os.popen("head -12 json.txt | grep -w 'status' | tr -d '\"'").read()
        f.write("\n\n")
        f.write(status)
        print status.strip()
        statusDetail = os.popen("head -12 json.txt | grep -w 'statusDetail' | tr -d '\"'").read()
        f.write(statusDetail)
        print statusDetail.strip()
        stepDescription = os.popen("head -12 json.txt | grep -w 'stepDescription'| tr -d '\"'").read()
        f.write(stepDescription)
        print stepDescription.strip()
        stepName = os.popen("head -12 json.txt | grep -w 'stepName'| tr -d '\"'").read()
        f.write(stepName)
        print stepName.strip()
        startTime = os.popen("head -12 json.txt | grep -w 'startTime' | tr -d '\"'").read()
        f.write(startTime)
        print startTime.strip()
        endTime = os.popen("head -12 json.txt | grep -w 'endTime' | tr -d '\"'").read()
        f.write(endTime)
        print endTime.strip()
        workflowInstanceId = os.popen("head -12 json.txt | grep -w 'workflowInstanceId' | tr -d '\"'").read().strip()
        f.write(workflowInstanceId)
        print workflowInstanceId.strip()
        fp.close()

    ###Send EMails###
    emailcmd = 'mail ' + '-s' + 'WF35\ Current\ Status\ in\ CDC\ Z12\ @ $(date)' + ' raju.borkakoty@oracle.com' + '<' + 'outfile.txt'
    sendmail = subprocess.Popen(emailcmd, shell=True)
    #time.sleep(5)
    #os.remove("outfile.txt")
    
    print "--- Time taken to check WF35 status is %s seconds ---" % (time.time() - start_time)

if __name__ == '__main__':
    p1 = statusWF35()
