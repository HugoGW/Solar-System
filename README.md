# Solar System Simulator — 2D Gravitational N-Body Simulation

This project simulates the motion of the eight planets of the Solar System using **Newtonian mechanics**, considering **mutual gravitational interactions** and optimized with **`numba`** to accelerate the numerical integration.

Rather than relying on analytical Keplerian solutions, we solve the full system of differential equations numerically, allowing us to observe effects such as **planetary perturbations** and accurately reflect elliptical orbits and relative mass influences.

---

## Physics Behind the Simulation

We solve Newton’s second law for a gravitationally interacting N-body system:

$$
\sum_k \vec{F}_k = m \vec{a} \quad \Rightarrow \quad \vec{a} = \frac{d^2\vec{r}}{dt^2} =  -G \sum \frac{m_j (\vec{r}_i - \vec{r}_j)}{|\vec{r}_i - \vec{r}_j|^3}
$$

where $j \neq i$. For each planet $i$, this includes:

* The attraction by the **Sun** (at the origin)
* The attractions by all other **planets**

In Cartesian coordinates, this gives for planet $i$:

$$
\frac{d^2x_i}{dt^2} = -G M_{\odot} \frac{x_i}{r_i^3} + \sum_{j \neq i} G m_j \frac{x_j - x_i}{|\vec{r}_j - \vec{r}_i|^3}
$$

$$
\frac{d^2y_i}{dt^2} = -G M_{\odot} \frac{y_i}{r_i^3} + \sum_{j \neq i} G m_j \frac{y_j - y_i}{|\vec{r}_j - \vec{r}_i|^3}
$$

Where $r_i = \sqrt{x_i^2 + y_i^2}$ is the distance from the Sun.

> **Note**: In a previous version, Mercury’s perihelion precession was artificially introduced. This version uses purely Newtonian physics without additional relativistic corrections.

---

## Implementation Highlights

* **Numerical Integration**: Using `scipy.integrate.odeint` for time integration.
* **Acceleration**: Core differential equation function accelerated with `@numba.njit`.
* **2D Visualization**: Real-time orbital animation with `matplotlib.animation`.
* **Interactive**: Hovering over planets or their orbits shows physical details (mass, speed, distance, blackbody temperature, etc.).

---

## 🪐 Planetary Parameters

Each planet is defined by:

* Semi-major axis $a$ (m)
* Eccentricity $e$
* Visual color
* Display size
* Mass $m$ (kg)

```python
params = {
    'Mercury': (57.91e9, 0.2056, 'gray', 0.13, 3.30e23),
    'Venus': (108.2e9, 0.0068, 'yellow', 0.5, 4.87e24),
    'Earth': (1.496e11, 0.0167, 'royalblue', 0.5, 5.972e24),
    'Mars': (227.9e9, 0.0934, 'red', 0.4, 6.42e23),
    'Jupiter': (778.3e9, 0.049, 'orange', 1.5, 1.898e27),
    'Saturn': (1.42e12, 0.056, 'gold', 1.3, 5.68e26),
    'Uranus': (2.87e12, 0.046, 'lightseagreen', 0.8, 8.68e25),
    'Neptune': (4.5e12, 0.010, 'blue', 0.8, 1.02e26)
}
```

Initial conditions use:

* $x_0 = a(1 - e)$
* $v_0 = \sqrt{\frac{GM_\odot(1 + e)}{a(1 - e)}}$

This places the planet at perihelion with appropriate tangential speed.

---

## 🖥 Output

### Animation

* Trajectories of all 8 planets
* Central Sun (static)
* Color-coded orbits and real-time position markers
* Clock showing simulation time (in Earth years)
* Planet hover tooltips displaying:

  * Orbital period (in days and years)
  * Instantaneous orbital speed
  * Distance to the Sun (in AU and km)
  * Estimated blackbody equilibrium temperature
  * Planetary mass (with comparison to Earth)

### Screenshots

| Orbits                                                                                             | Positions                                                                                          | Interactivity                                                                                      |
| -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| ![1](https://github.com/HugoGW/Solar-System/assets/140922475/1aa5cc5d-84fa-43ad-91c3-39e60f23185c) | ![2](https://github.com/HugoGW/Solar-System/assets/140922475/0e627381-3d16-4abd-bafc-51fdfed01820) | ![3](https://github.com/HugoGW/Solar-System/assets/140922475/8501f7d6-527e-4c95-84e0-b27e7086279f) |

---

## ⏱ Performance Tips

* The system is accelerated with `numba` for faster computations.
* You can reduce the time resolution (`t_values`) or number of simulated bodies for faster previews.
* The full simulation spans **two Neptune orbits** (\~330 years).

---

## Features Recap

* ✔ Mutual gravitational perturbations
* ✔ Per-planet orbital characteristics
* ✔ Realistic elliptical orbits
* ✔ Sun hover info (radius, temperature, mass)
* ✔ Dynamic tooltips and distance units
* ✔ Clean visual layout with black background and color coding

---

## Possible Extensions

* Include Pluto or asteroid belts
* Add relativistic precession (for Mercury)
* Implement zoom/pan interface
* Export to video with `FFMpegWriter`
* Build a 3D version using `plotly` or `pyvista`

---

## Requirements

* Python 3.8+
* `numpy`
* `scipy`
* `matplotlib`
* `numba`

