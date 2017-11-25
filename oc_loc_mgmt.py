import requests
import sys, getopt
import json
from pprint import pprint

user = ''
token = ''

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
   url='http://openchirp.andrew.cmu.edu:7000/api/location/'+loc_id
   global user
   global token
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
   url='http://openchirp.andrew.cmu.edu:7000/api/device/'+dev_id
   global user
   global token
   data = {'location_id': loc_id}
   headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
   response = requests.put(url, data=json.dumps(data), headers=headers, auth=(user, token ))
   if response.status_code!=200:
      print("Error connecting: {}".format(response.status_code))
      sys.exit()

 

# This function makes a get request to return all devices at a location 
#     loc_id is a string representing the location ID
#     depth is used for printing tabs correctly when needed
# This function will exit upon error
def print_devices(loc_id,depth):
   url='http://openchirp.andrew.cmu.edu:7000/api/location/'+loc_id+'/devices'
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
   url='http://openchirp.andrew.cmu.edu:7000/api/location/'+loc_id
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


# This is the main part of the program that is called below.
# It handles the menu and grabs the user name and token from the commandline
def main(argv):
   global user
   global token
   try:
      opts, args = getopt.getopt(argv,"hu:t:",["user=","token="])
   except getopt.GetoptError:
      print( "oc_loc_mgmt.py -u <user> -t <token>" )
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print("oc_loc_mgmt.py -u <user> -t <token>" )
         sys.exit()
      elif opt in ("-u", "--user"):
         user = arg
      elif opt in ("-t", "--token"):
         token = arg

   print_location_tree('',0,False)

   while True:
      print("\n\nMenu Options:\n1) Print Location Tree\n2) List Devices at Location (requires: location_id)\n3) Move device (requires: device_id, location_id)\n4) Remove device from tree (requires: device_id)\n5) Rename Location (requires: location_id)\n6) Print location tree with devices (warning, slow!)\n7) Delete Location\n8) Exit" );
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
         break 

   print( "Good Bye" )

if __name__ == "__main__":
   main(sys.argv[1:])

