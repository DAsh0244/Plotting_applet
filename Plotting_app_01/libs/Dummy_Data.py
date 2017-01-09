import numpy as np

tmin = 0
tmax = 3
delta = .002  # sample period
frequency = 2  # signal freq in Hz
amplitude = 5  # signal amplitude
phase = 0  # phase angle in degrees
t = np.arange(tmin, tmax, delta)
Sine = amplitude * np.sin(frequency * np.pi * 2 * t + phase * np.pi / 180)  # make nice Hz instead of rads

sine = np.array ([128, 140, 152, 164, 173, 181, 187, 191,
                 192, 191, 187, 181, 173, 164, 152, 140,
                  128, 116, 104, 92, 83, 75, 69, 65,
                 64, 65, 69, 75, 83, 92, 104, 116])
square = np.array ([192, 192, 192, 192, 192, 192, 192, 192,
                     192, 192, 192, 192, 192, 192, 192, 192,
                      64, 64, 64, 64, 64, 64, 64, 64,
                      64, 64, 64, 64, 64, 64, 64, 64])
triangle = np.array([128, 136, 144, 152, 160, 168, 176, 184,
                       192, 184, 176, 168, 160, 152, 144, 136, 128,
                       120, 112, 104, 96, 88, 80, 72, 64,
                       72, 80, 88, 96, 104, 112, 120, 128])

# data = np.concatenate([sine, square,  sine, triangle, square, sine])
# data = np.concatenate([sine, sine,  sine, sine, sine, sine])
# data = np.concatenate([square, square,  square, square, square, square])
# data = np.concatenate([triangle, triangle,  triangle, triangle, triangle, triangle])

# fft_data = np.fft.rfft(len(Sine))
# freq_data = np.fft.rfftfreq(len(Sine), delta)
