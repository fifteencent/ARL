from manimlib.imports import *

class Echo():
    def __init__(self, f, SL = 0, TS = 0, DI = 0, shape = "rectangle", BW1 = 0.01, BW2 = 0.3, s = 6.096 / 2, D = 3300, S = 36, t = 10, pH = 7.8, fresh = False, a = 0):
        self.D = D #depth in meters
        self.S = S #salinity is 36g/kg
        self.t = t #temperature is 10˚C
        self.f = f #frequency in kHz
        self.SL = SL #sound level
        self.TS = TS #target strength
        self.pH = pH #pH of salt water is 7.8
        self.s = s #radius of target
        self.a = a
        self.fresh = fresh
        self.shape = shape
        self.BW1 = BW1
        self.BW2 = BW2
        self.DI = DI

    def getSL(self):
        if self.SL <= 0:
            # givens, power in Watts
            efficiency = 0.1
            power = 1000
            nDb = 10 * np.log10(efficiency)
            xmitDI = getDI(self.DI, self.shape, self.BW1, self.BW2)
            self.SL = 10 * np.log10(power) + nDb + xmitDI + 170.8
        return self.SL

    def getTL(self, r):
        if self.a <= 0:
            f_1 = 2.8 * (self.S / 35)**0.5 * 10**((4-1245)/(self.t + 273))
            f_2 = (8.17 * 10**((8-1990)/(self.t + 273)))/(1 + 0.0018 * (self.S - 35))

            P_1 = 1
            P_2 = 1 - 1.37 * 10**(-4) * self.D + 6.2 * 10**(-9) * self.D**2
            P_3 = 1 - 3.83 * 10**(-5) * self.D + 4.9 * 10**(-10) * self.D**2

            c = 1412 + 3.21 * self.t + 1.19 * self.S + 0.0167 * self.D

            A_1 = 8.86 / c * 10**(0.78 * self.pH - 5)
            A_2 = 21.44 * self.S / c * (1 + 0.025 * self.t)
            if self.t <= 20:
                A_3 = 4.937 * 10**(-4) - 2.59 * 10**(-5) * self.t  + 9.11 * 10**(-7) * self.t**2 - 1.50 * 10**(-8) * self.t**3
            else:
                A_3 = 3.964 * 10**(-4) - 1.146 * 10**(-5) * self.t  + 1.45 * 10**(-7) * self.t**2 - 6.5 * 10**(-10) * self.t**3

            if self.fresh:
                a_boric = 0
                a_magnesium = 0
            else:
                a_boric = (A_1 * P_1 * f_1 * self.f**2)/(self.f**2 + f_1**2)
                a_magnesium = (A_2 * P_2 * f_2 * self.f**2)/(self.f**2 + f_2**2)
            a_water = A_3 * P_3 * self.f**2
            self.a = a_boric + a_magnesium + a_water

        TL = 20 * np.log10(r) + self.a / 1000 * r

        return TL

    def getTS(self):
        if self.TS == 0:
            self.TS = 10 * np.log10(self.s**2 / 4)
        return self.TS

    def getVars(self):
        return self.SL, self.TS, self.a, self.f, self.s

    def __call__(self, r):
        return self.getSL() - 2 * self.getTL(r) + self.getTS()


class Noise():
    def __init__(self, f, DT = 0, DI = 0, SS = 4, shape = "rectangle", BW1 = 0.01, BW2 = 0.3, tau = 20):
        self.f = f
        self.DT = DT
        self.DI = DI
        self.SS = SS
        self.shape = shape
        self.BW1 = BW1
        self.BW2 = BW2
        self.tau = tau

    def getNL(self):
        seaState = {
            0: 89,
            1: 281.8,
            2: 707.9,
            3: 891.3,
            4: 1259,
            6: 1778.3
        }

        Q = seaState.get(self.SS, 1259) # defaults to sea-state 4
        NL = 20 * np.log10(2000 * Q / (self.f * 1000) + self.f * 1000 * 5.6234/30000)
        return NL
    
    def getDT(self):
        if self.DT <= 0:
            # uses d value determined by probability of detection of 80% with a probability of false alarm rate of 0.1%
            self.DT = 10 * np.log10(25 / (2 * self.tau))
        return self.DT


    def getVars(self):
        return self.DT, self.tau, self.DI, self.SS

    def __call__(self):
        self.DI = getDI(self.DI, self.shape, self.BW1, self.BW2)
        return self.getNL() - self.DI + self.getDT()

def getDI(DI, shape, BW1, BW2):
        if DI <= 0:
            array = {
                "line": 100 / BW1,
                "circle": 36000 / (BW1**2),
                "rectangle": 31600 / (BW1 * BW2)
            }

            x = array.get(shape, 31600 / (BW1 * BW2))

            DI = 10 * np.log10(x)
        return DI