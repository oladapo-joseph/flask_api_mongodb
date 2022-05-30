from random import randint as rand

def generate_token():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    token = [alphabet[rand(0,len(alphabet)-1)] for i in range(5) ]
    
    return ''.join(token)
