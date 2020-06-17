from manimlib.imports import *

class Kalman():
    def __init__(self, A, Q, H, R, x_0, P_0):
        self.A = A
        self.Q = Q
        self.H = H
        self.R = R

        self.x = x_0
        self.P = P_0
    
    def predict(self):
        self.x = self.A @ self.x
        self.P = self.A @ self.P @ self.A.transpose() + self.Q
    
    def update(self, y):
        self.V = y - self.H @ self.x
        self.S = self.H @ self.P @ self.H.transpose() + self.R
        self.K = self.P @ self.H.transpose() @ np.linalg.inv(self.S)

        self.x = self.x + self.K @ self.V
        self.P = self.P - self.K @ self.S @ self.K.transpose()

    def get_state(self):
        return self.x, self.P

    def __call__(self, measurements):

        (I, _) = measurements.shape
        m = len(self.x)
        ests = np.zeros((I,m))

        for i in range(I):
            self.predict()
            self.update(measurements[i,:])
            (x, _) = self.get_state()
            ests[i, :] = x
        
        return ests