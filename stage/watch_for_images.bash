#!/bin/bash
export DISPLAY=:0
WATCH_DIR="/home/pi/Pictures"

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
