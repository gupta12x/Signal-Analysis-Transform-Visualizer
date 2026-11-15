# Signal Analysis & Transform Visualizer

A beginner-friendly Python project for visualizing basic signals and introductory transform concepts.

## Features
- Generate sine, cosine, square and exponential signals
- View the signal in the time domain
- View FFT-based magnitude and phase spectra
- View discrete-time samples and a finite-sample Z-transform evaluation on the unit circle
- Enter transfer-function coefficients and view Laplace-domain poles and zeros
- Download generated signal samples as CSV

## Requirements
- Python 3.10 or newer
- Packages listed in `requirements.txt`

## Run on Windows
Open this folder in VS Code, then run:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run project.py
```

The app opens in your browser at the local address shown in the terminal.

## Note
This is an educational numerical visualizer. FFT is used as a numerical approximation for sampled signals, and the Z-transform display evaluates a finite sequence on the unit circle. It does not perform symbolic CTFT, Laplace, or ROC derivations.
