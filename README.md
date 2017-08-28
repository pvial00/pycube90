# pycube90
A Linear Feedback Shift Register Stream Cipher
Python Implementation of the Cube90 Cipher

Supports ASCII characters 32-90

# Usage:
>>> from pycube90 import Cube
>>> Cube("Test").encrypt("Welcome!")
'pe8LZ0u('
>>> Cube("Test").decrypt("pe8LZ0u(")
'Welcome!'
