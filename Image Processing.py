from PIL import Image
import math
from collections import Counter
import hashlib
import time
import matplotlib.pyplot as plt

def shannon_entropy(data):
    if not data:
        return 0.0
    counts = Counter(data)
    total = len(data)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def hash_mix(value, salt):

    data = f"{value}-{salt}".encode()
    digest = hashlib.sha256(data).hexdigest()
    return int(digest, 16) % 100

def get_entropy_columns(image_path, column_step=1, max_rows=100, top_k=5):

    img = Image.open(image_path)
    pixels = img.load()

    entropy_sets = []
    entropies = []

    for x in range(0, img.width, column_step):
        col_vals = []
        for y in range(img.height):
            r, g, b = pixels[x, y]
            avg_rgb = ((r << 16) + (g << 8) + b) % 100
            val = avg_rgb % 100  # last two digits
            col_vals.append(val)

        e = shannon_entropy(col_vals)
        entropy_sets.append(col_vals)
        entropies.append((e, col_vals))

    # Sort by entropy descending and return top K sets
    entropy_sets_sorted = sorted(entropies, key=lambda x: x[0], reverse=True)
    top_sets = [x[1] for x in entropy_sets_sorted[:top_k]]

    return top_sets

def generate_random_digit(n_prev, entropy_sets):

    salt = int(time.time_ns() % 100000)

    # Choose set based on hashed n_prev
    set_index = hash_mix(n_prev, salt) % len(entropy_sets)
    selected_set = entropy_sets[set_index]

    # Derive index from hash-mixed input
    idx = hash_mix(n_prev ^ salt, salt + 1) % len(selected_set)
    raw_val = selected_set[idx]

    # Final whitening
    result = hash_mix(raw_val, salt + 2)
    return (result, selected_set)


image_path = "image2.png"
entropy_sets = get_entropy_columns(image_path)
# Start with user input
n = int(input("Enter a number between 0 and 100: "))
history = [n]
history1 = [n/100*0.1]
m1 = len(entropy_sets[0])
L = [0]
m = 0
while m < m1:
    x = generate_random_digit(n, entropy_sets)
    n = x[0]
    history.append(n)
    history1.append(round(n / max(x[1]), 4))
    m+=1
    L.append(m)
historyappend = []
with open("floats.txt", 'w') as file:
        for i in history1:
            historyappend.append(str(i) + '\n')
        file.writelines(historyappend)
historyappend = []
with open('numbers.txt', 'w') as file:
        for i in history:
            historyappend.append(str(i) + '\n')
        file.writelines(historyappend)
print("File Write Completed. Exiting.")