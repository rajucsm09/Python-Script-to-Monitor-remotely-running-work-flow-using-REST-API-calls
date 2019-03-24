# Python-Script-to-Monitor-remotely-running-work-flow-using-REST-API-calls


Here, this python script monitors a production workflow using REST API calls (using urllib due to compatibility, can be use requests as well if supported),
And, send timely email alert towards the completion of the workflow.

Triggering of script can be done from Jenkins and cron job. Disable the job in jenkins when your workflow is not running.
