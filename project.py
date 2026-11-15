import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

st.set_page_config(page_title="Signal Analysis & Transform Visualizer", page_icon="📡", layout="wide")
st.title("📡 Signal Analysis & Transform Visualizer")
st.write("Generate basic signals and explore their Fourier, Laplace and Z-transform views.")

with st.sidebar:
    st.header("Signal Settings")
    signal_type = st.selectbox("Select signal", ["Sine", "Cosine", "Square", "Exponential"])
    amplitude = st.slider("Amplitude", 0.5, 5.0, 1.0, 0.5)
    frequency = st.slider("Frequency (Hz)", 1, 20, 5)
    samples = st.slider("Number of samples", 64, 512, 256, 64)
    duration = st.slider("Duration (seconds)", 1, 5, 2)

fs = 100
t = np.arange(samples) / fs
if signal_type == "Sine":
    x = amplitude * np.sin(2 * np.pi * frequency * t)
elif signal_type == "Cosine":
    x = amplitude * np.cos(2 * np.pi * frequency * t)
elif signal_type == "Square":
    x = amplitude * signal.square(2 * np.pi * frequency * t)
else:
    x = amplitude * np.exp(-frequency * t / 5)

tab1, tab2, tab3, tab4 = st.tabs(["Signal Generator", "Fourier Transform", "Z-Transform", "Laplace & Poles-Zeros"])

with tab1:
    st.subheader("Time-domain signal")
    fig, ax = plt.subplots()
    ax.plot(t, x)
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Amplitude")
    ax.set_title(f"{signal_type} Signal")
    ax.grid(True)
    st.pyplot(fig)
    st.caption("The graph shows the selected signal against time.")

with tab2:
    st.subheader("Fourier Transform (FFT approximation)")
    X = np.fft.fft(x)
    freqs = np.fft.fftfreq(len(x), d=1/fs)
    positive = freqs >= 0
    magnitude = np.abs(X)[positive] / len(x)
    phase = np.angle(X)[positive]
    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots()
        ax.plot(freqs[positive], magnitude)
        ax.set_title("Magnitude Spectrum")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        ax.grid(True)
        st.pyplot(fig)
    with c2:
        fig, ax = plt.subplots()
        ax.plot(freqs[positive], phase)
        ax.set_title("Phase Spectrum")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Phase (radians)")
        ax.grid(True)
        st.pyplot(fig)
    st.info("FFT is used here as a numerical approximation of the Fourier transform for the sampled signal.")

with tab3:
    st.subheader("Discrete-Time Signal and Z-Transform")
    st.write("A finite-sample Z-transform is evaluated on the unit circle (z = e^jω).")
    n = np.arange(min(len(x), 128))
    xn = x[:len(n)]
    omega = np.linspace(-np.pi, np.pi, 512)
    z = np.exp(1j * omega)
    Z = np.array([np.sum(xn * np.exp(-1j * w * n)) for w in omega])
    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots()
        ax.stem(n, xn)
        ax.set_title("Discrete-Time Samples")
        ax.set_xlabel("n")
        ax.set_ylabel("x[n]")
        ax.grid(True)
        st.pyplot(fig)
    with c2:
        fig, ax = plt.subplots()
        ax.plot(omega, np.abs(Z))
        ax.set_title("Z-Transform Magnitude on Unit Circle")
        ax.set_xlabel("Angular frequency (rad/sample)")
        ax.set_ylabel("|X(z)|")
        ax.grid(True)
        st.pyplot(fig)
    st.caption("This is a finite-length numerical evaluation on |z| = 1. A complete ROC depends on the signal's definition and sidedness.")

with tab4:
    st.subheader("Laplace Transform: Poles and Zeros")
    st.write("Enter transfer-function coefficients in descending powers of s.")
    numerator_text = st.text_input("Numerator coefficients", "1")
    denominator_text = st.text_input("Denominator coefficients", "1, 3, 2")
    try:
        num = [float(v.strip()) for v in numerator_text.split(",")]
        den = [float(v.strip()) for v in denominator_text.split(",")]
        if not num or not den or all(v == 0 for v in den):
            raise ValueError("Enter valid non-zero denominator coefficients.")
        zeros, poles, gain = signal.tf2zpk(num, den)
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Zeros**")
            st.write(zeros if len(zeros) else "No finite zeros")
            st.write("**Poles**")
            st.write(poles if len(poles) else "No finite poles")
            st.write("**Gain**")
            st.write(float(gain))
        with c2:
            fig, ax = plt.subplots()
            ax.axhline(0, linewidth=1)
            ax.axvline(0, linewidth=1)
            if len(zeros):
                ax.scatter(np.real(zeros), np.imag(zeros), marker="o", facecolors="none", edgecolors="blue", label="Zeros")
            if len(poles):
                ax.scatter(np.real(poles), np.imag(poles), marker="x", color="red", label="Poles")
            ax.set_title("Pole-Zero Plot (s-plane)")
            ax.set_xlabel("Real")
            ax.set_ylabel("Imaginary")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)
        st.caption("For a continuous-time LTI system, poles are roots of the denominator and zeros are roots of the numerator.")
    except Exception as e:
        st.error(f"Please enter valid coefficients. Details: {e}")

st.divider()
st.subheader("Download signal data")
csv_data = "time,signal\n" + "\n".join(f"{ti:.6f},{xi:.6f}" for ti, xi in zip(t, x))
st.download_button("Download CSV", csv_data, file_name="signal_data.csv", mime="text/csv")
st.caption("Educational simulator: FFT and finite-sample Z-transform plots are numerical visualizations, not symbolic transform solvers.")
