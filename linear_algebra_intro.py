#!/usr/bin/env python3
"""
Created on Sat Aug  1 13:40:36 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
linear_algebra_intro.py — Linear algebra in NumPy, framed for power systems.

The mathematics is familiar from power engineering; only the NumPy notation is
new. Covers the three operations that carry Ax = b (load flow):
  * dot product        — ΣVI, three-phase power
  * matrix @ vector    — I = Y·V  (admittance matrix acting on voltages)
  * solve Ax = b       — recover voltages from injected currents (load flow)

Key habit: use np.linalg.solve, NOT np.linalg.inv, to solve a system —
faster and numerically more stable (matters for large/ill-conditioned Ybus).

Usage:  python linear_algebra_intro.py
"""
import numpy as np


def three_phase_power(V, I):
    """Total instantaneous power across phases = V · I (dot product)."""
    return V @ I


def bus_currents(Y, V):
    """I = Y · V — admittance matrix acting on the bus-voltage vector."""
    return Y @ V


def bus_voltages(Y, I):
    """Solve Y · V = I for V — the core of load-flow analysis.

    Uses solve (LU factorization), never inv: faster and more stable.
    """
    return np.linalg.solve(Y, I)


def main():
    # --- dot product: three-phase power ---
    V3 = np.array([230, 231, 229])  # volts
    I3 = np.array([10, 12, 11])  # amps
    print("Three-phase power:", three_phase_power(V3, I3), "W")

    # --- a small symmetric admittance-like matrix ---
    Y = np.array(
        [
            [2, 1, 0],
            [1, 3, 1],
            [0, 1, 2],
        ]
    )
    V = np.array([1, 2, 3])  # bus voltages

    # forward: voltages -> currents
    I = bus_currents(Y, V)
    print("Injected currents  I = Y·V:", I)

    # inverse: currents -> voltages (recovers V, the round trip)
    V_recovered = bus_voltages(Y, I)
    print("Recovered voltages via solve:", V_recovered)


if __name__ == "__main__":
    main()
