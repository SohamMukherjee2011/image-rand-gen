import math, random
from collections import Counter
from statsmodels.tsa.stattools import acf
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
#getting the data from the file
with open("floats_test.txt", 'r') as file:
    f = file.readlines()
    for i in range(len(f)):
        f[i] = float(f[i].strip())
    last_digits = []
    for t in f:
        fr_str = str(t).split(".")[1]
        dig = fr_str[-4:]
        last_digits.append(int(dig))
fl = [round(d / 9999, 4) for d in last_digits]
length = len(fl)
with open("test.txt", 'r') as file:
    history = file.readlines()
    for i in range(len(history)):
        history[i] = int(history[i].strip())
#OTHER TESTS

def shannon_entropy(data):
    if not data:
        return 0.0
    counts = Counter(data)
    total = len(data)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())
def runs_test(sequence):
    median = np.median(sequence)
    signs = ['+' if val > median else '-' for val in sequence]

    
    runs = 1
    for i in range(1, len(signs)):
        if signs[i] != signs[i-1]:
            runs += 1

    n1 = signs.count('+')
    n2 = signs.count('-')
    n = n1 + n2

    if n1 == 0 or n2 == 0:
        print("All values fall on one side of median — not suitable for test.")
        return

    expected = (2 * n1 * n2) / n + 1
    variance = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (n**2 * (n - 1))

    z = (runs - expected) / np.sqrt(variance)
    p_value = 2 * (1 - norm.cdf(abs(z)))

    print(f"Runs: {runs}")
    print(f"Expected Runs: {expected:.2f}")
    print(f"Z-score: {z:.2f}")
    print(f"P-value: {p_value:.4f}")

    if p_value < 0.05:
        print("Reject H₀ — sequence may not be random.")
    else:
        print("Fail to reject H₀ — sequence appears random.")

print("ENTROPY OF THE SET: ", shannon_entropy(history))
runs_test(history)
plt.hist(f, bins=50, edgecolor='black')
plt.title("Value Frequency Histogram")
plt.xlabel("Value (0-1)")
plt.ylabel("Frequency")
acf_vals = acf(history, nlags=20)
l, graph = plt.subplots()
graph.plot(acf_vals)
plt.title("Autocorrelation")
# plt.show()

#ENTANGLEMENT BEGINS FROM HERE:

# Parameters
theta_a = 0
theta_b = 45
n = int(input("Enter number of runs per trial:"))
runs = 10 #per major-run
diff = math.radians(theta_a - theta_b)
exp = math.cos(diff / 2) ** 2
print(f"Expected match: {exp * 100:.2f}%")

# mustn't choose in last seg
seq=2*n # = 4000valuesperrun
if len(fl) < seq:
    print("Entropy list too small.")
    exit()

g = 0
start = 0
#marco polo model
for i in range(runs):
    #Random start index that gives enough space for 4000 values
    # start = random.randint(0, len(fl) - 2000)
    m = 0

    for j in range(n):
        if (start + 2*j + 1) < length:
                x = fl[start + 2*j]
                y = fl[start + 2*j + 1]

                if x < exp:
                    a = b = 0 if y < 0.5 else 1

                else:
                    a,b=(0,1) if y < 0.5 else (1,0)
                if a == b:
                    m+=1
        else:
            break
    pr = (m/n)*100
    print(f"Run {i+1}: {pr:2f}% match")
    start += length//runs
    g+=pr

print(f"Avg: {g/runs:.2f}%")


runs = 10
step = 5

angles = list(range(0, 181, step))
theort_ = []
measured = []

req_seq = 2*n

if len(fl) < req_seq:
    print("Entropy list too small")
    exit()

for theta in angles:
    diff = math.radians(theta)
    exp = math.cos(diff/2)**2
    theort_.append(exp*100)

    g = 0
    start = 0
    for _ in range(runs):
        # start = random.randint(0, len(fl) - 2000)
        m = 0
        for j in range(n):
            if (start + 2*j + 1) < length:
                x = fl[start + 2*j]
                y = fl[start + 2*j + 1]

                if x < exp:
                    a = b = 0 if y < 0.5 else 1

                else:
                    a,b=(0,1) if y < 0.5 else (1,0)
                if a == b:
                    m+=1
            else:
                break
        pct = (m/n)*100
        g += pct
        start += length//runs
    avg = g/runs
    measured.append(avg)

#Plotting
plt.figure(figsize = (10,6))
plt.plot(angles, theort_, label = 'Quantum Prediction (cos^2)', color = 'teal', linewidth = 4)
plt.plot(angles, measured, label = 'Measured from entropy', color = 'coral', linestyle = '--', marker = 'o')
plt.xlabel('Angle(degrees)')
plt.ylabel('Match percentage')
plt.title('match vs angle')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
