#!/bin/bash
echo Frontend Deployment
cd /path/to/frontend
# Optional
# git pull origin master
npm install
npm run build
rm -rf /path/to/webroot
cp -r ./dist/* /path/to/webroot
echo Done.
exit