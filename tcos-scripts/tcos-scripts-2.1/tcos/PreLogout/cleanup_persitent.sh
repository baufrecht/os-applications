#!/bin/bash
# set -x
 # get UID/GID
        MY_UID=`id -u $USER`
        MY_GID=`id -g $USER`

        # Unmount $HOME
        sync
        sudo umount -l "$HOME"

        sudo rm /home/tcos
        sudo umount -l /home/*/.pulse
        sudo umount -l /home/*/
        sudo umount -l /home

        # terminate (respawning) launcher
        LAUNCHER_PIDS=`ps ax | grep "/opt/.*/tcos/launcher" | awk '{print $1}'`
        sudo kill $LAUNCHER_PIDS &>/dev/null
        
        # and give them 10 sec to terminate
        
        while `ps -U $(id -u $USER) &>/dev/null`; do
                        sleep 5

                        # time's up: kill'em all
                       pkill -U $USER               
        done

             
        # Remove leftovers
        #find /tmp -maxdepth 1 -uid $MY_UID -gid $MY_GID -exec rm -rf {} \;




