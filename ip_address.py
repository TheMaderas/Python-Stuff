import socket

hostname = socket.gethostname()
ipaddress = socket.gethostbyname(hostname)

print('\n########################################')
print('Your IP: '+ ipaddress)
print('########################################\n')
