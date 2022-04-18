import numpy as np
# from stoiip_prob import stoiip as stp
from stoiip_prob.stoiip import stoiip

#%% Define input variables
h = 12
A = 450
poro = 0.15
swc= 0.35
boi = 1.1

#%% Calculate STOIIP

# print(stp.stoiip(A, h, poro, swc, boi))
print(stoiip(A, h, poro, swc, boi))

#%% Defined Arrays for STOIIP

area = np.array([450.0, 500.0, 550.0])
h = np.array([30.0, 40.0, 50.0])
poro = np.array([0.12, 0.14, 0.16])
swc = np.array([0.30, 0.35, 0.40])
boi = np.array([1.01, 1.1, 1.12])

# print(np.around(stp.stoiip(area, h, poro, swc, boi), 2))
print(np.around(stoiip(area, h, poro, swc, boi), 2))