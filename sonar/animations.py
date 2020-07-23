from manimlib.imports import *
from ARL.sonar.sonar_eq import *
from ARL.sonar.fancy_sonar_eq import *
from scipy.optimize import fsolve

class BasicAnimation(GraphScene):
    CONFIG = {
        'x_min': 0,
        'x_max': 1000,
        'x_tick_frequency': 100,
        'x_axis_label': "Range (m)",
        'y_min': 0,
        'y_max': 160,
        'y_tick_frequency': 20,
        'y_log': False,
        'y_axis_label': "Sound Pressure Level (dB re 1 $\mu$Pa)",
        'graph_origin': 3 * DOWN + 5.5 * LEFT,
        'exclude_zero_label': False
    }

    def create_label(self,color,label):
        label1 = TextMobject(label)
        label1.set_color(color)
        return label1

    def noiseFunc(self, x):
        f = 36.162
        noise = Noise(f, SS = 4, tau = 80)
        noiseLevel = noise()
        return noiseLevel

    def construct(self):
        # Create Graph
        f = 36.162

        echo = Echo(f)
        noise = Noise(f, SS = 4, tau = 80)
        noiseLevel = noise()

        func = lambda r : echo(r) - noiseLevel
        intersect = fsolve(func, 30000)

        self.x_max = np.ceil(intersect * 4.0 / 2 / self.x_tick_frequency) * self.x_tick_frequency
        self.x_tick_frequency = int(np.round((self.x_max - self.x_min) / 8, -3))
        self.x_max = np.ceil(intersect * 4.0 / 2 / self.x_tick_frequency) * self.x_tick_frequency
        self.x_labeled_nums = range(int(self.x_min), int(self.x_max) + self.x_tick_frequency, self.x_tick_frequency)
        
        y = np.ceil(noiseLevel * 2 / self.y_tick_frequency) * self.y_tick_frequency
        if y > 0:
            self.y_max = y * 2
            self.y_tick_frequency = int(np.round((self.y_max - self.y_min) / 8, -1))
            self.y_max = np.ceil(noiseLevel * 3 / self.y_tick_frequency) * self.y_tick_frequency * 2
        else:
            self.y_min = y
            self.y_max = 300
            self.y_tick_frequency = int(np.round((self.y_max - self.y_min) / 8, -1))
            self.y_min = np.ceil(noiseLevel * 2.0 / self.y_tick_frequency) * self.y_tick_frequency * 2
            self.y_max = 300
        self.y_labeled_nums = range(int(self.y_min), int(self.y_max) + self.y_tick_frequency, self.y_tick_frequency)

        self.setup_axes(animate=True)

        title = self.create_label(WHITE, "ACTIVE SONAR EQUATION")
        title.move_to(2.25 * UP)

        subtitle = self.create_label(WHITE, "Echo Level vs Noise Masking Level")
        subtitle.move_to(1.75 * UP).scale(0.75)
        echoColor = WHITE
        echoGraph = self.get_graph(echo, echoColor)
        echoLabel = self.create_label(echoColor, "Echo Level").scale(0.75)
        echoDot = Dot(radius = 0.15, color = echoColor)
        echoDot.move_arc_center_to(0.75 * UP + 2 * LEFT)
        echoLabel.next_to(echoDot,RIGHT)

        noiseColor = YELLOW
        noiseGraph = self.get_graph(self.noiseFunc, noiseColor)
        noiseLabel = self.create_label(noiseColor, "Noise Masking Level").scale(0.75)
        noiseDot = Dot(radius = 0.15, color = noiseColor)
        noiseDot.move_arc_center_to(0.25 * UP + 2 * LEFT)
        noiseLabel.next_to(noiseDot,RIGHT)

        intersection = Dot(radius = 0.12, color = BLUE).move_to(self.coords_to_point(intersect, noiseLevel))
        intersectionLabel = self.create_label(BLUE, "Range Limit: " + str(float(np.round(intersect, 2))) + "m").scale(0.75).next_to(intersection,UP).align_to(intersection,LEFT)

        (SL, TS, al, Fc, Sh) = echo.getVars()
        (DT, PL, DI, SS) = noise.getVars()

        labelSL = self.create_label(WHITE, "SL: " + str(np.round(SL,2)) + "dB re 1$\mu$Pa @ 1m").scale(0.5).move_to(2 * UP + 5.25 * RIGHT)
        labelTS = self.create_label(WHITE, "TS: " + str(np.round(TS,2)) + "dB").scale(0.5).next_to(labelSL,DOWN).align_to(labelSL,LEFT)        
        labelDT = self.create_label(WHITE, "DT: " + str(np.round(DT,2)) + "dB").scale(0.5).next_to(labelTS,DOWN).align_to(labelSL,LEFT)
        labelFc = self.create_label(WHITE, "Fc: " + str(np.round(Fc,2)) + "kHz").scale(0.5).next_to(labelDT,DOWN).align_to(labelSL,LEFT)
        labelPL = self.create_label(WHITE, "Pulse Length: " + str(np.round(PL,2)) + "ms").scale(0.5).next_to(labelFc,DOWN).align_to(labelSL,LEFT)
        labelDI = self.create_label(WHITE, "DI: " + str(np.round(DI,2)) + "dB").scale(0.5).next_to(labelPL,DOWN).align_to(labelSL,LEFT)
        labelSS = self.create_label(WHITE, "Sea State: " + str(np.round(SS,2))).scale(0.5).next_to(labelDI,DOWN).align_to(labelSL,LEFT)
        labelAl = self.create_label(WHITE, "alpha: " + str(np.round(al,2)) + "dB/km").scale(0.5).next_to(labelSS,DOWN).align_to(labelSL,LEFT)

        # Display graph
        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(ShowCreation(echoGraph), ShowCreation(noiseGraph))
        self.play(ShowCreation(echoDot), ShowCreation(noiseDot), Write(echoLabel), Write(noiseLabel))
        self.play(ShowCreation(intersection), Write(intersectionLabel))
        self.wait(0.5)
        self.play(Write(labelSL), Write(labelTS), Write(labelDT), Write(labelFc), Write(labelPL), Write(labelDI), Write(labelSS), Write(labelAl))
        self.wait(0.5)
        #self.play(Write(rmseTitle))
        #self.play(Write(noisesrmse))
        #self.play(Write(kalmanrmse))
        #self.wait(1)

