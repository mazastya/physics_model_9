from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask("__name__")


def amplitude_modulation(carrier_freq, signal_freq, modulation_index, duration, sampling_rate):
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    carrier_signal = np.sin(2 * np.pi * carrier_freq * t)
    info_signal = np.sin(2 * np.pi * signal_freq * t)
    modulated_signal = (1 + modulation_index * info_signal) * carrier_signal
    carrier_spectrum = np.fft.fft(carrier_signal)
    info_spectrum = np.fft.fft(info_signal)
    modulated_spectrum = np.fft.fft(modulated_signal)
    freqs = np.fft.fftfreq(len(t), 1 / sampling_rate)

    return t, carrier_signal, info_signal, modulated_signal, freqs, carrier_spectrum, info_spectrum, modulated_spectrum


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/amplitude_modulation', methods=['POST'])
def perform_amplitude_modulation():
    if request.method == 'POST':
        carrier_freq = float(request.form['carrier_freq'])
        signal_freq = float(request.form['signal_freq'])
        modulation_index = float(request.form['modulation_index'])
        duration = float(request.form['duration'])
        sampling_rate = float(request.form['sampling_rate'])

        t, carrier_signal, info_signal, modulated_signal, freqs, carrier_spectrum, info_spectrum, modulated_spectrum = amplitude_modulation(
            carrier_freq, signal_freq, modulation_index, duration, sampling_rate)

        # Plotting
        fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 8))

        axes[0, 0].plot(t, carrier_signal)
        axes[0, 0].set_title('Несущий сигнал')
        axes[0, 0].set_xlabel('Время (t)')
        axes[0, 0].set_ylabel('Амплитуда (B)')

        axes[0, 1].plot(freqs, np.abs(carrier_spectrum))
        axes[0, 1].set_title('Спектр несущего сигнала')
        axes[0, 1].set_xlabel('Частота (рад/сек)')
        axes[0, 1].set_ylabel('Магнитуда (B)')

        axes[1, 0].plot(t, info_signal)
        axes[1, 0].set_title('Информационный сигнал')
        axes[1, 0].set_xlabel('Время (t)')
        axes[1, 0].set_ylabel('Амплитуда (B)')

        axes[1, 1].plot(freqs, np.abs(info_spectrum))
        axes[1, 1].set_title('Спектр информационного сигнала')
        axes[1, 1].set_xlabel('Частота (рад/сек)')
        axes[1, 1].set_ylabel('Магнитуда (B)')

        axes[2, 0].plot(t, modulated_signal)
        axes[2, 0].set_title('Модуляционный сигнал')
        axes[2, 0].set_xlabel('Время (t)')
        axes[2, 0].set_ylabel('Амплитуда (B)')

        axes[2, 1].plot(freqs, np.abs(modulated_spectrum))
        axes[2, 1].set_title('Спектр модулированного сигнала')
        axes[2, 1].set_xlabel('Частота (рад/сек)')
        axes[2, 1].set_ylabel('Магнитуда (B)')

        plt.tight_layout()

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        plt.close()

        return render_template('result.html', plot_url=plot_url)


if __name__ == '__main__':
    app.run(debug=True)
