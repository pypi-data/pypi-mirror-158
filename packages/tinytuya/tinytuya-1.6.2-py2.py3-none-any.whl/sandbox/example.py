# TuyaPower Network Scanning Example
"""
 Display device state and power data from registered Tuya WiFi smart devices on the network

 Author: Jason A. Cox
 For more information see https://github.com/jasonacox/tuyapower

 This example script reads a JSON file (devices.json) to get name, device ID and device key
 for a set of smart devices to poll.  It will use the tuyapower network scanning function to discover
 the IP address for these devices.  It will then loop through each device and display state (on/off) 
 and any power data that may be available (for devices that monitor power).

 The devices.json file can be created from the output of the "tuya-cli wizard" command to 
 gather ID and Keys for all devices registered on your network. Information on how to do this is in
 the tuyapower README. You can also watch this great 'Tech With Eddie YouTube tutorial: 
 https://www.youtube.com/watch?v=oq0JL_wicKg&feature=youtu.be

Note: the output of the "tuya-cli wizard" command is improperly formatted JSON. I'm using the
demjson module to read the dirty JSON so that you can simply copy and paste the output from the
"tuya-cli wizard" command.
"""
import demjson
import tuyapower

# Terminal Color Formatting
bold="\033[0m\033[97m\033[1m"
subbold="\033[0m\033[32m"
normal="\033[97m\033[0m"
dim="\033[0m\033[97m\033[2m"
alert="\033[0m\033[91m\033[1m"
alertdim="\033[0m\033[91m\033[2m"

# Load Device Keys from Tuya JSON file
print("Loading Tuya Keys...")
f = open('devices.json',"r")
data = demjson.decode(f.read())
f.close()
print("    %s%s device keys loaded%s"%(dim,len(data),normal))
print()

print("Scanning network for Tuya devices...")
devices = tuyapower.deviceScan(False,20)
print("    %s%s devices found%s"%(dim,len(devices),normal))
print()

def getIP(d, gwid):
    for ip in d:
        if (gwid == d[ip]['gwId']):
            return (ip,d[ip]['version'])
    return (0,0)

print("Polling devices...")
for i in data:
        name = i['name'] 
        (ip,ver) = getIP(devices, i['id'])
        if (ip == 0):
            print ("    %s[%s]%s - %sError: No IP found%s"%(subbold,name,dim,alert,normal))
        else:
            (on, w, mA, V, err) = tuyapower.deviceInfo(i['id'], ip, i['key'], ver)
            state = alertdim + "Off" + dim
            if(on):
                state = subbold + "On" + dim
            if(w >= 0):
                print("    %s[%s]%s - %s - Power: %sW, %smA, %sV"%(subbold,name,dim,state,w,mA,V))
            else:
                print("    %s[%s]%s - %s"%(subbold,name,dim,state))

print()