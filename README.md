# pycube90
A Linear Feedback Shift Register Stream Cipher
Python Implementation of the Cube90 Cipher

Supports ASCII characters 32-122

# Usage:
>>> from pycube90 import Cube
>>> Cube("Test").encrypt("Welcome!")
'pe8LZ0u('
>>> Cube("Test").decrypt("pe8LZ0u(")
'Welcome!'

# Passing a  nonce:
>>> from pycube90 import Cube
>>> Cube("Test", "NONCE").encrypt("Welcome!")
>>> Cube("Test", "NONCE").decrypt("pe8LZ0u(")

# Standalone script usage:
scripts/cube90.py <encrypt/decrypt>

# CubePassword
Password Generator  
passmaker = CubePassword()  
print passmaker.password(length=12, num=1)  
