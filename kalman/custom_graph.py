from manimlib.imports import *

class CustomGraph(GraphScene):
    CONFIG = {
        'x_min': -5,
        'x_max': 5,
        'y_min': -5,
        'y_max': 5,
        'axes_color': BLUE,
        "x_axis_label": "$x(m)$",
        "y_axis_label": "$y(m)$"
    }

    def get_points_from_coords(self,coords):
        return [
            # Convert COORDS -> POINTS
            self.coords_to_point(px,py)
            # See manimlib/scene/graph_scene.py
            for px,py in coords
        ]

    # Return the dots of a set of points
    def get_dots_from_coords(self,coords,color,radius=0.07):
        points = self.get_points_from_coords(coords)
        dots = VGroup(*[
            Dot(radius=radius, color=color).move_to([px,py,pz])
            for px,py,pz in points
            ]
        )
        return dots

    def get_coords(self,matrix): 
        coords = []
        for row in matrix:
            m = len(row)
            coord = [float(row[0]),float(row[int(m/2)])]
            coords.append(coord)
        return coords

    def create_label(self,color,label):
        label1 = TextMobject(label)
        label1.set_color(color)
        return label1