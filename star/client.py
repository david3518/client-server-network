# GET format = "GET /assignment2?request=key HTTP/1.1"
# PUT format = "PUT /assignment2/key/value HTTP/1.1"
# DELETE format = "DELETE /assignment2/key HTTP/1.1"

import socket

cacheIP = "10.0.1.2"

dst_ip = str(input("Enter dstIP: "))
s = socket.socket()

print(dst_ip)

port = 12346

s.connect((dst_ip, port))
s.send('Hello cache'.encode())
print(s.recv(1024).decode())
#Write your code here:
#1. Add code to send HTTP GET / PUT / DELETE request. The request should also include KEY.

request_input = str(input("Enter the request"))
s.send(request_input.encode())

#2. Add the code to parse the response you get from the server.
response = s.recv(2048).decode()
http_response = response.split("\n")[0].rstrip()
explanation  = ""
if http_response  == "HTTP/1.1 400" : 
	explanation = "BAD REQUEST  ,  MESSAGE IS NOT UNDERSTOOD BY SERVER"
elif http_response == "HTTP/1.1 200" : 
	explanation = "REQUEST SUCCEDED"
elif http_response == "HTTP/1.1 404" : 
	explanation = "REQUEST DOCUMENT NOT FOUND THIS SERVER"
elif http_response == "HTTP/1.1 301":
	explanation = "REQUESTED OBJECT MOVED TO NEW LOCATION"
elif http_response == "HTTP/1.1 505":
	explanation = "HTTP VERSION NOT SUPPORTED"

# this print statement with print the request we are using 
print (response  +  "\n" + explanation)


s.close()
