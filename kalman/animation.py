from manimlib.imports import *
from ARL.kalman.custom_graph import *
from ARL.kalman.kalman import Kalman
from ARL.kalman.model import *

class Animation(CustomGraph):
    CONFIG = {
        'x_min': 0,
        'x_max': 4,
        'y_min': 0,
        'y_max': 5,
        "graph_origin": 3 * DOWN + 6 * LEFT
    }

    def construct(self):
        # Create Graph
        np.random.seed(23460)
        I=1000
        x_0 = np.array([0, 0.5, 0, 0.5])
        P_0 = np.zeros((4,4))
        (A, H, Q, R) = parameters()
        (state, measures) = simulate(I, x_0)
        kalman = Kalman(A, H, Q, R, x_0, P_0)
        ests = kalman(measures)

        xmin = 0
        xmax = 1
        ymin = 0
        ymax = 1
        for i in range(I):
            xoptions = [ests[i][0], state[i][0], measures[i][0]]
            yoptions = [ests[i][int(len(ests[i,:])/2)], state[i][int(len(state[i,:])/2)], measures[i][int(len(measures[i,:])/2)]]
            xmin = min(min(xoptions),xmin)
            xmax = max(max(xoptions),xmax)
            ymin = min(min(yoptions),ymin)
            ymax = max(max(yoptions),ymax)

        self.x_min = round(xmin * 2) / 2
        self.x_max = round(xmax * 2) / 2
        self.y_min = round(ymin * 2) / 2
        self.y_max = round((ymax + math.copysign(ymax * 0.2, 1)) * 2) / 2
        xinterval = int(np.ceil((self.x_max - self.x_min) / 10))
        yinterval = int(np.ceil((self.y_max - self.y_min) / 10))
        self.x_labeled_nums = range(int(self.x_min), int(np.ceil(self.x_max / xinterval) * xinterval), xinterval)
        self.y_labeled_nums = range(int(self.y_min), int(np.ceil(self.y_max / yinterval) * yinterval), yinterval)

        self.setup_axes(animate=True)

        radius = 0 if max(xinterval, yinterval) >= 2 else 0.07

        stateColor = WHITE
        stateCoords = self.get_coords(state)
        stateDots = self.get_dots_from_coords(stateCoords, stateColor, radius=radius)

        statePathJagged = VMobject()
        statePathSmooth = VMobject()
        statePathJagged.set_points_as_corners(self.get_points_from_coords(stateCoords))
        statePathSmooth.set_points_smoothly(self.get_points_from_coords(stateCoords))
        stateLabel = self.create_label(stateColor, "true state").scale(0.75)
        stateDot = Dot(radius = 0.15, color = stateColor)
        stateDot.move_arc_center_to(0.5 * DOWN + 3.5 * RIGHT)
        stateLabel.next_to(stateDot,RIGHT)

        measureColor = RED
        measureCoords = self.get_coords(measures)
        measureDots = self.get_dots_from_coords(measureCoords, measureColor, radius=radius)

        measurePath = VMobject()
        measurePath.set_points_as_corners(self.get_points_from_coords(measureCoords)).set_color(measureColor)
        measureLabel = self.create_label(measureColor, "measured values").scale(0.75)
        measureDot = Dot(radius = 0.15, color = measureColor)
        measureDot.move_arc_center_to(1 * DOWN + 3.5 * RIGHT)
        measureLabel.next_to(measureDot,RIGHT)
        measureLabel.align_to(stateLabel,LEFT)

        estColor = YELLOW
        estCoords = self.get_coords(ests)
        estDots = self.get_dots_from_coords(estCoords, estColor, radius=radius)

        estPath = VMobject()
        estPath.set_points_smoothly(self.get_points_from_coords(estCoords)).set_color(estColor)
        estLabel = self.create_label(estColor, "predicted values").scale(0.75)
        estDot = Dot(radius = 0.15, color = estColor)
        estDot.move_arc_center_to(1.5 * DOWN + 3.5 * RIGHT)
        estLabel.next_to(estDot,RIGHT)
        estLabel.align_to(stateLabel,LEFT)

        rmseTitle = self.create_label(WHITE, "RMSError").scale(0.75)
        rmseTitle.move_to(1.5 * UP + 3 * RIGHT)
        rmseTitle.align_to(stateDot,LEFT)

        def rmse(predictions, targets):
            m = len(predictions[1,:])
            xpreds = predictions[:,0]
            ypreds = predictions[:,int(m/2)]
            respreds = np.sqrt(np.square(xpreds) + np.square(ypreds))

            n = len(targets[1,:])
            xtargs = targets[:,0]
            ytargs = targets[:,int(n/2)]
            restargs = np.sqrt(np.square(xtargs) + np.square(ytargs))

            return np.sqrt(((respreds - restargs) ** 2).mean())
        
        measuresrmse = TextMobject("Sensor: " + str(round(rmse(measures,state),3)), 
                    tex_to_color_map={str(round(rmse(measures,state),3)): measureColor}).scale(0.75)
        kalmanrmse = TextMobject("Kalman: " + str(round(rmse(ests,state),3)),    
                    tex_to_color_map={str(round(rmse(ests,state),3)): estColor}).scale(0.75)
        measuresrmse.move_to(1 * UP + 3 * RIGHT).align_to(stateDot,LEFT)
        kalmanrmse.move_to(0.5 * UP + 3 * RIGHT).align_to(stateDot,LEFT)

        title = self.create_label(WHITE, "KALMAN FILTER")
        title.move_to(3 * UP)

        # Display graph
        self.play(Write(title))
        self.play(ShowCreation(statePathJagged,run_time=3), ShowCreation(stateDots,run_time=3), ShowCreation(measurePath,run_time=3), ShowCreation(measureDots,run_time=3))
        self.play(ShowCreation(stateDot), ShowCreation(measureDot), Write(stateLabel), Write(measureLabel), Transform(statePathJagged, statePathSmooth))
        self.wait(0.5)
        self.play(ShowCreation(estPath,run_time=3), ShowCreation(estDots,run_time=3))
        self.play(ShowCreation(estDot), Write(estLabel))
        self.wait(0.5)
        self.play(Write(rmseTitle))
        self.play(Write(measuresrmse))
        self.play(Write(kalmanrmse))
        self.wait(1)