import socket
import json

def socket_server_link(serverIP , request_input) :
	p = socket.socket()
	port = 1234
	p.connect((serverIP , port))
	p.send('Hello server'.encode())
	print(p.recv(1024).decode())		
	p.send(request_input.encode())
	response = p.recv(2048).decode()
	p.close()
	return response
	
	
#WRITE CODE HERE:
#1. Create a KEY-VALUE pairs (Create a dictionary OR Maintain a text file for KEY-VALUES)
dict = {}
serverIP = "10.0.1.3"

dst_ip = str(input("Enter Server IP: "))

s = socket.socket()
print ("Socket successfully created")

dport = 12346

s.bind((dst_ip, dport))
print ("socket binded to %s" %(dport))

s.listen(5)
print ("socket is listening")


while True:
   
  c, addr = s.accept()
  print ('Got connection from', addr )
  print(c.recv(1024).decode())
  c.send("Hello Client".encode())
  recvmsg = c.recv(1024).decode()
  
  print('Server received '+recvmsg)
  

  #Write your code here


  #1. Uncomment c.send 
#2. Parse the received HTTP request
  #3. Do the necessary operation depending upon whether it is GET, PUT or DELETE
  #4. Send response

  with open('cache_data.json' , 'r') as file:
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
					response = socket_server_link(serverIP,recvmsg)
					c.send(response.encode())
				
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
						response = socket_server_link(serverIP,recvmsg)
						response_split = response.split("\n")
						if response_split[0].rstrip() == "HTTP/1.1 200" : 
							key = response_split[1].rstrip()
							value = response_split[2].rstrip()
							dict[key] = value
							with open('cache_data.json' ,'w') as file:
					        		json.dump(dict,file)
							c.send((response_split[0] + "\n"  + response_split[2] ).encode())
							
						else:
							c.send(response.encode())
					else:
						c.send((sendmsg + "\n"  + dict[key_get] ).encode()) 

	
				elif request_type == "DELETE" :
					l = L_split
					gl = l[2]
					key_delete = gl.split()[0]
					if dict.get(key_delete) != None:
						del dict[key_delete.rstrip()]
						c.send(sendmsg .encode())
						with open('cache_data.json' ,'w') as file:
					        	json.dump(dict,file)
					response = socket_server_link(serverIP,recvmsg)
					c.send(response.encode())
								
	
			else:
				sendmsg = "HTTP/1.1 301" 
				c.send((sendmsg +   " \n "  +  " { New location: /assignment2  } ").encode())
		else:
			sendmsg = "HTTP/1.1 400"
			c.send( (sendmsg ) .encode())
	else: 	

		sendmsg = "HTTP/1.1 505"
		c.send(sendmsg.encode())
  

  ##################

  c.close()
  
  #break