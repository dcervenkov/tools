#!/bin/bash

while getopts "m:u:" opt; do
  case $opt in
    m)
        EMAIL="$OPTARG"
    ;;
    u)
        USER="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

shift $((OPTIND-1))

if [ "$#" -ne 1 ]; then
    echo "ERROR: Must have 1 argument!"
    echo "Usage: $0 [OPTIONS] PROCESS-NAME"
    exit 1
fi

if [ ! -f $HOME/.mailaddress ] && [ -z $EMAIL ]; then
    echo "ERROR: Email not specified and can't find file '$HOME/.mailaddress'."\
         "Please specify an email using '-m EMAIL' or create"\
         "'$HOME/.mailaddress' and populate it with the email address to which"\
         "notifications should be sent."
    exit 2
fi

PROC_NAME=$1

if [ -z $EMAIL ]; then
    EMAIL=$(cat $HOME/.mailaddress)
fi

echo "[$(date '+%F %R')]" "Monitoring process '$PROC_NAME' for user $USER."
echo "[$(date '+%F %R')]" "Email will be sent to $EMAIL when the process exits."

FOUND=false
START=$(date +%s)

while true; do
    if pgrep -x -u $USER $PROC_NAME > /dev/null; then
        FOUND=true
        sleep 6
    else
        if [ "$FOUND" = false ]; then
            echo "[$(date '+%F %R')]" "No process named '$PROC_NAME' found. Exiting."
            exit 3
        fi
        echo "[$(date '+%F %R')]" "Process '$PROC_NAME' not found anymore."

        END=$(date +%s)
        HOURS=$(echo "scale=0; ($END - $START) / 3600" | bc -l )
        MINUTES=$(echo "scale=0; (($END - $START) % 3600)/60" | bc -l )

        (echo "Monitored process '$PROC_NAME' could no longer be found at $(date) after approximately $HOURS hours and $MINUTES minutes." | mail -s "$PROC_NAME Finished" $EMAIL) && echo "Mail sent."

        exit 0
    fi
done
