#!/bin/bash
echo Backend Deployment
# cd /path/to/frontend
# git pull origin master
cd /path/to/backend
rm -rf `ls /path/to/backend/deployment | grep -v "config.yml"`
cp -r /path/to/backend/* /path/to/backend/deployment
echo Done.
exit