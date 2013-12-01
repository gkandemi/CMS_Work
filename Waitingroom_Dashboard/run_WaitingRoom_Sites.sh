#!/bin/bash
# Script in acrontab t1
# 5,20,35,50 * * * * lxplus ssh vocms202 /afs/cern.ch/user/g/gkandemi/scratch0/Waitingroom_Dashboard/source_The_Run_File_WaitingRoom_Sites.sh &> /dev/null
# Script for Dashboard metric 153
# outputfile WaitingRoom_Sites.txt
# outputdir /afs/cern.ch/user/g/gkandemi/www/WFMon/ 

cd /afs/cern.ch/user/g/gkandemi/scratch0/Waitingroom_Dashboard

echo "exporting KEY and CERT"

#fixing access
export X509_USER_CERT=/data/certs/servicecert.pem
export X509_USER_KEY=/data/certs/servicekey.pem


# Email if things are running slowly
if [ -f scriptRunning.run ];
then
   echo "run_WaitingRoom_Sites.sh is already running. Will send an email to the admin."
   # script to send simple email
   # email subject
   SUBJECT="[Monitoring] load WaitingRoom sites"
   # Email To ?
   EMAIL="sten.luyckx@cern.ch"
   # Email text/message
   if [ -f emailmessage.txt ];
   then
      rm emailmessage.txt
   fi
   touch emailmessage.txt
   EMAILMESSAGE="/tmp/emailmessage.txt"
   echo "run_WaitingRoom_Sites.sh  is running to slowly. See: /afs/cern.ch/user/g/gkandemi/scratch0/Waitingroom_Dashboard/"> $EMAILMESSAGE
   echo "/afs/cern.ch/user/g/gkandemi/scratch0/Waitingroom_Dashboard/" >>$EMAILMESSAGE
   # send an email using /bin/mail
   /bin/mail -s "$SUBJECT" "$EMAIL" < $EMAILMESSAGE

else
     echo "bash run_WaitingRoom_Sites.sh succesfully"
     touch scriptRunning.run
fi


#Run the script
txt="WaitingRoom_Sites.txt"
echo "python WaitingRoom_Sites.py $txt1"
python WaitingRoom_Sites.py $txt &> sites_WaitingRoom.log
cat sites_WaitingRoom.log

problem="$?"
echo "problem: $problem"

cp $txt /afs/cern.ch/user/g/gkandemi/www/WFMon/
echo "files copied to: /afs/cern.ch/user/g/gkandemi/www/WFMon/ "
rm scriptRunning.run

