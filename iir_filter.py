import numpy as np

class iir_filter:
    def __init__(self, b, a):
        """
        Initialize the IIR filter.

        Parameters:
        b (array-like): Numerator coefficients of the filter.
        a (array-like): Denominator coefficients of the filter.
        """
        self.b = np.array(b)
        self.a = np.array(a)
        self.x_hist = np.zeros(len(self.b))
        self.y_hist = np.zeros(len(self.a) - 1)

    def filter(self, x):
        """
        Apply the IIR filter to the input signal x using the standard IIR difference equation.

        Parameters:
        x (array-like): Input signal.

        Returns:
        y (ndarray): Filtered output signal.
        """
        x = np.asarray(x)
        y = np.zeros_like(x, dtype=float)
        for i in range(len(x)):
            # Compute y[n] using the IIR difference equation:
            # y[n] = (b[0]*x[n] + b[1]*x[n-1] + ... + b[M]*x[n-M]
            #         - a[1]*y[n-1] - ... - a[N]*y[n-N]) / a[0]
            x_terms = 0.0
            for j in range(len(self.b)):
                if i - j >= 0:
                    x_terms += self.b[j] * x[i - j]
            y_terms = 0.0
            for k in range(1, len(self.a)):
                if i - k >= 0:
                    y_terms += self.a[k] * y[i - k]
            y[i] = (x_terms - y_terms) / self.a[0]
        return y
