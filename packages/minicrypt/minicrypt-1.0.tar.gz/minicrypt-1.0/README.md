# minicrypt
Easy encryption algorithm 

```python
import minicrypt

key = minicrypt.generate_key() # random uuid4 hex
message = 'Hello, world!'

###### Encryption
encrypted = minicrypt.encrypt(message, key)
print(encrypted) # your encrypted message

###### Decryption
print(minicrypt.decrypt(encrypted, key)) # your message (Hello, world!) 
```

Install
```
pip3 install minicrypt
```