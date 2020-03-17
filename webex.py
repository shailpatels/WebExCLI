'''
MIT License

Copyright (c) 2020 Shail Patel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''



import requests

MY_KEY = "NmM3NWNiZGUtZjE4My00ZGMwLTlmMTQtZDk1ZDNiOTc5YTEzZDk4NThmZWItMWI5_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
#send a request
ENDPOINT = ""
#response = requests.get( ENDPOINT, headers = {"Authorization" : "Bearer " + MY_KEY} )


'''
The handleResponse function takes a URL and an optional payload parameter and 
makes a request to the target. It will use whatever MY_KEY is set to for autherization

endpoint : a string representing a URL to send the request to
payload : a dictionary of data to send to the target

returns True on success along with a response object
return False on failure with a None object
'''
def handleResponse(endpoint, payload = {}):
    response = requests.get(endpoint, headers={"Authorization" : "Bearer " + MY_KEY}, params=payload )
    if ( response.status_code != 200):
        print("Something went wrong! Got an error code of :", response.status_code)
        json = response.json()

        print ("Message ", json["message"] )
        print ("Here are the errors I got:")
        for error in json["errors"]:
            print("\t")
            for key in error:
                print(error[key])


        return False, None
    else:
        return True, response


def whoAmI():
    status, response = handleResponse("https://api.ciscospark.com/v1/people/me" )
    if status == True:
        json = response.json()
        #pretty print the users information
        print("Hi ", json["displayName"], "!" )
        print("Your email(s) are : ")
        for x in json["emails"]:
            print(x)


        print("Take a look at your profile pic at : ")
        print(json["avatar"])
        print()


'''
Attempts to find a user ID from a given username
If none are found returns False, ""
otherwise returns True, {ID}
'''
def searchIdFromUsername(username):
    status, response = handleResponse("https://api.ciscospark.com/v1/people", {"displayName" :  username})
    if ( status == True):
        # lets see if we found anyone
        json = response.json()
        people = json["items"]

        if len(people) < 1:
            return False, ""
        else:
            return True, people[0]

    else:
        return False, ""

'''
Given a username tries to find that person's information
'''
def whoIs(tgt):
    status, response = searchIdFromUsername( tgt )
    if status == False:
        print("Failed to lookup ", tgt )
        return


    user_id = response["id"]
    #we have the user_id now perform a look up on it
    #append the user_id to the url since each person is an endpoint
    status, response = handleResponse("https://api.ciscospark.com/v1/people/" + user_id )
    if status == False:
        print("Failed to lookup ", user_id)

    else:
        #pretty print data
        json = response.json()
        print()
        print("This is what I know about \"" + tgt + "\"")
        print("Goes by : " + json["displayName"] )
        print("Their emails are: ")

        for x in json["emails"]:
            print(x)

        print()
        print("Their avatar is: ")
        print(json["avatar"])
        print()
        print("Right now they're ", json["status"], " and were last online ", json["lastActivity"]  )
        print()


current_room = ""

'''
Lists all the rooms the user is apart of and returns 
a list of them
if the request could not be made, returns an empty list
'''
def Ls():
    status, response = handleResponse("https://api.ciscospark.com/v1/rooms")
    if ( status ):
        json = response.json()
        rooms = json["items"]

        for i in range( len(rooms) ):
            print(i, " : ", rooms[i]['title'] )

        print("You are apart of ", len(rooms), " rooms")
        print()

        return rooms

    return []

'''
given a target room attempt to change to it
'''
def Cd(tgt):
    #is it a number or string 
    status, response = handleResponse("https://api.ciscospark.com/v1/rooms")
    if ( status ):
        json = response.json()
        rooms = json["items"]
    else:
        return 


    is_number = tgt.isnumeric()

    global current_room
    for i in range( len (rooms) ):
        if (is_number and int(tgt) == i ):
            current_room = rooms[i]
            break
        elif( rooms[i]['title'] == tgt ):
            current_room = rooms[i]
            break

    print("Current room is ", current_room['title'])


'''
Sends a given message to the current room
'''
def sendMsg(msg):
    global current_room
    curr_id = current_room["id"]
    response = requests.post("https://api.ciscospark.com/v1/messages", 
                             headers={"Authorization" : "Bearer " + MY_KEY},
                             data={"roomId" : curr_id, "text" : msg})

    if response.status_code == 200:
        print("Sent message to ", current_room, "!!")
    else :
        print("ERROR ", response.status_code)


def showHelp():
    print("ls - list spaces")
    print("cd - change space")
    print("msg <MSG> - send a message to a space")
    print("whoami - gets information on yourself")
    print("whois <ID> - gets information on someone else")
    print("@q - exit the program")


def main():
    while (True):
        #get the user input
        cmd = input("Enter a command, or type \"help\" for help\n")

        #remove trailing and leading whitespace and change to lowercase
        cmd = cmd.strip().lower()

        if (cmd == "help"):
            showHelp()
        elif (cmd == "@q"):
            break
        elif (cmd == "whois"):
            tgt = input("Enter a person to search\n")
            whoIs(tgt)
        elif (cmd == "whoami"):
            whoAmI()
        elif(cmd == "msg"):
            msg = input("Enter a message to send\n")
            sendMsg(msg)
        elif(cmd == "ls"):
            Ls()
        elif(cmd == "cd"):
            tgt = input("Enter an index or name to enter\n")
            Cd(tgt)
        else:
            print("Unknown command \"" + cmd + "\"" )

main()