import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
nx, ny = 50, 50       # grid points
nt = 100              # number of time steps
dx = 1.0 / (nx - 1)
dy = 1.0 / (ny - 1)
dt = 0.001            # time step
rho = 1.0             # density
nu = 0.1              # kinematic viscosity

# Initialize velocity (u, v) and pressure (p)
u = np.zeros((ny, nx))
v = np.zeros((ny, nx))
p = np.zeros((ny, nx))

def build_up_b(u, v, dx, dy, dt, rho):
    b = np.zeros_like(u)
    b[1:-1,1:-1] = (rho * (1/dt *
                   ((u[1:-1,2:] - u[1:-1,0:-2]) / (2*dx) +
                    (v[2:,1:-1] - v[0:-2,1:-1]) / (2*dy)) -
                   ((u[1:-1,2:] - u[1:-1,0:-2]) / (2*dx))**2 -
                     2*((u[2:,1:-1] - u[0:-2,1:-1]) / (2*dy) *
                        (v[1:-1,2:] - v[1:-1,0:-2]) / (2*dx)) -
                     ((v[2:,1:-1] - v[0:-2,1:-1]) / (2*dy))**2))
    return b

def pressure_poisson(p, dx, dy, b, nit=50):
    pn = np.empty_like(p)
    for _ in range(nit):
        pn[:] = p[:]
        p[1:-1,1:-1] = (((pn[1:-1,2:] + pn[1:-1,0:-2])*dy**2 +
                         (pn[2:,1:-1] + pn[0:-2,1:-1])*dx**2) /
                        (2*(dx**2 + dy**2)) -
                        dx**2 * dy**2 / (2*(dx**2 + dy**2)) * b[1:-1,1:-1])
        # Boundary conditions
        p[:, -1] = p[:, -2]    # dp/dx = 0 at x = L
        p[:, 0] = p[:, 1]      # dp/dx = 0 at x = 0
        p[-1, :] = 0           # p = 0 at y = L
        p[0, :] = p[1, :]      # dp/dy = 0 at y = 0
    return p

# Main loop
for n in range(nt):
    un = u.copy()
    vn = v.copy()

    b = build_up_b(u, v, dx, dy, dt, rho)
    p = pressure_poisson(p, dx, dy, b)

    # Update velocities
    u[1:-1,1:-1] = (un[1:-1,1:-1] -
                     un[1:-1,1:-1] * dt / dx *
                     (un[1:-1,1:-1] - un[1:-1,0:-2]) -
                     vn[1:-1,1:-1] * dt / dy *
                     (un[1:-1,1:-1] - un[0:-2,1:-1]) -
                     dt / (2*rho*dx) *
                     (p[1:-1,2:] - p[1:-1,0:-2]) +
                     nu * (dt / dx**2 *
                     (un[1:-1,2:] - 2*un[1:-1,1:-1] + un[1:-1,0:-2]) +
                     dt / dy**2 *
                     (un[2:,1:-1] - 2*un[1:-1,1:-1] + un[0:-2,1:-1])))

    v[1:-1,1:-1] = (vn[1:-1,1:-1] -
                     un[1:-1,1:-1] * dt / dx *
                     (vn[1:-1,1:-1] - vn[1:-1,0:-2]) -
                     vn[1:-1,1:-1] * dt / dy *
                     (vn[1:-1,1:-1] - vn[0:-2,1:-1]) -
                     dt / (2*rho*dy) *
                     (p[2:,1:-1] - p[0:-2,1:-1]) +
                     nu * (dt / dx**2 *
                     (vn[1:-1,2:] - 2*vn[1:-1,1:-1] + vn[1:-1,0:-2]) +
                     dt / dy**2 *
                     (vn[2:,1:-1] - 2*vn[1:-1,1:-1] + vn[0:-2,1:-1])))

    # Boundary conditions (lid-driven cavity)
    u[0, :] = 0
    u[:, 0] = 0
    u[:, -1] = 0
    u[-1, :] = 1  # moving lid
    v[0, :] = 0
    v[-1, :] = 0
    v[:, 0] = 0
    v[:, -1] = 0

# Plot final velocity field
X, Y = np.meshgrid(np.linspace(0,1,nx), np.linspace(0,1,ny))
plt.quiver(X, Y, u, v)
plt.title("2D Lid-Driven Cavity Velocity Field")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
