#!/usr/bin/env python3

"""ICS Importer

This module uses vobject to load a calendar event from an ICS file and adds it to Google Calendar via gcalcli. The default calendar and neccessary secrets should be specified in ~/.gcalclirc. A desktop file must be created to allow choosing the ICS Importer as the default program for opening ICS files.

Example desktop file (~/.local/share/applications/google-calendar-import.desktop):
    [Desktop Entry]
    Name=Google Calendar ICS Import
    Exec=sh -c "ics_importer.py %U"
    Type=Application
    MimeType=application/x-calendar;x-scheme-handler/ics;text/calendar
"""

import subprocess
import sys

import vobject

body = ""
with open(sys.argv[1]) as ics_file:
    for vevent in vobject.readOne(ics_file).vevent_list:
        body += vevent.summary.value

try:
    proc = subprocess.run(["gcalcli", "import", sys.argv[1]])
    if proc.returncode == 0:
        subprocess.run(["notify-send", "-i", "vcalendar", "Calendar Event Added", body])
    else:
        subprocess.run(["notify-send", "-i", "dialog-warning", "Calendar Import Failed", body])
except FileNotFoundError:
    subprocess.run(
        [
            "notify-send",
            "-i",
            "dialog-warning",
            "Calendar Import Failed",
            "gcalcli not found"
        ]
    )

