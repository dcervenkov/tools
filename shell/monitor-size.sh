#!/bin/bash

while getopts "m:i:" opt; do
  case $opt in
    m)
        EMAIL="$OPTARG"
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
    echo "Usage: $0 [OPTIONS] DIRECTORY"
    exit 1
fi

if [ ! -f "$HOME/.mailaddress" ] && [ -z "$EMAIL" ]; then
    echo "ERROR: Email not specified and can't find file '$HOME/.mailaddress'."\
         "Please specify an email using '-m EMAIL' or create"\
         "'$HOME/.mailaddress' and populate it with the email address to which"\
         "notifications should be sent."
    exit 2
fi

DIRECTORY=$(realpath "$1")

if [ -z "$EMAIL" ]; then
    EMAIL=$(cat "$HOME/.mailaddress")
fi

if ! du -s "${DIRECTORY}"; then
    exit 3
fi

if [ -z "$SLEEP_INTERVAL" ]; then
    SLEEP_INTERVAL=6
fi

echo "[$(date '+%F %R')]" "Monitoring the size of '$DIRECTORY' directory every ${SLEEP_INTERVAL}s."
echo "[$(date '+%F %R')]" "Email will be sent to $EMAIL when the directory stops growing."

LAST_SIZE=0
START=$(date +%s)

while true; do
    SIZE=$(du -s "${DIRECTORY}" | cut -f1)
    if [[ $SIZE -gt $LAST_SIZE ]] ; then
        LAST_SIZE=$SIZE
        sleep $SLEEP_INTERVAL
    else
        echo "[$(date '+%F %R')]" "Size of '$DIRECTORY' didn't increase in the last $SLEEP_INTERVAL seconds."

        END=$(date +%s)
        HOURS=$(echo "scale=0; ($END - $START) / 3600" | bc -l )
        MINUTES=$(echo "scale=0; (($END - $START) % 3600)/60" | bc -l )

        (echo "Monitored directory '$DIRECTORY' stopped growing at $(date) after approximately $HOURS hours and $MINUTES minutes." | mail -s "$DIRECTORY Stopped Growing" "$EMAIL") && echo "Mail sent."

        exit 0
    fi
done
