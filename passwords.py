import random

utilizaveis = "#abcdefghijklmnopqrstuvwxyz0123456789!@%€&*()/§?}{£"
tamanho = 18
password = "".join(random.sample(utilizaveis,tamanho))

print('\n########################################')
print('Password: '+ password)
print('########################################\n')