class FancyAnimation(ThreeDScene):
    
    def create_label(self,color,label):
        label1 = TextMobject(label)
        label1.set_color(color)
        return label1
    
    def construct(self):
        # Create Graph

        axes = ThreeDAxes(
            x_min = -3,
            x_max = 7,
            y_min = -3,
            y_max = 7,
            z_min = -2,
            z_max = 10
        )

        echo = fancyEcho()
        noise = fancyNoise()
        func = lambda f, tau : echo(f) - noise(f, tau)

        graph = ParametricSurface(
            lambda u, v : np.array([
                u, 
                v, 
                (echo(10**u) - noise(10**u, 2**v)) / 100]),
                checkerboard_colors=[BLUE_D, BLUE_E], 
                u_min = -2, u_max = 6, 
                v_min = -2, v_max = 6)

        title = self.create_label(WHITE, "ACTIVE SONAR EQUATION")
        title.to_corner(UL)
        title.bg=BackgroundRectangle(title,fill_opacity=0.6)
        title_group = VGroup(title.bg,title)

        subtitle = self.create_label(WHITE, "Difference in Echo and Noise Levels vs Pulse Length and Frequency")
        subtitle.next_to(title,DOWN).scale(0.65)
        subtitle.bg=BackgroundRectangle(subtitle,fill_opacity=0.6)
        subtitle_group = VGroup(subtitle.bg,subtitle)
        subtitle.to_edge(LEFT)

        (SL, TS, _, Ra, Sh) = echo.getVars()
        (DT, DI, SS) = noise.getVars()

        labelSL = self.create_label(WHITE, "SL: " + str(np.round(SL,2)) + "dB re 1$\mu$Pa @ 1m").scale(0.5).to_corner(UR)
        labelTS = self.create_label(WHITE, "TS: " + str(np.round(TS,2)) + "dB").scale(0.5).next_to(labelSL,DOWN).align_to(labelSL,LEFT)        
        labelDT = self.create_label(WHITE, "DT: " + str(np.round(DT,2)) + "dB").scale(0.5).next_to(labelTS,DOWN).align_to(labelSL,LEFT)
        labelRa = self.create_label(WHITE, "Range: " + str(np.round(Ra,2)) + "m").scale(0.5).next_to(labelDT,DOWN).align_to(labelSL,LEFT)
        labelDI = self.create_label(WHITE, "DI: " + str(np.round(DI,2)) + "dB").scale(0.5).next_to(labelRa,DOWN).align_to(labelSL,LEFT)
        labelSS = self.create_label(WHITE, "Sea State: " + str(np.round(SS,2))).scale(0.5).next_to(labelDI,DOWN).align_to(labelSL,LEFT)
        label_group = VGroup(labelSL, labelTS, labelDT, labelRa, labelDI, labelSS)
        label_group.bg=BackgroundRectangle(label_group,fill_opacity=0.6)
        label_group = VGroup(label_group.bg, labelSL, labelTS, labelDT, labelRa, labelDI, labelSS)

        # Display graph
        self.add(axes)
        self.add_fixed_in_frame_mobjects(title_group, subtitle_group, label_group)
        self.set_camera_orientation(phi = 80 * DEGREES, theta = 45 * DEGREES, distance = 50)
        self.begin_ambient_camera_rotation(rate=0.5)
        self.play(Write(graph))
        self.wait(5)
        #self.play(Write(rmseTitle))
        #self.play(Write(noisesrmse))
        #self.play(Write(kalmanrmse))
        #self.wait(1)
    
