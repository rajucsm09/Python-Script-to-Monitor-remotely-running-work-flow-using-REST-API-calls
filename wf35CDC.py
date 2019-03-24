#!/usr/bin/python

'''
Sep, 2018
Written By Raju B
'''

import base64
import urllib2
import time
import json


def statusWF():
    
    start_time = time.time()

    ###Credential Encoding###
    user = 'username'
    passwd = 'password'
    base64string = base64.encodestring('%s:%s' % (user, passwd))[:-1]

    ###URI & Header details - Configurable###
    url=r'https://your-production-url.com/<your-rest-uri-path>/id/<endpoint>' 
    req=urllib2.Request(url)
    req.add_header("Authorization", "Basic %s" % base64string)
   
    ###EMail recipient###
    emailrecipients = "abc@abc.com, xyz@xyz.com, pqr@pqr.com"
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
        print "Current status of the WF in Datacenter XYZ:", wfStatus
        f.write('Current Status of WF:\t' + wfStatus)

        wfStepDetails = data["instanceSteps"]
        prettyStepDetails = json.dumps(wfStepDetails, sort_keys = True, indent = 6)
        
        fp = open("json.txt", 'w')
        fp.write(prettyStepDetails)
        
        f.write("\n\n\n")
        f.write("Progress Details of the WF in Datacenter XYZ:")
        
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
    emailcmd = 'mail ' + '-s' + 'WF\ Current\ Status\ in\ DatacenterXYZ\ ZoneID\ @ $(date)' + ' xyz@xyz.com' + '<' + 'outfile.txt'
    sendmail = subprocess.Popen(emailcmd, shell=True)
    time.sleep(5)
    os.remove("outfile.txt")
    
    print "--- Time taken to check WF status is %s seconds ---" % (time.time() - start_time)

if __name__ == '__main__':
    p1 = statusWF()
