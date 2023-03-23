from collections import Counter

ip_list = ["1.1.1.1", "2.2.2.2", "4.4.4.4", "1.1.1.1", "2.2.2.2", "5.5.5.5", "1.1.1.1"]

test = Counter(ip_list)
'''
#using for loop 
for k, v in test.items():
    #print(k)#test to see if keys(IP's) display in the output.
    #print(v)#test to see if values(# times each IP is displayed) display in the output.
    if v > 1:#display any value greater than 1
        print(k)#display the IP that has listed more than 1 per the if statement above this line.
'''

#using comprehension as an alternative to the code above.
test = [k for k, v in Counter(ip_list).items() if v > 1]
print(test)