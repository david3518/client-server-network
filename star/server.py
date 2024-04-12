import socket
import json

#WRITE CODE HERE:
#1. Create a KEY-VALUE pairs (Create a dictionary OR Maintain a text file for KEY-VALUES)
dict = {}


dst_ip = str(input("Enter Server IP: "))

s = socket.socket()
print ("Socket successfully created")

dport = 1234

s.bind((dst_ip, dport))
print ("socket binded to %s" %(dport))

s.listen(5)
print ("socket is listening")


while True:
   
  c, addr = s.accept()
  print ('Got connection from', addr )
  print(c.recv(1024).decode())
  c.send("Hello Cache".encode())
  recvmsg = c.recv(1024).decode()
  
  print('Server received '+recvmsg)
  

  #Write your code here


  #1. Uncomment c.send 
#2. Parse the received HTTP request
  #3. Do the necessary operation depending upon whether it is GET, PUT or DELETE
  #4. Send response

  with open('data.json' , 'r') as file:
  	dict = json.load(file)
  request_type = ""
  if len(recvmsg) != 0:
	L_split = recvmsg.split('/')
  	request_type =  L_split[0]
	request_type = request_type.rstrip()
	HTTP_version = L_split[len(L_split)-1]
	index = recvmsg.find('/' , 0 , 100)
	location = L_split[1][0:12]

	if HTTP_version == '1.1' : 
		location =  L_split[1]
		location_value = location.split('?')
		if request_type == "PUT" or request_type == "GET" or request_type == "DELETE" :
  
			if location_value[0] == 'assignment2'   :
	
				sendmsg = "HTTP/1.1 200"
	
				if request_type == "PUT" : 
					l = L_split
					key = l[2].rstrip()
					value = l[3].split()[0].rstrip()
					dict[key] = value
					c.send(sendmsg.encode())
					with open('data.json' ,'w') as file:
						json.dump(dict,file)
				
				elif request_type == "GET" : 
					key_get = ""
					index  = -1
					index = recvmsg.find('request' , 0 , 100)
					if index == -1 : 
						sendmsg = "HTTP/1.1 400"
						c.send(sendmsg.encode())
						continue
					for i in range(index + 8 , 100):
						if recvmsg[i] == " ":
							key_get = recvmsg[index+8 : i]
							break
					if dict.get(key_get) == None:
						sendmsg = "HTTP/1.1 404"
						c.send(sendmsg.encode())
						continue
					c.send((sendmsg + "\n"  +  key_get  + " \n"  +  dict[key_get] ).encode()) 
			
				elif request_type == "DELETE" :
					l = L_split
					gl = l[2]
					key_delete = gl.split()[0].rstrip()
					if dict.get(key_delete) == None:
						sendmsg = "HTTP/1.1 404"
						continue
								
					del dict[key_delete.rstrip()]
					c.send(sendmsg .encode())
					with open('data.json' ,'w') as file:
				        	json.dump(dict,file)
	
			else:
				sendmsg = "HTTP/1.1 301" 
				c.send((sendmsg +   " \n "  +  " { New location: /assignment2  } ").encode())
		else:
			sendmsg = "HTTP/1.1 400"
			c.send( (sendmsg ) .encode())
	else: 	

		sendmsg = "HTTP/1.1  505"
		c.send(sendmsg.encode())
  

  ##################

  c.close()
  
  #break