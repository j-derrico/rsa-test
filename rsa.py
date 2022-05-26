import random
from tracemalloc import start


def Convert_Text(_string):
    integer_list = []
    # for loop to get each letter
    for let in _string:
        # convert each letter to ascii value and append to integer_list
        integer_list.append(ord(let))
    return integer_list


def Convert_Num(_list):
    # empty string that will be updated as we go
    _string = ''
    # for loop to iterate through list of integers
    for i in _list:
        # update the string with the letter that corresponds to the value of i
        _string += chr(i)
    return _string


#incorporated binary conversion in FME function--more streamlined
# def Convert_Binary_String(_int):
#     # if the int is 0, it's already in binary so we don't need to convert it
#     if _int == 0:
#         return [0]
#     # creating the empty string to hold our binary conversion
#     bit = ""
#     while _int > 0:
#         bit = bit + str(_int % 2)
#         _int = _int // 2
#     # reversing the order, since we build out the binary number from right to left but our string updates from left to right
#     bits = bit[::-1]
#     return bits


def Euclidean_Alg(a, b):
    # set conditions for the loop
    while b > 0:
        k = a % b
        q = a // b
        a = b
        b = k
    return a


def FME(a, b, m):
    # will return a^b mod m
    # initialize the variables for the result and the square
    result = 1
    square = a
    #convert to binary
    while b > 0:
        k = b % 2
        if k == 1:  # if there is a binary 1 in this position, we'll update the value of the result
            result = (result * square) % m
        square = (square * square) % m  # we'll update the value of square even if there's a 0 in this position
        b = b // 2  
    return result


def Find_Public_Key_e(p, q):
    # n is product of p and q
    n = p * q
    # find public key e, which has to be relatively prime to (p-1)(q-1).  Here I used randrange so that I would not always
    # have a low e
    while True:
        i = random.randrange(2, 100000)
        # calculating the GCD for i, (p-1)(q-1)
        gcd = Euclidean_Alg(i, ((p - 1) * (q - 1)))
        # if they are relatively prime and i !=p or q, that value works for e
        if gcd == 1 and i != p and i != q and i < ((p - 1) * (q - 1)):
            e = i
            return e


# defining Extended Euclidean Algorithm:
def EEA(a, b):
    # initializing values of s and t (Bezout's Coefficients)
    s1, t1 = 1, 0
    s2, t2 = 0, 1
    # beginning the while loop, ends when k=0 (meaning we've reached the GCD)
    while b > 0:
        # first step of Euclidean algorithm , m mod n
        k = a % b
        # quotient gives us the recipe for creating the value of m mod n at each step, which updates s and t
        q = a // b
        # setting the new values for m and n for the next iteration
        a = b
        b = k
        # updating the values for s1, t1 and s2, t2
        s1, s2 = s2, s1 - q * s2
        t1, t2 = t2, t1 - q * t2
    return a, s1


def Find_Private_Key_d(e, p, q):
    # private key is the modular inverse of e mod (p-1)(q-1)
    d = (EEA(e, ((p - 1) * (q - 1)))[1])
    # while loop to ensure that d is positive:
    while d < 0:
        d = d + ((p - 1) * (q - 1))
    return d


def Encode(n, e, message):
    cipher_text = []
    # converting each character to its ascii value
    a = Convert_Text(message)
    # loop to run each character through the encryption and add it to the list
    for i in a:
        cipher_text.append(FME(i, e, n))
    return cipher_text


def Decode(n, d, cipher_text):
    # create empty list to add to
    message_num = []
    # iterate through each number in cipher_text
    for num in cipher_text:
        message_num.append(FME(num, d, n))
    return Convert_Num(message_num)


def factorize(n):
    # n is a number, return the smallest factor of n
    # loop to iterate through the values from 2 to n-1
    for i in range(2, n - 1):
        # if n has a factor, that factor will be returned
        if n % i == 0:
            return i
    return False


def factorize_for_p_and_q(n):
    # start with similar code to above
    for i in range(2, n - 1):
        if n % i == 0:
            # settng p equal the factor
            p = i
            # setting q
            q = n // p
            return p, q
    return False


def brute_force_decode(n, e, cipher_text):
    # solve for p and q from n
    p, q = factorize_for_p_and_q(n)
    # solve for d
    d = Find_Private_Key_d(e, p, q)
    # decode with the earlier function now that we know the private key
    return Decode(n, d, cipher_text)


def find_primes():
    # need values large enough to accommodate ascii values, so use randrange.  Because I'm still using brute force
    #factorization, it can't be too high or it will take forever just to find values of p and q
    while True:
        i = random.randrange(29, 1500000)
        if factorize(i) == False:
            return i



#main function to demonstrate functions above 
def main ():
    #while loop so that the program runs until the user decides to quit
    while True:   
        print ("RSA encryption testing:\n")
        start = input('Are you here to Encode or Decode?\n')
        #if user chooses to encode
        if start == 'Encode' or start == 'encode':
            #giving user options for generating keys or encoding using keys they already have (to respond to someone on piazza, for example)
            start_encode = int(input ('Would you like to: \n 1. Encode using your own keys \n 2. Encode using keys generated by this program\n'))
            if start_encode == 1:
                n = int (input('Please enter public key n:\n'))
                e = int (input ('Please enter public key e:\n'))
                enc_message = input ('Please enter the message you would like to encode:\n')
                print ('Here is your encoded message:\n', Encode (n, e, enc_message))
            elif start_encode == 2:
                #generating prime number values for p and q, calculating n and e
                p = find_primes()
                q = find_primes()
                n = p * q
                e = Find_Public_Key_e (p, q)
            
                enc_message = input('Please enter the message you would like to encode:\n')
                print('Here is your encoded message:', Encode(n, e, enc_message))
                print('The public keys for your message are n = {}, e = {}'.format(n, e))
            
                d_print = input('Would you like to print the private key? y/n \n')
                if d_print == 'y':
                    d = Find_Private_Key_d(e, p, q)
                    print('d =', d)
        #if user chooses to decode
        elif start == 'Decode' or start == 'decode':
            dec_message = (input('Please enter the encoded message as a list of numbers separated by commas:\n'))
            #removing the brackets so we can convert the string to a list of integers
            if '[' in dec_message:
                dec_message = dec_message [1:-1]
            #splitting the string into a list of string integers
            dec_ = dec_message.split(', ')
            #converting the list of strings into a list of integers using the map function
            dec_message2 = list(map(int, dec_))
            n2 = int(input('What is the public n?\n'))
            #if user has the private key they can input it to decode, otherwise the program will use the brute_force_decode function
            priv_key = (input('Do you have the private key? y/n\n'))
            if priv_key == 'y':
                d2 = int(input('Please enter it now:\n'))
                print('The decoded message is, "{}"'.format (Decode(n2, d2, dec_message2)))
            elif priv_key == 'n':
                e = int(input('What is the public e?\n'))
                print('Please wait...')
                print('The decoded message is "{}"'.format ( brute_force_decode(n2, e, dec_message2)),"\n")
        #if user selects someting other than encode or decode
        else:
            print('Please enter "Encode" or "Decode"\n')
        #asking the user if they would like to continue 
        again = input('Would you like to continue? y/n\n')
        #if they do, the program starts again from the beginning
        if again == 'y':
            pass
        #if they don't, the program ends
        else:
            break
if __name__ == '__main__':
    main ()
    