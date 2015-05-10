# check_mk
My check_mk work. 
Experimental stuff. Not extensibly tested.
##GoogleMaps check_mk plugin. 
1. install plugin
2. edit a host, in the coordinates field, klick the button, move the marker to the hosts location. Press Use this location.
3. Save the host. 

###Now you will have a host with a position. 
Do the same with all your hosts. 
You can go to the maps page from the added dashboard. This way will zoom to the bounds of all the hosts. Sometimes the zoom will fail and you will end up at coordinates -180,-180. I have not been able to solve this. The problem is in the javascript code. If I run the code in a debugger it always works. 
You can also click on the host icon. (looks like google maps logo) Then you will zoom in on the selected host.
The color of the hosts will change with the host state. (Green=OK, and so on)
