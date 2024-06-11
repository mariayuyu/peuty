#!/bin/bash

LOG_FILE="/home/pi/display_service_log.txt"
LAST_FEH_COMMAND="/home/pi/last_feh_command.sh"
DEFAULT_IMAGE="/home/pi/peuty_gold.jpg"

echo "Starting display_last_image service" >> $LOG_FILE
export DISPLAY=:0

if [ -f "$LAST_FEH_COMMAND" ]; then
        echo "Running last feh command" >> "$LOG_FILE"
        IMAGE_PATH=$(grep -oP '(?<=feh --fullscreen --hide-pointer ).*(?= &)' "$LAST_FEH_COMMAND" | xargs)
        echo "Extracted image path: '$IMAGE_PATH'" >> "$LOG_FILE"
        if [ -n "$IMAGE_PATH" ] && [ -f "$IMAGE_PATH" ]; then
                echo "Found image path: '$IMAGE_PATH'" >> "$LOG_FILE"
                bash "$LAST_FEH_COMMAND"
        else
                echo "Last image not found or deleted, displaying default image" >> "$LOG_FILE"
                feh --fullscreen --hide-pointer "$DEFAULT_IMAGE" &
        fi

else
        echo "Displaying default image" >> "$LOG_FILE"
        feh --fullscreen --hide-pointer "$DEFAULT_IMAGE" &
fi
