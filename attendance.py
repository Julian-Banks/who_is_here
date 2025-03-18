import subprocess
import re
from typing import Dict, Set, List
from datetime import datetime, timedelta
import threading
import time

class attendance_list():

    def __init__(self):
        #A list of all known macs
        self.KNOWN_MACS = {
        "2e:9f:fb:96:70:a7": {"name": "Julian", "device": "Phone"},
	    "a2:71:fe:a8:81:53": {"name": "Julian", "device": "Laptop"},
        "c8:89:f3:e4:45:fe": {"name": "Julian", "device": "Laptop"},
	    "32:0D:49:12:34:65": {"name": "Arno", "device": "Phone"},
        "62:95:8B:54:C3:5C": {"name": "Coral", "device": "Phone"},
        "3e:88:6c:11:dc:3a": {"name": "Leko", "device": "Phone"},
        "3e:2c:3b:bd:fd:09": {"name": "Charl", "device": "Phone"},
        "e0:63:da:a2:af:7d": {"name": "Leon", "device": "Phone"},
        "24:AE:CC:7D:32:F5": {"name": "Daynan", "device": "Phone"},
        "C4:06:83:D7:74:65": {"name": "Maurisha", "device": "Phone"},
        "a4:c6:9a:62:f0:61": {"name": "Shiyaam", "device": "Android"},
        "32:26:E3:4A:F9:0F": {"name": "Cyrne", "device": "Phone"},
        "F4:6D:3F:F3:EA:A8": {"name": "Cyrne", "device": "Laptop"},
        "34:41:5d:91:b8:c9": {"name": "Arno", "device": "Laptop"},
        "c6:1c:28:34:ce:c3": {"name": "Shiyaam", "device": "Laptop"},
        "58:1C:F8:27:45:BB": {"name": "Leon", "device": "Laptop"},
        "60:A5:E2:3B:1A:FA": {"name": "Charl", "device": "Laptop"},
        "3a:bc:ff:44:6b:fb": {"name": "Ilaam", "device": "Phone"},
        "60:45:2E:E6:1D:CE": {"name": "Ilaam", "device": "Laptop"},
        "ca:ce:cc:59:64:88": {"name": "Jon", "device": "Phone"},
        "b0:f1:d8:4d:37:1f": {"name": "Jon", "device": "Laptop"},
        "f8:0f:f9:e0:59:46": {"name": "Thalia", "device": "Phone"},
        "CC:15:31:6D:9D:0E": {"name": "Thalia", "device": "Laptop"},
        "12:69:9C:7B:F8:51": {"name": "Tam", "device": "Phone"},
        "7e:d1:68:91:65:46": {"name": "Tam", "device": "Laptop"},
        "e2:2b:99:eb:8e:ac": {"name": "Shahied", "device": "Phone"},
        "70:CF:49:73:64:46": {"name": "Shahied", "device": "Laptop"},
        "52:99:3F:EF:66:24": {"name": "Zenon", "device": "Phone"},
        "c6:65:79:10:ab:7b": {"name": "Zenon", "device": "Laptop"},
        "c2:db:f7:21:33"   : {"name": "Taya", "device": "Phone"},
        "26:05:7b:30:ee:35": {"name": "Taya", "device": "Laptop"},
    }
        #A list of everyone who has been present today. Dict keys("name", "first_seen", "last_seen", present)
        self.present: List[Dict[str,str]] = []
        self.start_background_tasks()
        self.sleep_period :int = 10


    #Public API to get the list of people present
    def get_present(self) -> List[Dict[str,str]]:
         return self.present

    #counter loop to run self.process_macs() periodically
    def check_attendance_loop(self)-> None:
        while True:
           self.process_macs()
           time.sleep(self.sleep_period)

    #A lot of code to run a function every day at midnight... I'm sure there is a better way of doing this. 
    def reset_attendance_loop(self)->None:
        while True:
            now = datetime.now()
            midnight = (now + timedelta(days=1)).replace(hour=0,minute=0, second=0,microsecond =0)
            seconds_until_midnight = (midnight - now).total_seconds()
            print (f"Next reset in {seconds_until_midnight:.2f} seconds")
            time.sleep(seconds_until_midnight)
            self.daily_reset()

    #Reset the attendance list daily. Could send the list somewhere first before resetting it?
    def daily_reset(self)->None:
        self.present = []

    #Start the loop to check for new devices and the daily counter for resets.
    def start_background_tasks(self)-> None:
        threading.Thread(target = self.reset_attendance_loop, daemon=True).start()
        threading.Thread(target = self.check_attendance_loop, daemon=True).start()


    def get_unique_mac_addresses(self) -> Set[str]:
        try:
            # Run arp-scan and capture the output.
            result = subprocess.run(["sudo","arp-scan", "--localnet"], capture_output=True, text=True, check=True)

            # Regular expression to match MAC addresses
            mac_regex = r"\t([0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5})\t"

            # Extract unique MAC addresses using a set
            unique_macs = set(re.findall(mac_regex, result.stdout))
            return unique_macs

        except subprocess.CalledProcessError as e:
            print("Error running arp-scan:", e)
            return set()


    # Get and print unique MAC addresses
    def process_macs(self)->None:

        mac_addresses = self.get_unique_mac_addresses()
        mac_addresses = self.to_lower(mac_addresses)
        KNOWN_MACS = self.get_known_macs() # Get all macs, lowercase
        print(mac_addresses)

        for mac in mac_addresses:
           if mac in KNOWN_MACS:
               self.process_attendance(mac)
               #print(f"Mac: {mac}, Name: {KNOWN_MACS[mac]}")
           else:
               pass
               #print(mac)

    def process_attendance(self,mac: str)  -> None:
        #Get the current time to update Last Seen
        current_time = datetime.now().strftime("%H:%M")

        device_info = self.get_known_macs()[mac]
        
	#Check the present list to see if the mac is already there and update last seen if it is
        for index, entry in enumerate(self.present):
            if entry["name"] == device_info["name"] and entry["device"] == device_info["device"]:
                #if the name is in the present list then just update and return. 
                self.present[index]["last_seen"] = current_time
                return None
        #If the function has not ended then the name is not in the present list. Add it with current time    
        self.present.append({
            "name": device_info["name"],
            "device": device_info["device"],
            "first_seen": current_time,
            "last_seen": current_time,
            "drill_attendance": ""
        })
        return None


    def get_known_macs(self) -> Dict[str,str] :
        KNOWN_MACS = {key.lower(): value for key, value in self.KNOWN_MACS.items()}
        #print(KNOWN_MACS)
        return KNOWN_MACS
    
    def update_drill_attendance(self, name:str, drill_attendance:str) -> bool:
        flag : bool = False
        for entry in self.present:
            if entry["name"] == name:
                entry["drill_attendance"] = drill_attendance
                flag = True
        if flag == True:
            return True
        else:
            return False

    def to_lower(self, set_to_lower: Set[str]) -> Set[str]:
        result = set()  # Initialize an empty set
        for item in set_to_lower:
            result.add(item.lower())  # Convert to lowercase and add to set
        return result

#Printing out some stuff to see
#mac_addresses = attendance_list.get_unique_mac_addresses()

#for mac in mac_addresses:
#    if mac in KNOWN_MACS:
#        print(f"{mac} - {KNOWN_MACS[mac]}")
#    else:
#        print(f"{mac} - Unknown Device")