class Absorption(GraphScene):
    CONFIG = {
        'x_min': -6,
        'x_max': 4,
        'x_tick_frequency': 2,
        'x_axis_label': "Frequency ($10^x$ Hz)",
        'y_min': -10,
        'y_max': -2,
        'y_tick_frequency': 2,
        'y_axis_label': "Absorption ($10^y$ dB/km)",
        'graph_origin': 3 * DOWN + 5.5 * LEFT,
        'exclude_zero_label': False
    }

    def create_label(self,color,label):
        label1 = TextMobject(label)
        label1.set_color(color)
        return label1

    def construct(self):
        self.x_labeled_nums = range(self.x_min, self.x_max + self.x_tick_frequency, self.x_tick_frequency)
        self.y_labeled_nums = range(self.y_min, self.y_max + self.y_tick_frequency, self.y_tick_frequency)
        self.setup_axes(animate=True)

        fresh = fancyEcho(fresh = True, D = 0)
        freshFunc = lambda f : np.log10(fresh.getA(10**(f)/1000))

        title = self.create_label(WHITE, "ACTIVE SONAR EQUATION")
        title.move_to(2.5 * UP)
        title.bg=BackgroundRectangle(title,fill_opacity=0.6)
        title_group = VGroup(title.bg,title)

        subtitle = self.create_label(WHITE, "Absorption vs Frequency")
        subtitle.move_to(2 * UP).scale(0.75)
        subtitle.bg=BackgroundRectangle(subtitle,fill_opacity=0.6)
        subtitle_group = VGroup(subtitle.bg,subtitle)

        freshColor = BLUE
        freshGraph = self.get_graph(freshFunc, freshColor)
        freshLabel = self.create_label(freshColor, "Fresh Water").scale(0.75)
        freshDot = Dot(radius = 0.15, color = freshColor)
        freshDot.move_arc_center_to(0.25 * UP + 4 * RIGHT)
        freshLabel.next_to(freshDot,RIGHT)

        salt = fancyEcho(fresh = False, D = 0)
        saltyFunc = lambda f : np.log10(salt.getA(10**f/1000))

        saltColor = WHITE
        saltGraph = self.get_graph(saltyFunc, saltColor)
        saltLabel = self.create_label(saltColor, "Salt Water").scale(0.75)
        saltDot = Dot(radius = 0.15, color = saltColor)
        saltDot.move_arc_center_to(0.25 * DOWN + 4 * RIGHT)
        saltLabel.next_to(saltDot,RIGHT)

        self.play(ShowCreation(freshGraph), ShowCreation(saltGraph), Write(title_group), Write(subtitle_group))
        self.play(ShowCreation(freshDot), ShowCreation(saltDot), Write(freshLabel), Write(saltLabel))
        self.wait(0.5)

