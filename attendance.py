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
        "2e:9f:fb:96:70:a7": "Julian's Phone",
	"a2:71:fe:a8:81:53": "Julian's Laptop (Home)",
        "c8:89:f3:e4:45:fe": "Julian's Laptop",
	"32:0D:49:12:34:65": "Arno's Phone",
        "34:41:5d:91:b8:c9": "Arno's Laptop",
        }
        #A list of everyone who has been present today. Dict keys("name", "first_seen", "last_seen")
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

        for mac in mac_addresses:
           if mac in self.KNOWN_MACS:
               self.process_attendance(self.KNOWN_MACS[mac])


    def process_attendance(self,name: str)  -> None:
        #Get the current time to update Last Seen
        current_time = datetime.now().strftime("%H:%M")

	#Check the present list to see if the mac is already there and update last seen if it is
        for index, entry in enumerate(self.present):
            if entry["name"] == name:
                #if the name is in the present list then just update and return. 
                self.present[index]["last_seen"] = current_time
                return None
        #If the function has not ended then the name is not in the present list. Add it with current time
        self.present.append({"name":name, "first_seen":current_time, "last_seen":current_time})
        return None


#Printing out some stuff to see
#mac_addresses = attendance_list.get_unique_mac_addresses()

#for mac in mac_addresses:
#    if mac in KNOWN_MACS:
#        print(f"{mac} - {KNOWN_MACS[mac]}")
#    else:
#        print(f"{mac} - Unknown Device")

