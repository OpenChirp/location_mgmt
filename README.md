# Location Tree Manager
Python command line location tree manager that allows users with developer role to manipulate the location tree.
 
``` 
python oc_loc_mgmt.py -h
oc_loc_mgmt.py -u <user> -t <token>
```

You can get your user id and token under the "My Profile" tab on the web page that appears when you click on your name in the upper right.
```
Example Output:
python oc_loc_mgmt.py -u user -t a6gyLVaXkKUU4JaYoSaCbAaAaQl5RI
"root" (59092f3d357344172464b270)
        "CMU" (59092fa4f7a4575caac3b865)
                "CIC" (59092facf7a4575caac3b866)
                        "Floor 1" (590a7beae65c736876c9bba7)
                                "1301" (590b8a9bc1d7ee2313ee421b)
                        "Floor 2" (590b8868c1d7ee2313ee4215)
                                "Craig Desk" (592880467d6ec25f901d9666)
                                "Ryan's Desk" (5935952015ac3f064e81aeb7)
                                "Artur's Desk" (5935f9a315ac3f064e81aeb9)
                                "Agr's Desk" (59b58c99f230cf7055614d78)
                "Porter Hall" (59307e0b7d6ec25f901d96c1)
                        "Floor 2" (5977dabd2d16735bdcadecae)
                "GHC" (59ea56cff230cf7055615d00)
                        "Floor 6" (59ea57c3f230cf7055615d02)
                                "6407" (59ea57f2f230cf7055615d03)
        "Bosch" (590a7baae65c736876c9bba6)
                "3rd Floor" (5926d60365aedb58661c3daf)
        "Public" (5988ca102a8c221284d199ea)
                "Pittsburgh (USA)" (5988ca392a8c221284d199eb)
                        "Anh's" (59e801f8f230cf7055615cb3)
                        "Artur's" (59fb6449f230cf7055615d9a)
                        "Agr's House" (5a121c7bea6c865841d1cd46)

Menu Options:
1) Print Location Tree
2) List Devices at Location (requires: location_id)
3) Move device (requires: device_id, location_id)
4) Remove device from tree (requires: device_id)
5) Rename Location (requires: location_id)
6) Print location tree with devices (warning, slow!)
7) Delete Location
8) Exit
:
```

# Command Line Options
```
$ python oc_loc_mgmt.py -h
oc_loc_mgmt.py -u <user> -t <token> [-c printTree | listDevices | moveDevices | removeDevice | renameLoc | deleteLoc] [-l <loc-id>] [-d <dev-id>] [-n  'name']
	printTree	 Prints the location tree
	listDevices	 List all devices at a location. Requires "-l <loc-id>" parameter
	moveDevices	 Move a device to a new location. Requires  "-l <loc-id> -d <dev-id>" parameters
	removeDevice	 Remove a device from the location tree. Requires  "-d <dev-id>" parameter
	renameLoc	 Rename a location in the tree. Requires  "-l <loc-id> -n <name>" parameter
	deleteLoc	 Delete a location from the tree. Requires  "-l <loc-id>" parameter

Example of listing devices at a location:
	python oc_loc_mgmt.py -u user -t a6gyLVVXkaaa4JaYoStabALAaQl5RIK -c listDevices -l 59307e0b7d6ec25f901d96c1

Example of renaming a location:
	python oc_loc_mgmt.py -u user -t a6gyLVVXkaaa4JaYoStabALAaQl5RIK -c renameLoc -l 59307e04556ec25f901d96c1 -n "my new location"
```
