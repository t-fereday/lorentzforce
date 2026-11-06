import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
import scipy.constants
from scipy.integrate import solve_ivp

mass = scipy.constants.m_p #kg
position = [0, 0, 0] #m
velocity = [0, 10, 0] #m/s
charge = scipy.constants.e #C


def b(x, y, z):
  
  b = np.array([0, 0, 1]) #T

  return b

def e(x, y, z):
  
  e = np.array([0, 1, 0]) #V/m

  return e


def lorentz_force(q, v, E, B):
    v = np.array(v)
    E = np.array(E)
    B = np.array(B)
    force = q * (E + np.cross(v, B))
    return force

def f(t, state, m, q):
   x, y, z, vx, vy, vz = state
   pos = state[0:3]
   vel = state[3:6]
   B_field = b(pos[0], pos[1], pos[2])
   E_field = e(pos[0], pos[1], pos[2])
   force = lorentz_force(q, vel, E_field, B_field)
   return np.concatenate([vel, force/m])

tau_c = (2*scipy.constants.pi*mass)/(abs(charge)*np.linalg.norm(b(position[0], position[1], position[2])))
sol = solve_ivp(f, (0,5*tau_c), np.concatenate([position, velocity]), args=(mass, charge),  max_step=tau_c/200, atol=10**(-15),rtol=10**(-15))

for i in range (3):
   print(sol.y[i])
print(f"period: {tau_c}")

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

t = np.linspace(0, 5*tau_c, 1000)
ax.plot(sol.y[0]*1e9, sol.y[1]*1e9, sol.y[2]*1e9)

ax.set_xlabel("x [nm]")
ax.set_ylabel("y [nm]")
ax.set_zlabel("z [nm]")
plt.show()










# def step(p, v, m, q, steptime):
#     B_field = b(p[0], p[1], p[2])
#     E_field = e(p[0], p[1], p[2])
#     force = lorentz_force(q, v, E_field, B_field)
#     accel = force/m
#     velocity = solve_ivp(accel, steptime, np.array(v))
#     position = solve_ivp(velocity, steptime, np.array(p))

#     return position, velocity


# for i in range (5):
#    print(f"velocity_{i}:{step(position, velocity, mass, charge, tstep)[1]}")
#    position, velocity = step(position, velocity, mass, charge, tstep)