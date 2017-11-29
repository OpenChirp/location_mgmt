import requests
import sys, getopt
import json
from pprint import pprint


# Set these globals based on the command line tool parsing
user = ''
token = ''
server_prefix = "http://openchirp.andrew.cmu.edu:7000"

# This function deletes a location 
#     loc_id is a string representing the location ID
# This function will exit upon error
def delete_location(loc_id):
   url='http://openchirp.andrew.cmu.edu:7000/api/location/'+loc_id
   global user
   global token
   check = input( "Are you sure you want to delete?  Type 'y' for yes: " )
   if check=='y':
      response = requests.delete(url,  auth=(user, token ))
      if response.status_code!=200:
         print("Error connecting: {}".format(response.status_code))
         sys.exit()



# This function makes a put request to change a location's name
#     loc_id is a string representing the location ID
#     name is a string representing the new name for the location
# This function will exit upon error
def rename_location(loc_id,name):
   global user
   global token
   global server_prefix
   url=server_prefix + '/api/location/'+loc_id
   data = {'name': name}
   headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
   response = requests.put(url, data=json.dumps(data), headers=headers, auth=(user, token ))
   if response.status_code!=200:
      print("Error connecting: {}".format(response.status_code))
      sys.exit()



# This function makes a put request to move a device to a new location 
#     dev_id is a string representing the device ID
#     loc_id is a string representing the location ID
# This function will exit upon error
def move_devices(dev_id,loc_id):
   global server_prefix
   url=server_prefix + '/api/device/'+dev_id
   global user
   global token
   data = {'location_id': loc_id}
   headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
   response = requests.put(url, data=json.dumps(data), headers=headers, auth=(user, token ))
   if response.status_code!=200:
      print("Error connecting: {}".format(response.status_code))
      sys.exit()

 
# This function prints the user's devices 
def print_myDevices():
   global server_prefix
   url=server_prefix + '/api/user/mydevices'
   global user
   global token
   response = requests.get(url, auth=(user, token ))
   if response.status_code!=200:
      print("Error connecting: {}".format(response.status_code))
      sys.exit()
   
   # not sure the best way to get raw json text, but this seems to work
   raw_json=response.text

   parsed_json=json.loads(raw_json)
   
   print( "My Devices:")
   if len(parsed_json)==0:
      print( "\tNo devices")
   # iterate through all of the returned json elements
   for i in range(0,len(parsed_json)):
       print("\"{}\" ({})".format(parsed_json[i]['name'],parsed_json[i]['id'] ))



# This function makes a get request to return all devices at a location 
#     loc_id is a string representing the location ID
#     depth is used for printing tabs correctly when needed
# This function will exit upon error
def print_devices(loc_id,depth):
   global server_prefix
   url=server_prefix + '/api/location/'+loc_id+'/devices'
   global user
   global token
   response = requests.get(url, auth=(user, token ))
   if response.status_code!=200:
      print("Error connecting: {}".format(response.status_code))
      sys.exit()
   
   # not sure the best way to get raw json text, but this seems to work
   raw_json=response.text

   parsed_json=json.loads(raw_json)
   
   if depth!=0:
      print( "\t"*(depth+1),end='')
   print( "Devices:")
   if len(parsed_json)==0:
      if depth!=0:
         print( "\t"*(depth+1),end='')
      print( "\tNo devices found at location")
   # iterate through all of the returned json elements
   for i in range(0,len(parsed_json)):
       if depth!=0:
          print( "\t"*(depth),end='')
       print("\t\"{}\" ({})".format(parsed_json[i]['name'],parsed_json[i]['id'] ))



# This function recursively prints the entire location tree 
#     loc_id is a string representing the location ID
#            if loc_id is blank, it starts at root
#     depth is a recursion counter used for printing tabs
# This function will exit upon error
def print_location_tree(loc_id,depth,device_flag):
   global server_prefix
   url=server_prefix + '/api/location/'+loc_id
   global user
   global token
   response = requests.get(url, auth=(user, token ))
   if response.status_code!=200:
      print("Error connecting: {}".format(response.status_code))
      sys.exit()

   raw_json=response.text

   if raw_json[0]=='[':
      raw_json=raw_json[1:-1]

   parsed_json=json.loads(raw_json)
   print( "\t"*depth,end='')
   print("\"{}\" ({})".format(parsed_json['name'],parsed_json['id']) )
   if device_flag==True:
     print_devices(parsed_json['id'],depth)

   children = parsed_json['children']
   for x in children:
      print_location_tree(str(x),depth+1,device_flag)


def create_location(loc_id,name,building_type,gps_lat, gps_lon):
   global user
   global token
   global server_prefix
   url=server_prefix + '/api/location/'+loc_id
   if gps_lat=='' or gps_lon=='':
      data = {'name': name, 'type' : building_type}
   else:
      data = {'name': name, 'type' : building_type, 'geo_loc' : {'coordinates' : [float(gps_lat) , float(gps_lon)]} }
   headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
   response = requests.post(url, data=json.dumps(data), headers=headers, auth=(user, token ))
   if response.status_code!=200:
      print("Error connecting: {}".format(response.status_code))
      sys.exit()




