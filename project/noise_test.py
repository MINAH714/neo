import random

def noisy_exponential(x, a=1, k=0.1, noise_level=0.1):
    base = a * math.exp(k * x)
    noise = random.uniform(-noise_level, noise_level) * base
    return base + noise

for x in range(11):
    print(f"x={x}, y={noisy_exponential(x):.2f}")