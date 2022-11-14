#!/usr/bin/env python

import math
import sys
from datetime import datetime
from mpmath import *
from textwrap import wrap
import re

"""I have commented this as I went, but up top here is a sort of explanation as to what we're doing.
Just know that I sometimes use "I" and "we" interchangable. I'm really not sure why, but it feels weird to say "I". So if you see "we," it's just me working on it, 
but to me it's more comfortable to say "we" as if you, the reader, are following along with me. 

1) First, we are grabbing the day, month and year. Those will become integers.
2) We will then multiple the month by 5 to have a larger number. The large number will be the number of digits we will drag "pi" out to. We are aiming for 50+. 
EDIT - after trying this, I had to up the number of iterations quite a few. Even with a string of characters 400+ long, I might still only retrieve 10 or so usable characters. 
So, I changed it from 5 to 357
3) We will drag out this number to pi to that number of places. 
4) We will then discard the "3." part of it, using only the tenths on down. 
5) We will break that really long number into 2 parts, right down the middle. This accounts for any mixed digits, but frankly, it doesn't matter either way.
6) We will then add those together and, just like the Fibonacci sequence, will continue to add the previous number to the "new number," then add the previous number to the new number, and so forth.
    for instance, instead of 0, 1, 1, 2, 3, 5, 8...... We might start with seeds 111 and 354 (our numbers will be much higher, but the point is to show the process without using standard Fibonacci numbers)
    111, 354, 465, 819, 1284, 2103, 
7) We continue this sequence 42 times because Douglas Adams. We need a large-ish number to work with. We want our final seed to be 60+ chars.

    We will repeat this 10 more times, from range 42-52. Each iteration ends in a domain
8) Regardless of what our numbers is, as long as it is over 60 chars, we will take the last 60 chars (because why take the first 60? That's no fun)
    Based on testing, it will ALWAYS be over 60 chars.
    Of the last 60 characters, we will break it into chunks of 4 (which are actually 2 chunks of 2). Every other block of two will be used,
    and the second block of two will be "in reserve" in case the first one creates a vowel. 
    so, for instance, 0195 will use the 01 value, and hold the 95 in reserve, in case chr(01) produces a/e/i/o/u. 
9) After using the 60 characters and converting them to a domain, we will append the tlds for our final product. 

"""


# Importing the day, month and year. 
#We are going to use these to find a "nth" spot of pi, then use those two numbers to generate our own flavor of a fibonacci sequence. 
day = int(datetime.now().day)
month = int(datetime.now().month)


#This becomes a little less predictable if we use lower numbers fro the month, like 3. So, if the number is a single digit month, append a 0.
# This created a little monstrosity because we can only append strings, not integers
#So I had to concatenate two strings, then use the "int" in front of it. I laughed a little at this, but ti works. (shrugs)
#For the purposes of this assignment, I didn't really need to exit the month - but I did want to solve it for my own curiosity and to do it RIGHT, so I hard coded in January and made sure it worked as advertised.
if month <=10:
    month = int((str(month) + str(0)))
    print(f"The new month is {month}.")
year = int(datetime.now().year)

#This is mostly for me to see while I'm writing it. 
print(f"[+] The day is {day}\n[+] The month is {month}\n[+] The year is {year}\n")

#This is where we use the month to find the nth spot for pi.
#The first line is defining how many places to drag out pi. In this specific case, it's 11 * 3, or 33.
#That resulted in "3.1415926535897932384626433832795"
mp.dps = (month * 357)
#Update - modified this to 13 to have more digits to work with.
#We needed a LOT more

#print("[-]The string we are working with is : " + (str(+mp.pi))+"\n")
#What we're going to do here is take our pi string - AKA seed_string - and create two longer numbers, seed, and seed2. 
#After that, we will use those numbers below for our own Fibonacci-like sequence.
seed_string = str(+mp.pi)
split_seed = seed_string.split(".")[-1]
print(f"[-] The split seed string is {split_seed}.\n\n[-] We only want whats after the 3 and the period.\n")

#Let's take that long number and split it in half. I really don't care if they match or not, as long as it's consistent across programs. 
seed = split_seed[:len(split_seed)//2]
seed2 = split_seed[len(split_seed)//2:]
print(f"[-] The first seed is {seed}\n\n[-] The second is {seed2}\n\n")




'''Now that we have our seed values, let's put them into our little machine,
This will create a truly massive number, and grab the first 12 "actionable" characters.
This will also have to re-format several times, but I tried to comment it enough to make it very obvious what I'm doing. 
For a very long number (e.g. 1950 digits) we will convert it to int base 16, grab 3 at a time, and then strain out all that are numbers and letters.
After we have a good list (20?) we will strain out the vowels and use the first 12 available characters.
'''

#These are the TLDs I are required to use for the assignment. I'm putting the dot here rather than appending the dot and then the tld at the end like I did in dga
#This just seems cleaner to me
tlds = [".csc840.lan", ".com", ".press", ".me", ".cc"]
list_of_domains=[]
#The tld_index is borrowed from ranybus. Something something standing on the shoulders of giants I guess?
tld_index = day

# generate fibonacci sequence
print(f"[*] Begining our self-made Fibonacci sequence using the first and second seeds\n")
for i in range(42,52):
    #print(seed)
    nth = int(seed) + int(seed2)
    # update values
    seed = seed2
    seed2 = nth
    #print(nth)
    #The "nth" number string is too long, so we have to convert it to list format
    #There is a lot going on here to format them just right. 
    #If I had more python experience, I could probably make this much smoother. But alas, I'm a hacker, not a dev, so a hack-ish solution is what we'll do :)
    
    actual_domains = []
    domains = list(str(nth)) 
    domains = ''.join(domains)
    #print(f"[!] The characterset is {(len(domains))} characters")
    #Cool, now they are printing nicely, and don't have all the commas and ticks between them from list format.
    #Now that it's in list format, we can peel off the back 60 characters.
    domain_candidates = []
    #Break our really long string into manageable chunks. The first 2 lines break apart the "final domain" info chunks of 2 numbers
    f = 3
    chunks = [domains[i:i+f] for i in range(0, len(domains), f)]
    #Next, let's convert back to int base 16 and concert to characters
    for j in chunks:
        new_number = int(j,16)
        new_letter = chr(new_number)
        if re.match("^[A-Za-z0-9_-]*$", new_letter):
            domain_candidates.append(new_letter)
    #print(f"The raw material string is {domain_candidates}")
    vowels = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
    no_vowels = ""
    for e in range(len(domain_candidates)):
        if domain_candidates[e] not in vowels:
            no_vowels = no_vowels + domain_candidates[e]
    print("\nAfter removing Vowels: ", no_vowels)
    usable_domain = no_vowels[0:12]
    print(f"The trimmed 12 characters are {usable_domain}")
    usable_domain += tlds[tld_index % (len(tlds) - 1)]
    tld_index += 1
    print(f"[!]The domain to add to DNS records is {usable_domain}\n")
   