import socket as s

host = 'google.com' #example :D

ip = s.gethostbyname(host)
print('\n#########################################')
print('Host: [' + host + "] - IP: [" + ip + "]")
print('#########################################\n')