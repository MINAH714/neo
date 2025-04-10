#!/usr/bin/env python

a = int(input("input the first number: "))
b = int(input("input the second number: "))

def gcd(a, b):
    print("gcd", (a,b))
    while b != 0:
        r = a % b
        a = b
        b = r
    return a

print(f'gcd({a}, {b}) of {a}, {b} = {gcd(a, b)}')