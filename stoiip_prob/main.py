import numpy as np
import matplotlib.pyplot as plt
from stoiip_prob.stoiip import stoiip
from scipy.stats import expon, lognorm, norm, triang, uniform

# %% Define input variables
h = 12
A = 450
poro = 0.15
swc = 0.35
boi = 1.1

# %% Calculate STOIIP

print(stoiip(A, h, poro, swc, boi))

# %% Defined Arrays for STOIIP

area = np.array([450.0, 500.0, 550.0])
h = np.array([30.0, 40.0, 50.0])
poro = np.array([0.12, 0.14, 0.16])
swc = np.array([0.30, 0.35, 0.40])
boi = np.array([1.01, 1.1, 1.12])

print(np.around(stoiip(area, h, poro, swc, boi), 2))

# %% Create random values for each distribution

norm_values = norm.rvs(loc=0.5, scale=0.3, size=1000)
expon_values = expon.rvs(loc=0, scale=0.3, size=1000)
lognorm_values = lognorm.rvs(s=0.95, size=1000)
triang_values = triang.rvs(c=0.3, loc=0, scale=1, size=1000)
unif_values = uniform.rvs(loc=0, scale=2, size=1000)

# %% Define values for porosity according to each distribution

porosity_norm = norm_values[np.logical_and(norm_values >= 0, norm_values <= 0.4)]
porosity_exp = expon_values[np.logical_and(expon_values >= 0, expon_values <= 0.4)]
porosity_log = lognorm_values[np.logical_and(lognorm_values >= 0, lognorm_values <= 0.4)]
porosity_tria = triang_values[np.logical_and(triang_values >= 0, triang_values <= 0.4)]
porosity_unif = unif_values [np.logical_and(unif_values >= 0, unif_values <= 0.4)]
print(porosity_unif)

# %% Define values for saturation according to each distribution

saturation_norm = norm_values[np.logical_and(norm_values >= 0, norm_values <= 1)]
saturation_exp = expon_values[np.logical_and(expon_values >= 0, expon_values <= 1)]
saturation_log = lognorm_values[np.logical_and(lognorm_values >= 0, lognorm_values <= 1)]
saturation_tria = triang_values[np.logical_and(triang_values >= 0, triang_values <= 1)]

# %% Plotting distribution for porosity and saturation

# plt.hist(porosity_norm)
# plt.show()

# %% Define values for Boi according to each distribution

boi_norm = norm_values[np.logical_and(norm_values >= 1, norm_values <= 2)]
boi_exp = expon_values[np.logical_and(expon_values >= 1, expon_values <= 2)]
boi_log = lognorm_values[np.logical_and(lognorm_values >= 1, lognorm_values <= 2)]
boi_triag = triang_values[np.logical_and(triang_values >= 1, triang_values <= 2)]
boi_unif = unif_values[np.logical_and(unif_values >= 1, unif_values <= 2)]

# %% Generating random values for thicknes and area variables

norm_val2 = norm.rvs(loc=50, scale=100, size=1000)
expon_val2 = expon.rvs(loc=50, scale=100, size=1000)
lognorm_val2 = lognorm.rvs(s=0.95, loc=50, scale=100, size=1000)
triang_val2 = triang.rvs(c=0.3, loc=5, scale=10, size=1000)
unif_val2 = uniform.rvs(loc=1, scale=500, size=1000)

# %% Define values for area according to each distribution

area_norm = norm_val2[np.where(norm_val2 >= 0)]
area_exp = expon_val2[np.where(expon_val2 >= 0)]
area_log = lognorm_values[np.where(lognorm_values >= 0)]
area_triag = triang_val2[np.where(triang_val2 >= 0)]
area_unif = unif_val2[np.logical_and(unif_val2 >= 50, unif_val2 <= 500)]


# %% Define values for thickness according to each distribution

thickness_norm = norm_val2[np.where(norm_val2 >= 0)]
thickness_exp = expon_val2[np.where(expon_val2 >= 0)]
thickness_log = lognorm_val2[np.where(lognorm_val2 >= 0)]
thickness_triag = triang_val2[np.where(triang_val2 >= 0)]
thickness_unif = unif_val2[np.logical_and(unif_val2 >= 1, unif_val2 <= 100)]

# %% Plotting the distributions

# plt.hist(thickness_unif)
# plt.show()