class SeaNoise(GraphScene):
    CONFIG = {
        'x_min': 3,
        'x_max': 6,
        'x_tick_frequency': 0.5,
        'x_axis_label': "Frequency ($10^x$ Hz)",
        'y_min': 10,
        'y_max': 80,
        'y_tick_frequency': 10,
        'y_axis_label': "SPL (dB re 1$\mu$Pa)",
        'graph_origin': 3 * DOWN + 5.5 * LEFT,
        'exclude_zero_label': False
    }

    def create_label(self,color,label):
        label1 = TextMobject(label)
        label1.set_color(color)
        return label1

    def construct(self):
        self.x_labeled_nums = np.linspace(self.x_min, self.x_max, int((self.x_max - self.x_min) / self.x_tick_frequency) + 1)
        self.y_labeled_nums = np.linspace(self.y_min, self.y_max, int((self.y_max - self.y_min) / self.y_tick_frequency) + 1)
        self.setup_axes(animate=True)

        noise0 = fancyNoise(SS = 0)
        func0 = lambda f : noise0.getNL(10**f/1000)
        noise1 = fancyNoise(SS = 1)
        func1 = lambda f : noise1.getNL(10**f/1000)
        noise2 = fancyNoise(SS = 2)
        func2 = lambda f : noise2.getNL(10**f/1000)
        noise3 = fancyNoise(SS = 3)
        func3 = lambda f : noise3.getNL(10**f/1000)
        noise4 = fancyNoise(SS = 4)
        func4 = lambda f : noise4.getNL(10**f/1000)
        noise6 = fancyNoise(SS = 6)
        func6 = lambda f : noise6.getNL(10**f/1000)
        thermalFunc = lambda f : -15 + 20 * np.log10(10**f/1000)
        

        title = self.create_label(WHITE, "ACTIVE SONAR EQUATION")
        title.move_to(2.5 * UP)
        title.bg=BackgroundRectangle(title,fill_opacity=0.6)
        title_group = VGroup(title.bg,title)

        subtitle = self.create_label(WHITE, "Sea State Noise vs Frequency")
        subtitle.move_to(2 * UP).scale(0.75)
        subtitle.bg=BackgroundRectangle(subtitle,fill_opacity=0.6)
        subtitle_group = VGroup(subtitle.bg,subtitle)

        color0 = PURPLE
        graph0 = self.get_graph(func0, color0)
        color1 = BLUE
        graph1 = self.get_graph(func1, color1)
        color2 = GREEN
        graph2 = self.get_graph(func2, color2)
        color3 = YELLOW
        graph3 = self.get_graph(func3, color3)
        color4 = ORANGE
        graph4 = self.get_graph(func4, color4)
        color6 = RED
        graph6 = self.get_graph(func6, color6)
        thermalColor = WHITE
        thermalGraph = self.get_graph(thermalFunc, thermalColor)

        graphs = VGroup(graph0, graph1, graph2, graph3, graph4, graph6, thermalGraph)

        dot0 = Dot(radius = 0.15, color = color0)
        dot0.move_arc_center_to(1.5 * DOWN + 4 * RIGHT)
        dot1 = Dot(radius = 0.15, color = color1)
        dot1.move_arc_center_to(1.0 * DOWN + 4 * RIGHT)
        dot2 = Dot(radius = 0.15, color = color2)
        dot2.move_arc_center_to(0.5 * DOWN + 4 * RIGHT)
        dot3 = Dot(radius = 0.15, color = color3)
        dot3.move_arc_center_to(0 * DOWN + 4 * RIGHT)
        dot4 = Dot(radius = 0.15, color = color4)
        dot4.move_arc_center_to(0.5 * UP + 4 * RIGHT)
        dot6 = Dot(radius = 0.15, color = color6)
        dot6.move_arc_center_to(1 * UP + 4 * RIGHT)
        thermalDot = Dot(radius = 0.15, color = thermalColor)
        thermalDot.move_arc_center_to(1.5 * UP + 4 * RIGHT)

        dots = VGroup(thermalDot, dot6, dot4, dot3, dot2, dot1, dot0)

        label0 = self.create_label(color0, "Sea State 0").scale(0.75)
        label0.next_to(dot0,RIGHT)
        label1 = self.create_label(color1, "Sea State 1").scale(0.75)
        label1.next_to(dot1,RIGHT)
        label2 = self.create_label(color2, "Sea State 2").scale(0.75)
        label2.next_to(dot2,RIGHT)
        label3 = self.create_label(color3, "Sea State 3").scale(0.75)
        label3.next_to(dot3,RIGHT)
        label4 = self.create_label(color4, "Sea State 4").scale(0.75)
        label4.next_to(dot4,RIGHT)
        label6 = self.create_label(color6, "Sea State 6").scale(0.75)
        label6.next_to(dot6,RIGHT)
        thermalLabel = self.create_label(thermalColor, "Thermal Noise").scale(0.75)
        thermalLabel.next_to(thermalDot,RIGHT)

        labels = VGroup(thermalLabel, label6, label4, label3, label2, label1, label0)

        self.play(ShowCreation(graphs), Write(title_group), Write(subtitle_group))
        self.play(ShowCreation(dots), Write(labels))
        self.wait(0.5)