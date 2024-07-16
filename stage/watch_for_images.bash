#!/bin/bash
export DISPLAY=:0
WATCH_DIR="/home/pi/Pictures"
APP_IDENTIFIER="_APPID"

#fonction pour vérifier si le fichier est complètement téléchargé
is_file_stable(){
        local file=$1
        local prev_size=0
        local cur_size=0

        while true; do
                cur_size=$(stat -c%s "$file")
                if [ "$cur_size" -eq "$prev_size" ]; then
                        break
                fi
                prev_size=$cur_size
                sleep 1
        done
}

inotifywait -m -e create -e moved_to --format '%w%f' "${WATCH_DIR}" | while read NEWFILE
do
        echo "Detected change in file: ${NEWFILE}" >> /home/pi/inotify_log.txt
        if [[ "${NEWFILE}" =~ \.(jpg|jpeg|png|bmp|gif)$ ]]; then
                echo "Processing image file: ${NEWFILE}" >> /home/pi/inotify_log.txt

                is_file_stable "${NEWFILE}"
                if [[ "${NEWFILE}" == *"${APP_IDENTIFIER}"* ]]; then
                        echo "File verified: ${NEWFILE}" >> /home/pi/inotify_log.txt
                        chmod 644 "${NEWFILE}"
                        feh --fullscreen --hide-pointer "${NEWFILE}" &
                        echo "feh --fullscreen --hide-pointer '${NEWFILE}' &" > /home/pi/last_feh_command.sh
                else
                        echo "File rejected: ${NEWFILE}" >> /home/pi/inotify_log.txt
                        rm "${NEWFILE}"
                fi
        fi
done

