# @Author: Felix Kramer <kramer>
# @Date:   24-02-2022
# @Email:  felixuwekramer@proton.me
# @Last modified by:   kramer
# @Last modified time: 08-07-2022


import networkx as nx
import numpy as np
from scipy.spatial import Voronoi
import random as rd
from dataclasses import dataclass, field


def init_graph_from_random(random_type, periods, sidelength):

    """
    Initialize a random spatial graph customized by type and size.

    Args:
        random_type (string):\n
            The type of random lattice to be constructed(voronoi_planar,
            voronoi_volume).
        periods (int):\n
            Number of random points.
        sidelength (float):\n
            The box size into which random points in space are generated.

    Returns:
        nx.Graph: A random spatial graph.

    """

    choose_constructor_option = {
        'default': NetworkxVoronoiPlanar,
        'voronoi_planar': NetworkxVoronoiPlanar,
        'voronoi_volume': NetworkxVoronoiVolume,
        }

    if random_type in choose_constructor_option:
        random = choose_constructor_option[random_type](
            periods,
            sidelength
            )

    else:
        print('Warning, crystal type unknown, set default: simple')
        random = choose_constructor_option['default'](periods, sidelength)

    return random.G


@dataclass
class NetworkxRandom():

    """
    A base class for spatial, random networks.

    Attributes
    ----------
        num_periods(int):\n
            Number of points for internal Voronoi construction.
        sidelength (float):\n
            Box length for spatial initialization.
        G (dictionary):\n
            An internal simple graph.

    """
    num_periods: int = 0
    sidelength: float = 0
    G: nx.Graph = field(default_factory=nx.Graph, repr=False, init=False)

    def mirror_boxpoints(self, points, sl):
        """
        Periodically mirror points in 2D for voronoi construction.

        Args:
            points (list):\n
                The original list of points (x,y)
            sl (float):\n
                The sidelength, acting as scale for the transition vector.

        Returns:
            ndarray: A matrix of all points and their mirrors

        """

        points_matrix = points
        intervall = [-1, 0, 1]
        for i in intervall:
            for j in intervall:
                if (i != 0 or j != 0):
                    points_matrix = np.concatenate(
                        (points_matrix, points+(i*sl, j*sl))
                        )

        return points_matrix

    def mirror_cubepoints(self, points, sl):
        """
        Periodically mirror points in 3D for voronoi construction.

        Args:
            points (list):\n
                The original list of points (x,y,z)
            sl (float):\n
                The sidelength, acting as scale for the transition vector.

        Returns:
            ndarray: A matrix of all points and their mirrors

        """
        points_matrix = points
        intervall = [-1, 0, 1]
        for i in intervall:
            for j in intervall:
                for k in intervall:
                    if (i != 0 or j != 0 or k != 0):
                        points_matrix = np.concatenate(
                            (points_matrix, points+(i*sl, j*sl, k*sl))
                            )

        return points_matrix
    # construct random 3d graph, confined in a box

    def is_in_box(self, v, sl):

        """
        Test whether new random point is inside the constraining boundaries.

        Args:
            v (list):\n
                The point vector to be tested.
            sl (float):\n
                The sidelength, acting as scale for the transition vector.

        Returns:
            bool: The boolean value, True if inside the original volume.

        """
        answer = True

        if (v[0] > sl) or (v[0] < -sl):
            answer = False
        if (v[1] > sl) or (v[1] < -sl):
            answer = False
        if (v[2] > sl) or (v[2] < -sl):
            answer = False

        return answer