def print_help():
   print("oc_loc_mgmt.py -u <user> -t <token> [-c printTree | listDevices | moveDevice | removeDevice | renameLoc | deleteLoc | myDevices | createLocation ] [-l <loc-id>] [-d <dev-id>] [-n  'name'][-s 'BUILDING | INDOOR'] [-g lat lon]" )
   print("\tprintTree\t Prints the location tree")
   print("\tlistDevices\t List all devices at a location. Requires \"-l <loc-id>\" parameter")
   print("\tmoveDevice\t Move a device to a new location. Requires  \"-l <loc-id> -d <dev-id>\" parameters")
   print("\tremoveDevice\t Remove a device from the location tree. Requires  \"-d <dev-id>\" parameter")
   print("\trenameLoc\t Rename a location in the tree. Requires  \"-l <loc-id> -n <name>\" parameter")
   print("\tdeleteLoc\t Delete a location from the tree. Requires  \"-l <loc-id>\" parameter")
   print("\tmyDevices\t List all of the current user's devices\" parameter")
   print("\tcreateLocation\t Create a new location \"-l <parent-id> -n <name> -s <BUILDING | INDOOR> [-g <lat lon>] \" parameters")
   print("\nExample of running in interactive mode:\n\tpython oc_loc_mgmt.py -u user -t a6gyLVVXkaaa4JaYoStabALAaQl5RIK")
   print("\nExample of listing devices at a location:\n\tpython oc_loc_mgmt.py -u user -t a6gyLVVXkaaa4JaYoStabALAaQl5RIK -c listDevices -l 59307e0b7d6ec25f901d96c1")
   print("\nExample of renaming a location:\n\tpython oc_loc_mgmt.py -u user -t a6gyLVVXkaaa4JaYoStabALAaQl5RIK -c renameLoc -l 59307e04556ec25f901d96c1 -n \"my new location\"")
   print("\nExample of moving a device to a new location:\n\tpython oc_loc_mgmt.py -u user -t a6gyLVVXkaaa4JaYoStabALAaQl5RIK -c moveDevice -d 59fb644aaaa0cf7055615d9a -l 59307e04556ec25f901d96c1 ")
   sys.exit()

# This is the main part of the program that is called below.
# It handles the menu and grabs the user name and token from the commandline
def main(argv):
   global user
   global token

   clt_loc_id = ''
   clt_dev_id = '' 
   clt_name = ''
   clt_type= ''
   clt_lat= ''
   clt_lon= ''

   # Default the command line tool to interactive mode
   clt_mode= 'interactive'

   try:
      opts, args = getopt.getopt(argv,"hu:t:c:l:d:n:s:g::",["user=","token=","command=","loc=","dev=","name="])
   except getopt.GetoptError:
      print_help()
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         print_help()
      elif opt in ("-u", "--user"):
         user = arg
      elif opt in ("-t", "--token"):
         token = arg
      elif opt in ("-c","--command"):
         clt_mode = arg 
      elif opt in ("-l","--loc"):
         clt_loc_id =  arg 
      elif opt in ("-d","--dev"):
         clt_dev_id =  arg 
      elif opt in ("-n","--name"):
         clt_name =  arg 
      elif opt in ("-s","--space"):
         clt_type =  arg 
      elif opt in ("-g","--gps"):
         clt_lat =  arg[0] 
         clt_lon =  arg[1] 


#   print( "mode {}\nloc {}\ndev {}\nname {}".format(clt_mode,clt_loc_id,clt_dev_id,clt_name))
   if user=='' or token=='':
      print_help()

   if clt_mode=='printTree':
      print_location_tree('',0,False)
   elif clt_mode=='listDevices':
      print_devices(clt_loc_id,0)
   elif clt_mode=='moveDevice':
       move_devices(clt_dev_id,clt_loc_id)
   # Remove device simply reassigns the location to 0
   elif clt_mode=='removeDevice':
       move_devices(clt_dev_id,'000000000000000000000000')
   elif clt_mode=='renameLoc':
       rename_location(clt_loc_id,clt_name)
   elif clt_mode=='deleteLoc':
       delete_location(clt_loc_id) 
   elif clt_mode=='myDevices':
       print_myDevices()
   elif clt_mode=='createLocation':
       if((clt_loc_id=='') or (clt_name=='') or (clt_type=='') ):
          print_help()
       create_location(clt_loc_id, clt_name,clt_type,clt_lat,clt_lon)
   
   if clt_mode!='interactive':
      sys.exit(0) 

   print_location_tree('',0,False)

   while True:
      print("\n\nMenu Options:\n1) Print Location Tree\n2) List Devices at Location (requires: location_id)\n3) Move device (requires: device_id, location_id)\n4) Remove device from tree (requires: device_id)\n5) Rename Location (requires: location_id, name)\n6) Print location tree with devices (slow! Not using alldevices option)\n7) Delete Location (requires: location_id) \n8) List My Devices\n9) Create Location (requires: parent_id, name, type, [lat], [lon]\n10) Exit" );
      menu_option = input(': ')
      if menu_option=='1':
         print_location_tree('',0,False) 
      if menu_option=='2':
         loc_id=input('Enter location id: ')
         print_devices(loc_id,0)
      if menu_option=='3':
         device_id=input('Enter device id: ')
         loc_id=input('Enter destination location id: ')
         move_devices(device_id,loc_id)
      if menu_option=='4':
         device_id=input('Enter device id: ')
         move_devices(device_id,'000000000000000000000000')
      if menu_option=='5':
         loc_id=input('Enter location id: ')
         name=input('Enter new location name: ')
         rename_location(loc_id,name)
      if menu_option=='6':
         print_location_tree('',0,True) 
      if menu_option=='7':
         loc_id=input('Enter location id: ')
         delete_location(loc_id) 
      if menu_option=='8':
         print_myDevices() 
      if menu_option=='9':
         loc_id=input("Enter parent location ID: " )
         name=input('Enter new location name: ')
         building_type=input('Enter type [BUILDING or INDOOR]: ')
         gps_lat=input('Enter Latitude: ')
         gps_lon=input('Enter Longitude: ')
         create_location(loc_id,name,building_type,gps_lat, gps_lon) 
      if menu_option=='10':
         break 

   print( "Good Bye" )

if __name__ == "__main__":
   main(sys.argv[1:])

