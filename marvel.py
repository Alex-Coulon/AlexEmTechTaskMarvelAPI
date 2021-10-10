import hashlib # for hashing the request
import requests # for creating requests
import datetime # for using correct datetime
import json # for reading json
import time # for delays
from prettytable import PrettyTable # third party module for output format

# End of Imports ------------------------------------------------------------------------------------------------------------

timestamp = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S') # setting time & date format

pub_key = 'xxx' # alex's public key
priv_key = 'xxx' # alex's private key

# End of setup keys & datetime ----------------------------------------------------------------------------------------------

print("Welcome to Alex Coulon's comic searcher.")
while True: # to keep on requesting new characters
    print("------------------------------------------------")
    print("Example marvel characters: hulk, thanos, thor, vision, ...")
    marvel_name_input = input('Type in a comic character to get their info. Fill in "exit" to cancel: ') #request marvel character
    if marvel_name_input == "": # check if marvel character has been given and not empty
        print("You didn't provide us with any character. Try again.")
        continue
    elif marvel_name_input == "exit":
        print('Cancelled.')
        break # stop program

# End of user input ----------------------------------------------------------------------------------------------------------


    def hash_params(): # definition for hasing, this def will be called on later

        hash_md5 = hashlib.md5() # put the hash in a variable
        hash_md5.update(f'{timestamp}{priv_key}{pub_key}'.encode('utf-8')) # we'll add the timestamp, private and public key in the hash and encode in utf-8 format
        hashed_params = hash_md5.hexdigest() # hash it in hex


        return hashed_params # give the full hash back


# End of hashing --------------------------------------------------------------------------------------------------------------


    params = {'ts': timestamp, 'apikey': pub_key, 'hash': hash_params()}; # the api call needs parameters, these will be collected here in 1 var

    apireturn = requests.get('https://gateway.marvel.com:443/v1/public/characters?name=' + marvel_name_input, params=params) # we'll get the date from the api and put it in a var

    results = apireturn.json() # we convert the received data to json, this works easier for me for testing and readability

# End of API call --------------------------------------------------------------------------------------------------------------

    status = results["code"] # we'll ask the status code of the api call

    if status == 200: #200 == all ok
        if results["data"]["total"] == 0: # if the character is not in the db this code will be executed
            print('------------------------------------------------')

            print("We did not find any characters named '" + marvel_name_input  +"', please check for typos and try again.")
            print('------------------------------------------------\n \n \n' )
            time.sleep(0.5) #add some time before requesting new character, this to prevent giant blocks of text appearing at once

        else:
            print('------------------------------------------------')
            name = results["data"]["results"][0]["name"] # get the characters name in a variable
            description = results["data"]["results"][0]["description"] # get the characters description in a variable

            print("Name: " + name)
            print("Description: " + description)
            chartable = PrettyTable() # setup table
            chartable.field_names = [name + "'s Comics"] # table header

            for each in results["data"]["results"][0]["comics"]["items"]: # for every comic we add a row to the table
                chartable.add_row(
                    [
                        each["name"],
                    ]
                )
            print(chartable) # print the table when all characters are added

            print(' \n \n \n' )
            time.sleep(0.5) # add some time before requesting new character, this to prevent giant blocks of text appearing at once
            
    else: # other api code, fail.
        print("The API request has failed, please try again.")



# End of program --------------------------------------------------------------------------------------------------------------




