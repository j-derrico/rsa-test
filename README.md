# rsa-test
exploring how rsa encryption works with Python
 
This project designs and implements Python code for encoding and decoding messages using the RSA cryptosystem, which involves using prime numbers to generate public and private keys.  First, I start with basic programs for converting a string of text into numbers using ascii (American Standard Code for Information Interchange) values, converting a string of numbers back into text, and converting an integer into binary.

Next, I wrote programs for some of the more advanced mathematical processes used in RSA encryption, including Fast Modular Exponentiation (FME), Euclid's Algorithm for finding the Greatest Common Divisor (GCD) of two numbers, and Euclid's Extended Algorithm to find Bezout's coefficients, which in turn gives us the modular inverse to create our private key for the encryption.  From there, I wrote the code to actually generate the public and private keys, and encode and decode messages.

The main function is designed to demonstrate the functions working together.

This is designed purely to explore the mathemtacal theory behind RSA encryption using Python rather than to actually securely encrypt messages.  It would require several more layers (offsetting the alphabet a la Julius Caesar by "random" number would be an easy first one, hash functions would also be very easy) of encryption to be even a little bit effective.
