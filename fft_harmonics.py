#!/usr/bin/env python3
"""
Created on Sat Aug  1 22:09:31 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
fft_harmonics.py — FFT for power-quality analysis: spectrum + THD.

The complete pipeline a power-quality analyser runs:
  build/sample a waveform -> FFT -> read the harmonic peaks -> compute THD.
Saves two figures: the time-domain waveform and the frequency spectrum.

Also: eigenvalues via np.linalg.eig (modal analysis / small-signal stability —
stable iff every eigenvalue has a negative real part).

Usage:  python fft_harmonics.py
"""
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")  # non-interactive backend: save files, no window
import matplotlib.pyplot as plt

OUTDIR = "reports"


def make_signal(fs, duration, components):
    """Build a signal from (frequency_hz, amplitude) components.

    components: list of (freq, amp) tuples, e.g. [(50, 1.0), (150, 0.3)]
    Returns (t, signal).
    """
    t = np.arange(0, duration, 1 / fs)
    signal = np.zeros_like(t)
    for freq, amp in components:
        signal += amp * np.sin(2 * np.pi * freq * t)
    return t, signal


def spectrum(signal, fs):
    """Return (freqs, amplitudes) for the positive-frequency half, scaled to
    real amplitude."""
    n = len(signal)
    fft_result = np.fft.fft(signal)
    freqs = np.fft.fftfreq(n, 1 / fs)
    half = n // 2
    amplitude = np.abs(fft_result[:half]) * 2 / n
    return freqs[:half], amplitude


def amplitude_at(freqs, amps, target_hz):
    """Amplitude of the spectral bin nearest target_hz."""
    return amps[np.argmin(np.abs(freqs - target_hz))]


def thd(freqs, amps, fundamental_hz=50, n_harmonics=10):
    """Total Harmonic Distortion = sqrt(sum of harmonic^2) / fundamental."""
    fund = amplitude_at(freqs, amps, fundamental_hz)
    harmonics = [
        amplitude_at(freqs, amps, fundamental_hz * k) for k in range(2, n_harmonics + 1)
    ]
    return np.sqrt(np.sum(np.square(harmonics))) / fund


def plot_waveform(t, signal, path):
    """Time-domain plot of the sampled waveform."""
    plt.figure(figsize=(10, 3))
    plt.plot(t, signal)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Time domain — sampled waveform")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def plot_spectrum(freqs, amps, path, xmax=300):
    """Frequency-domain plot (the FFT spectrum)."""
    plt.figure(figsize=(10, 3))
    plt.stem(freqs, amps)
    plt.xlim(0, xmax)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title("Frequency spectrum — FFT")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def stability_eigenvalues(A):
    """Eigenvalues of a system matrix; stable iff all real parts < 0."""
    vals = np.linalg.eig(A)[0]
    stable = np.all(vals.real < 0)
    return vals, stable


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    fs = 5000
    t, sig = make_signal(fs, 0.1, [(50, 1.0), (150, 0.3)])
    freqs, amps = spectrum(sig, fs)

    # save both figures
    wave_path = os.path.join(OUTDIR, "fft_waveform.png")
    spec_path = os.path.join(OUTDIR, "fft_spectrum.png")
    plot_waveform(t, sig, wave_path)
    plot_spectrum(freqs, amps, spec_path)

    print("50 Hz amplitude: ", round(amplitude_at(freqs, amps, 50), 3))
    print("150 Hz amplitude:", round(amplitude_at(freqs, amps, 150), 3))
    print(f"THD = {thd(freqs, amps)*100:.2f}%")
    print(f"Saved: {wave_path}")
    print(f"Saved: {spec_path}")

    A = np.array([[4.0, 1.0], [2.0, 3.0]])
    vals, stable = stability_eigenvalues(A)
    print("\nEigenvalues:", vals, "| stable?", stable)


if __name__ == "__main__":
    main()
