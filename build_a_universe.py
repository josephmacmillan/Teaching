import scipy.integrate as integrate
import matplotlib.pyplot as plt
import numpy as np

Omega_m0 = 0.31
# Omega_l0 = 1.72897 # longest age ...
Omega_l0 = 1.1

# convert H0 to Gyrs
H0 = 68.0 / 3.086e+19 * (60*60*24*365*1e9)

# this is the integrand
def f(a):
    return 1.0 / np.sqrt(Omega_m0 / a + Omega_l0 * a**2 + (1.0 - Omega_m0 - Omega_l0))

# set up the integration
N = 1000
a = np.linspace(1e-5, 3.0, N)

t = np.zeros(N)
for i in range(N):
    t[i], err = integrate.quad(f, 1.0, a[i])

print(f"This universe is {-t[0]/H0} Gyrs old")

# plot the results as a(t)
plt.plot(t, a)
plt.xlabel("$H_0(t - t_0)$")
plt.ylabel("$a$")
plt.show()
