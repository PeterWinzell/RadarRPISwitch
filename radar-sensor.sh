#! /bin/sh

case "$1" in
    start)
	echo "starting radar-sensor python script"
	/usr/local/bin/radar-sensor.py &
	;;
    stop)
	echo "stopping radar-sensor python script"
	pkill -f /usr/local/bin/radar-sensor.py
	;;
    *)
    	echo "Usage /etc/radar-sensor.sh {start|stop}"
	exit 1
	;;
esac

exit 0
