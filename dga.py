#!/usr/bin/env python
#import datetime
import sys

#I took a little liberty porting this to python, but I used the same string if it failes

#The first thing it does is define dga, along with the vars day, month, year, seed. These args are parsed based on input. 
def dga(day, month, year, seed):
    #I don't actually need to declare variables in Python, but I will for funsies. The assignment states to be as close to C as possible
    #Yes, I said funsies. I would never do that ina  formal paper, but just because this is "class" doesn't mean it has to be boring :)
    d = None
    #This one is specificed in the C coding and I think needs to be here, too
    #I could probably hvae it be whatever I wanted and it wouldn't matter, but we'll stil with the day to have some kind of int value to start with
    tld_index = day
    #While the ranybus docs say NR is hard-coded to 40, I am going to cut it off at 10 due to the assignment requirements
    #I am also going to change to using a python range-based approach, rather than the traditional C "i=0, i<=, i++" approach
    for d in range(0,10):
        #We need an initialized list to append to here. I had some errors without doing that. 
        domain = []
        #I removed the "unsigned i" part here - Python knows it exists somehow, someway
        for i in range (0,14):
            #I just copied and pasted this. It *should* work.... at least in theory. Fingers crossed!
            day = (day >> 15) ^ 16 * (day & 0x1FFF ^ 4 * (seed ^ day))
            year = ((year & 0xFFFFFFF0) << 17) ^ ((year ^ (7 * year)) >> 11)
            month = 14 * (month & 0xFFFFFFFE) ^ ((month ^ (4 * month)) >> 8)
            seed = (seed >> 6) ^ ((day + 8 * seed) << 8) & 0x3FFFF00
            x = ((day ^ month ^ year) % 25) + 97
            #Now I have to append to the lsit, then do ti all over again. Also noteworthy is thatup to this poiint, it's an integer - and it needs to be a letter (ASCII)
            domain.append(chr(x))
        #Now we join each iteration together. Remember we have two loops going - one for 10 total domains, but also each domain has 14 rounds as well (0..14)
        #So, each round of 0-14 makes a singular domain. Rinse and repeat 10 times.
        domain = ''.join(domain)
        #These are the TLDs that are involved in created the domains. In the C code, there was an error due to the modulus being 8 rather than 9
        # But I am using a different approach because math using len is moar gooder.
        tlds =  ["in", "me", "cc", "su", "tw", "net", "com", "pw", "org"]
        #I did have to borrow this little snippet below from https://github.com/baderj/domain_generation_algorithms/blob/907dbe456fb995cff2071c273d89026524b5e78d/ranbyus/september/ranbyus_reloaded.py#L55
        #I could not find any other way to use the modulus, but honestly, there aren't that many ways to do this.
        # I tried to think of another way to do it, but I had about 90% of the same string myself and just needed 1 or two minor changes to get across the finish line. 
        domain += '.' + tlds[tld_index % (len(tlds) - 1)]
        tld_index += 1
        print(domain)


dga(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4], 16))