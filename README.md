# RadarRPISwitch
Using the Radar sensor RCWL0516 to boot a raspberry PI through a relay
The motion sensor is used to boot a rpi which has a camera attached, invoke a python script that takes three pictures. The PI should shutdown if no further motion is 
detected. The first protoype will use the RPI 5v port to power a relay and the motion sensor. The end goal is to be able to cold boot the PI which means that the motion sensor asn the switch needs to be supplied from another source.
