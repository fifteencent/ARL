from manimlib.imports import *
from ARL.kalman.custom_graph import *

class TrueModel():
    def __init__(self, A, Q):
        self.A = A
        self.Q = Q
        (m, _) = Q.shape
        self.mean = np.zeros(m)

    def __call__(self, x):
        state = self.A @ x + np.random.multivariate_normal(self.mean, self.Q)
        return state

class MeasurementModel():
    def __init__(self, H, R):
        self.H = H
        self.R = R
        (n, _) = R.shape
        self.mean = np.zeros(n)

    def __call__(self, x):
        measurement = self.H @ x + np.random.multivariate_normal(self.mean, self.R)
        return measurement

def parameters(T = 1, s2_x = 0.1 ** 2, s2_y = 0.1 ** 2, lambda2 = 0.3 ** 2):
    F = np.array([[1, T],[0, 1]])
    zeros2 = np.zeros((2,2))
    A = np.block([[F, zeros2],[zeros2, F]])

    base = np.array([[T ** 3 / 3, T ** 2 / 2],[T ** 2 / 2, T]])
    sigma_x = s2_x * base
    sigma_y = s2_y * base
    Q = np.block([[sigma_x, zeros2],[zeros2, sigma_y]])

    H = np.array([[1, 0, 0, 0],[0, 0, 1, 0]])

    R = lambda2 * np.eye(2)

    return A, Q, H, R

def simulate(I, x_0):
    #I = iterations, x_0 = initial state
    (A, Q, H, R) = parameters()
    trueModel = TrueModel(A, Q)
    measurementModel = MeasurementModel(H, R)

    (m, _) = Q.shape
    (n, _) = R.shape
    state = np.zeros((I,m))
    measures = np.zeros((I,n))

    x = x_0
    for i in range(I):
        x = trueModel(x)
        y = measurementModel(x)

        state[i,:] = x
        measures[i,:] = y
    
    return state, measures