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

# %% Defining random values for porosity from norm_values variable

# Normal distribution
norm_values = norm.rvs(loc=0.2, scale=0.3, size=1000)
porosity_norm = np.where(norm_values < 0, 0, norm_values)
porosity_norm = np.where(porosity_norm > 0.4, 0.4, porosity_norm)

# Exponential distribution
expon_values = expon.rvs(loc=0, scale=0.1, size=1000)
porosity_exp = np.where(expon_values < 0, 0, expon_values)
porosity_exp = np.where(expon_values > 0.4, 0.4, expon_values)

# Lognormal distribution
lognorm_values = lognorm.rvs(s=0.8, loc=0, scale=0.2, size=1000)
porosity_log = np.where(lognorm_values < 0, 0, lognorm_values)
porosity_log = np.where(lognorm_values > 0.4, 0.4, lognorm_values)

# Triangular distribution
triang_values = triang.rvs(c=0.3, loc=0, scale=0.4, size=1000)
porosity_tria = np.where(triang_values < 0, 0, lognorm_values)

# Uniform distribution
porosity_unif = uniform.rvs(loc=0, scale=0.4, size=1000)

# %% Define values for saturation according to each distribution

# Normal distribution
saturation_norm = norm.rvs(loc=0.4, scale=0.2, size=1000)
saturation_norm = np.where(saturation_norm < 0, 0, saturation_norm)
saturation_norm = np.where(saturation_norm > 1, 1, saturation_norm)

# Exponential distribution
saturation_exp = expon.rvs(loc=0, scale=0.2, size=1000)
saturation_exp = np.where(saturation_exp < 0, 0, saturation_exp)
saturation_exp = np.where(saturation_exp > 1, 1, saturation_exp)

# Lognormal distribution
saturation_log = lognorm.rvs(s=0.8, loc=0, scale=0.2, size=1000)
saturation_log = np.where(saturation_log < 0, 0, saturation_log)
saturation_log = np.where(saturation_log > 1, 1, saturation_log)

# triangular distribution
saturation_tria = triang.rvs(c=0.3, loc=0, scale=1, size=1000)

# %% Define values for Boi according to each distribution

# Normal distribution
boi_norm = norm.rvs(loc=1.5, scale=0.5, size=1000)
boi_norm = np.where(boi_norm < 1, 1, boi_norm)
boi_norm = np.where(boi_norm > 2, 2, boi_norm)

# Exponential distribution
boi_exp = expon.rvs(loc=1, scale=0.2, size=1000)
boi_exp = np.where(boi_exp < 1, 1, boi_exp)
boi_exp = np.where(boi_exp > 2, 2, boi_exp)

# Lognormal distribution
boi_log = lognorm.rvs(s=0.7, loc=1, scale=0.2, size=1000)
boi_log = np.where(boi_log < 1, 1, boi_log)
boi_log = np.where(boi_log > 2, 2, boi_log)

# Triangular distribution
boi_tria = triang.rvs(c=0.3, loc=1, scale=1, size=1000)

# Uniform distribution
boi_unif = uniform.rvs(loc=1, scale=1, size=1000)

# %% Define values for area according to each distribution

# Normal distribution
area_norm = norm.rvs(loc=190, scale=100, size=1000)
area_norm = np.where(area_norm < 50, 50, area_norm)

# Exponential distribution
area_exp = expon.rvs(loc=50, scale=100, size=1000)

# Lognormal distribution
area_log = lognorm.rvs(s=0.8, loc=50, scale=100, size=1000)

# Triangular distribution
area_triag = triang.rvs(c=0.3, loc=50, scale=450, size=1000)

# Uniform distribution
area_unif = uniform.rvs(loc=50, scale=500, size=1000)

# %% Define values for thickness according to each distribution

# Normal distribution
thickness_norm = norm.rvs(loc=50, scale=70, size=1000)
thickness_norm = np.where(thickness_norm < 0, 0, thickness_norm)
thickness_norm = np.where(thickness_norm > 180, 180, thickness_norm)

# Exponential distribution

thickness_exp = expon.rvs(loc=0, scale=50, size=1000)
thickness_exp = np.where(thickness_exp > 180, 180, thickness_exp)

# Lognormal distribution
thickness_log = lognorm.rvs(s=0.6, loc=0, scale=40, size=1000)

# Triangular distribution
thickness_tria = triang.rvs(c=0.3, loc=0, scale=150, size=1000)

# Uniform distribution
thickness_unif = uniform.rvs(loc=0, scale=200, size=1000)

# %% Plotting the distributions

# plt.hist(thickness_unif)
# plt.show()





