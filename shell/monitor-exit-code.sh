#!/bin/bash

while getopts "m:r:i:" opt; do
  case $opt in
    m)
        EMAIL="$OPTARG"
    ;;
    r)
        REPEAT="$OPTARG"
    ;;
    i)
        SLEEP_INTERVAL="$OPTARG"
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

if [ ! -f "$HOME/.mailaddress" ] && [ -z "$EMAIL" ]; then
    echo "ERROR: Email not specified and can't find file '$HOME/.mailaddress'."\
         "Please specify an email using '-m EMAIL' or create"\
         "'$HOME/.mailaddress' and populate it with the email address to which"\
         "notifications should be sent."
    exit 2
fi

COMMAND=$1

if [ -z "$EMAIL" ]; then
    EMAIL=$(cat "$HOME/.mailaddress")
fi

if [ -z "$REPEAT" ]; then
    REPEAT=1
fi

if [ -z "$SLEEP_INTERVAL" ]; then
    SLEEP_INTERVAL=6
fi

echo "[$(date '+%F %R')]" "Monitoring exit code of '$COMMAND'."
echo "[$(date '+%F %R')]" "Email will be sent to $EMAIL when the command exit code changes."

FOUND=false
START=$(date +%s)

while true; do
    $COMMAND &> /dev/null
    EXIT_CODE=$?
    if ! $FOUND; then
        ORIG_EXIT_CODE=$EXIT_CODE
        echo "[$(date '+%F %R')]" "Initial exit code: $ORIG_EXIT_CODE."
    fi

    if [ $EXIT_CODE == 127 ]; then
        echo "Command not found"
        exit
    fi

    if [ $EXIT_CODE != $ORIG_EXIT_CODE ]; then
        echo "[$(date '+%F %R')]" "'$COMMAND' exit code changed from $ORIG_EXIT_CODE to $EXIT_CODE."
        END=$(date +%s)
        HOURS=$(echo "scale=0; ($END - $START) / 3600" | bc -l )
        MINUTES=$(echo "scale=0; (($END - $START) % 3600)/60" | bc -l )

        (echo "Monitored process '$PROC_NAME' could no longer be found at $(date) after approximately $HOURS hours and $MINUTES minutes." | mail -s "$PROC_NAME Finished" "$EMAIL") && echo "Mail sent."
        exit
    else
        FOUND=true
        sleep $SLEEP_INTERVAL
    fi


done
