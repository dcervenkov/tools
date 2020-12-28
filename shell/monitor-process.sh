#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "ERROR: Must have 1 argument!"
	echo "Usage: $0 PROCESS-NAME"
	exit 1
fi

if [ ! -f $HOME/.mailaddress ]; then
	echo "ERROR: Can't find file '$HOME/.mailaddress', please"\
	     "create it and populate it with the email address"\
	     "to which notifications should be sent."
	exit 2
fi

PROC_NAME=$1
EMAIL=$(cat $HOME/.mailaddress)

echo "[$(date '+%F %R')]" "Monitoring process '$PROC_NAME'."
echo "[$(date '+%F %R')]" "Will send email to $EMAIL when the process exits."

FOUND=false
START=$(date +%s)

while true; do
	if pgrep -x $PROC_NAME > /dev/null; then
		FOUND=true
		sleep 6
	else
		if [ "$FOUND" = false ]; then
			echo "[$(date '+%F %R')]" "Process '$PROC_NAME' not found."
			exit 0
		fi
		echo "[$(date '+%F %R')]" "Process '$PROC_NAME' not found anymore."

		END=$(date +%s)
		HOURS=$(echo "scale=0; ($END - $START) / 3600" | bc -l )
		MINUTES=$(echo "scale=0; (($END - $START) % 3600)/60" | bc -l )

		(echo "Monitored process '$PROC_NAME' could no longer be found at $(date) after approximately $HOURS hours and $MINUTES minutes." | mail -s "$PROC_NAME Finished" $EMAIL) && echo "Mail sent."

		exit 0
	fi
done
