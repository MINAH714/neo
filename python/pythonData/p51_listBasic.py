#!/usr/bin/env python

somelist = ['김의찬', '유만식', '주서연', '정민아', '심수련', '이단비', '윤기석']

print(somelist)
print(somelist[4])
print(somelist[-2])
print(somelist[1:4])
print(somelist[4:])
length = len(somelist)
print(f'length of list : {length}')
print(somelist[:length:2])
print(somelist[1:length:2])