@dataclass
class NetworkxVoronoiPlanar(NetworkxRandom):

    """
    A class algorithms to generate spatial, 2D random networks, generated via
    voronoi tesselation of a periodic plane.

    Attributes
    ----------
        num_periods(int):\n
            Number of points for internal Voronoi construction.
        sidelength (float):\n
            Box length for spatial initialization.
        G (dict):\n
            An internal simple graph.

    """

    def __post_init__(self):

        self.random_voronoi_periodic(self.num_periods, self.sidelength)
        # construct random 2d graph, confined in a certain spherical boundary,
        # connections set via voronoi tesselation

    def construct_voronoi_periodic(self, number, sidelength):
        """
        Generate random points in 2D, mirror them periodically and perform a
        Voronoi tesselation for a 2D random point set.

        Args:
            number (int):\n
                The number of points to be generated.
            sidelength (float):\n
                The sidelength of the box which hold points

        Returns:
            Voronoi: A scipy.spatial.Voronoi output object

        """

        V = 0
        # create points for voronoi tesselation
        XY = []

        for i in range(number):
            x = rd.uniform(0, sidelength)
            y = rd.uniform(0, sidelength)

            XY.append((x, y))
        self.XY = XY
        XY = self.mirror_boxpoints(np.array(XY), sidelength)
        self.XY_periodic = XY
        V = Voronoi(XY)

        return V

    def random_voronoi_periodic(self, number, sidelength):
        """
        Build a spatially embedded in 2D, random networkx internally for
        given size parameters.

        Args:
            number (int):\n
                The number of points to be generated.
            sidelength (float):\n
                The sidelength of the box which hold points

        """
        # construct a core of reandom points in 2D box for voronoi tesselation,
        # mirror the primary box so a total of 9 cells is created with the
        # initial as core
        V = self.construct_voronoi_periodic(number, sidelength)
        # pick up the face of the core which correspond to a periodic voronoi
        # lattice
        faces = []
        for j, i in enumerate(V.point_region):
            faces.append(np.asarray(V.regions[i]))

            if j == number-1:
                break
        # use periodic kernel to construct the correponding network
        faces = np.asarray(faces)
        f = faces[0]

        for i in range(len(faces[:])):
            if i+1 == len(faces[:]):
                break
            f = np.concatenate((f, faces[i+1]))
        for i in faces:
            for j in i:
                v = V.vertices[j]
                self.G.add_node(j, pos=v, lablel=j)

        k = 0
        for i in V.ridge_vertices:

            mask = np.in1d(i, f)
            if np.all(mask):

                for j in range(len(i)):
                    h = len(i)-1

                    options = {
                        # 'slope': (V.vertices[i[h-(l+1)]],
                        # V.vertices[i[h-l]]),
                        'label': k,
                    }
                    self.G.add_edge(i[h-(j+1)], i[h-j], **options)
                    k += 1
                    if len(i) == 2:
                        break


@dataclass
class NetworkxVoronoiVolume(NetworkxRandom):

    """
    A class algorithms to generate spatial, 3D random networks, generated via
     voronoi tesselation of a periodic volume.

    Attributes
    ----------
        num_periods(int):\n
            Number of points for internal Voronoi construction.
        sidelength (float):\n
            Box length for spatial initialization.
        G (dict):\n
            An internal simple graph.

    """

    def __post_init__(self):

        self.random_voronoi_periodic(self.num_periods, self.sidelength)
    # construct random 3d graph, confined in a certain spherical boundary,
    # connections set via voronoi tesselation

    def construct_voronoi_periodic(self, number, sidelength):

        """
        Generate random points in 3D, mirror them periodically and perform a
        Voronoi tesselation for a 3D random point set.

        Args:
            number (int): The number of points to be generated.
            sidelength (float): The sidelength of the box which hold points

        Returns:
            Voronoi: A scipy.spatial.Voronoi output object

        """
        V = 0
        # create points for voronoi tesselation

        XYZ = []

        for i in range(number):
            x = rd.uniform(0, sidelength)
            y = rd.uniform(0, sidelength)
            z = rd.uniform(0, sidelength)

            XYZ.append((x, y, z))
        self.XYZ = XYZ
        XYZ = self.mirror_cubepoints(np.array(XYZ), sidelength)
        self.XYZ_periodic = XYZ
        V = Voronoi(XYZ)

        return V

    def random_voronoi_periodic(self, number, sidelength):
        """
        Build a spatially embedded in 3D, random networkx internally for given
         size parameters.

        Args:
            number (int): The number of points to be generated.
            sidelength (float): The sidelength of the box which hold points

        """
        # construct a core of reandom points in 2D box for voronoi tesselation,
        # mirror the primary box so a total of 9 cells is created with the
        # initial as core
        V = self.construct_voronoi_periodic(number, sidelength)
        # pick up the face of the core which correspond to a periodic
        # voronoi lattice
        faces = []
        for j, i in enumerate(V.point_region):
            faces.append(np.asarray(V.regions[i]))

            if j == number-1:
                break
        # use periodic kernel to construct the correponding network
        faces = np.asarray(faces)
        f = faces[0]

        for i in range(len(faces[:])):
            if i+1 == len(faces[:]):
                break
            f = np.concatenate((f, faces[i+1]))
        for i in faces:
            for j in i:
                v = V.vertices[j]
                self.G.add_node(j, pos=v, lablel=j)

        k = 0
        for i in V.ridge_vertices:

            mask = np.in1d(i, f)
            if np.all(mask):

                for j in range(len(i)):
                    h = len(i)-1
                    options = {
                        # 'slope': (V.vertices[i[h-(l+1)]],
                        # V.vertices[i[h-l]]),
                        'label': k
                    }
                    self.G.add_edge(i[h-(j+1)], i[h-j], **options)
                    k += 1
                    if len(i) == 2:
                        break
