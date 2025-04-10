#!/usr/bin/env python

def gcd(a, b):
    if a < b:
        a, b = b, a
    print("gcd", (a,b))
    while b != 0:
        r = a % b
        a = b
        b = r
    return a

a = int(input("input the first number: "))
b = int(input("input the second number: "))

print(f'gcd({a}, {b}) of {a}, {b} = {gcd(a, b)}')