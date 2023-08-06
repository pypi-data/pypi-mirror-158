# @Author: Felix Kramer <kramer>
# @Date:   24-02-2022
# @Email:  felixuwekramer@proton.me
# @Last modified by:   kramer
# @Last modified time: 08-07-2022


import networkx as nx
import numpy as np


# construct a non-trivial,  periodic 3d embedding
def init_graph_from_crystal(crystal_type, periods):

    """
    Initialize a spatially embedded graph, with based on crystal lattice.

    Args:
        crystal_type (string):\n
            The type of crystal skeleton (default, simple, chain, bcc, fcc,
            diamond, laves, square, hexagonal, trigonal_planar).
        periods (int):\n
            Repetition number of the lattice's unit cell.

    Returns:
        nx.Graph: A networkx graph.

    """

    choose_constructor_option = {
        'default': NetworkxSimple,
        'simple': NetworkxSimple,
        'chain': NetworkxChain,
        'bcc': NetworkxBcc,
        'fcc': NetworkxFcc,
        'diamond': NetworkxDiamond,
        'laves': NetworkxLaves,
        'square': NetworkxSquare,
        'hexagonal': NetworkxHexagonal,
        'triagonal_planar': NetworkxTriagonalPlanar,
        }

    if crystal_type in choose_constructor_option:
        crystal = choose_constructor_option[crystal_type](periods)

    else:
        print('Warning, crystal type unknown, set default: simple')
        crystal = choose_constructor_option['default'](1)

    return crystal.G


def init_graph_from_asymCrystal(crystal_type, periodsZ, periodsXY):

    """
    Initialize a spatially embedded graph, with based on an asymmetric
    crystal lattice.

    Args:
        crystal_type (string):\n
            The type of crystal skeleton (trigonal_stack).
        periodsZ (int):\n
            Vertical repetition number of the lattice's unit cell.
        periodsXY (int):\n
            Lateral repetition number of the lattice's unit cell.

    Returns:
        nx.Graph: A networkx graph.

    """

    choose_constructor_option = {
        'trigonal_stack': NetworkxTriagonalStack,
        }

    if crystal_type in choose_constructor_option:
        crystal = choose_constructor_option[crystal_type](periodsZ, periodsXY)

    else:
        print('Warning, crystal type unknown, set default: trigonal_stack')
        crystal = choose_constructor_option['default'](2, 2)

    return crystal.G


class NetworkxCrystal():

    """
    A base class for spatial, crystal-like graphs.

    Attributes
    ----------

        G (nx.Graph):\n
            An internal networkx graph variable.
        dict_cells (dictionary):\n
            A dictionary of the current cells.
        lattice_constant (float):\n
            Scale for the lattice. spacing
        translation_length (float):\n
            Scale for the translational offset.

    """

    def __init__(self):

        """
        A constructor for crystal objects, setting default values
        for the interal graph objects and geometry
        """

        self.G = nx.Graph()
        self.dict_cells = {}
        self.lattice_constant = 1
        self.translation_length = 1

    # construct one of the following crystal topologies
    def lattice_translation(self, t, T):

        """
        Return a networkx graph, initialzed from given unit cell and offset.

        Args:
            t (ndarray):\n
                A translational offset for the lattice.
            T (nx.Graph):\n
                A networkx graph, unit cell.

        Returns:
            nx.Graph: A simple, periodic Graph.

        """

        D = nx.Graph()
        for n in T.nodes():
            D.add_node(tuple(n+t), pos=T.nodes[n]['pos']+t)

        return D

    def periodic_cell_structure(self, cell, num_periods):

        """
        Set the internal graph variable by periodically repeating the chosen
        unitcell type.

        Args:
            cell (nx.Graph):\n
                A networkx graph, unit cell.
            num_periods (int):\n
                Repetition number for the unit cells.

        """

        DL = nx.Graph()

        if type(num_periods) is not int:
            periods = [range(num_periods[i]) for i in range(3)]
        else:
            periods = [range(num_periods) for i in range(3)]
        for i in periods[0]:
            for j in periods[1]:
                for k in periods[2]:
                    v = self.translation_length*np.array([i, j, k])
                    TD = self.lattice_translation(v, cell)
                    DL.add_nodes_from(TD.nodes(data=True))
                    self.dict_cells[(i, j, k)] = list(TD.nodes())

        list_n = np.array(list(DL.nodes()))
        for i, n in enumerate(list_n[:-1]):
            for m in list_n[(i+1):]:
                p = DL.nodes[tuple(n)]['pos']
                q = DL.nodes[tuple(m)]['pos']
                dist = np.linalg.norm(p-q)
                if dist == self.lattice_constant:
                    DL.add_edge(tuple(n), tuple(m))

        dict_nodes = {}
        for idx_n, n in enumerate(DL.nodes()):
            self.G.add_node(idx_n, pos=DL.nodes[n]['pos'])
            dict_nodes.update({n: idx_n})
        for idx_e, e in enumerate(DL.edges()):
            u, v = dict_nodes[e[0]], dict_nodes[e[1]]
            self.G.add_edge(u, v)

        self.dict_cubes = {}
        dict_aux = {}
        for i, k in enumerate(self.dict_cells.keys()):
            dict_aux[i] = [dict_nodes[n] for n in self.dict_cells[k]]
        for i, k in enumerate(dict_aux.keys()):
            self.dict_cubes[k] = nx.Graph()
            n_list = list(dict_aux[k])
            for u in n_list[:-1]:
                for v in n_list[1:]:
                    if self.G.has_edge(u, v):
                        self.dict_cubes[k].add_edge(u, v)


# 3D
class NetworkxSimple(NetworkxCrystal):

    """
    A derived class for spatial, simple cubic graphs.

    """

    def __init__(self,  num_periods):

        """
        A constructor for simple cubic crystal objects, setting default values
        for the interal graph objects and geometry
        """

        super(NetworkxSimple, self).__init__()
        self.lattice_constant = 1.
        self.translation_length = 1.
        self.simple_cubic_lattice(num_periods)

    # construct full cubic grid as skeleton
    def simple_unit_cell(self):

        """
        Return a networkx graph of the simbple cubic unit cell.

        Returns:
            nx.Graph:\n
                A  networkx graph.

        """

        D = nx.Graph()
        for i in [0, 1]:
            for j in [0, 1]:
                for k in [0, 1]:
                    D.add_node(tuple((i, j, k)), pos=np.array([i, j, k]))

        return D

    def simple_cubic_lattice(self, num_periods):

        """
        Set the internal graph as simple cubic lattice.

        Args:
            num_periods (int):\n
                Repetition number for the unit cell.

        """

        D = self.simple_unit_cell()
        self.periodic_cell_structure(D, num_periods)


class NetworkxChain(NetworkxCrystal):

    """
    A derived class for spatial, 1D chain graphs.

    """

    def __init__(self, num_periods):

        """
        A constructor for chain objects, setting default values
        for the interal graph objects and geometry
        """

        super(NetworkxChain, self).__init__()
        self.simple_chain(num_periods)

    def simple_chain(self, num_periods):

        """
        Set the internal graph as a simple 1D chain.

        Args:
            num_periods (int):\n
                Length of the chain.

        """

        # construct single box
        for i in range(num_periods):
            self.G.add_node(i, pos=np.array([i, 0, 0]))
        for i in range(num_periods-1):
            self.G.add_edge(i+1, i)


class NetworkxBcc(NetworkxCrystal):

    """
    A derived class for spatial, simple bcc graphs.

    """

    def __init__(self,  num_periods):

        """
        A constructor for simple bcc crystal objects, setting default values
        for the interal graph objects and geometry
        """
        super(NetworkxBcc, self).__init__()
        self.lattice_constant = np.sqrt(3.)/2.
        self.translation_length = 1.
        self.simple_bcc_lattice(num_periods)

    def bcc_unit_cell(self):

        """
        Return a networkx graph of the simple bcc unit cell.

        Returns:
            nx.Graph:\n
                A  networkx graph.

        """

        D = nx.Graph()
        for i in [0, 1]:
            for j in [0, 1]:
                for k in [0, 1]:
                    D.add_node(tuple((i, j, k)), pos=np.array([i, j, k]))
        D.add_node(tuple((0.5, 0.5, 0.5)), pos=np.array([0.5, 0.5, 0.5]))

        return D

    def simple_bcc_lattice(self, num_periods):

        """
        Set the internal graph as simple bcc lattice.

        Args:
            num_periods (int):\n
                Repetition number for the unit cell.

        """

        # construct single box
        D = self.bcc_unit_cell()
        self.periodic_cell_structure(D, num_periods)


class NetworkxFcc(NetworkxCrystal):

    """
    A derived class for spatial, simple fcc graphs.

    """

    def __init__(self, num_periods):

        """
        A constructor for simple fcc crystal objects, setting default values
        for the interal graph objects and geometry
        """
        super(NetworkxFcc, self).__init__()
        self.lattice_constant = np.sqrt(2.)/2.
        self.translation_length = 1.
        self.simple_fcc_lattice(num_periods)

    def fcc_unit_cell(self):

        """
        Return a networkx graph of the simple fcc unit cell.

        Returns:
            nx.Graph:\n
                A  networkx graph.

        """

        D = nx.Graph()
        for i in [0, 1]:
            for j in [0, 1]:
                for k in [0, 1]:
                    D.add_node(tuple((i, j, k)), pos=np.array([i, j, k]))
        for i in [0., 1.]:
            D.add_node(tuple((0.5, i, 0.5)), pos=np.array([0.5, i, 0.5]))
        for i in [0., 1.]:
            D.add_node(tuple((0.5, 0.5, i)), pos=np.array([0.5, 0.5, i]))
        for i in [0., 1.]:
            D.add_node(tuple((i, 0.5, 0.5)), pos=np.array([i, 0.5, 0.5]))

        return D

    def simple_fcc_lattice(self, num_periods):

        """
        Set the internal graph as simple fcc lattice.

        Args:
            num_periods (int):\n
                Repetition number for the unit cell.

        """

        D = self.fcc_unit_cell()
        self.periodic_cell_structure(D, num_periods)


class NetworkxDiamond(NetworkxCrystal):

    """
    A derived class for spatial, diamond graphs.

    """

    def __init__(self, num_periods):
        """
        A constructor for diamond crystal objects, setting default values
        for the interal graph objects and geometry
        """
        super(NetworkxDiamond, self).__init__()
        self.lattice_constant = np.sqrt(3.)/2.
        self.translation_length = 2.
        self.diamond_lattice(num_periods)

    def diamond_unit_cell(self):

        """
        Return a networkx graph of the dioamond unit cell.

        Returns:
            nx.Graph:\n
                A  networkx graph.

        """

        D = nx.Graph()
        T = [nx.Graph() for i in range(4)]
        T[0].add_node((0, 0, 0), pos=np.array([0, 0, 0]))
        T[0].add_node((1, 1, 0), pos=np.array([1, 1, 0]))
        T[0].add_node((1, 0, 1), pos=np.array([1, 0, 1]))
        T[0].add_node((0, 1, 1), pos=np.array([0, 1, 1]))
        T[0].add_node((0.5, 0.5, 0.5), pos=np.array([0.5, 0.5, 0.5]))
        translation = [
            np.array([1, 1, 0]),
            np.array([1, 0, 1]),
            np.array([0, 1, 1])
            ]
        for i, t in enumerate(translation):
            for n in T[0].nodes():
                T[i+1].add_node(tuple(n+t), pos=T[0].nodes[n]['pos']+t)
        for t in T:
            D.add_nodes_from(t.nodes(data=True))

        return D

    def diamond_lattice(self, num_periods):

        """
        Set the internal graph as diamond lattice.

        Args:
            num_periods (int):\n
                Repetition number for the unit cell.

        """

        D = self.diamond_unit_cell()
        self.periodic_cell_structure(D, num_periods)


class NetworkxLaves(NetworkxCrystal):

    """
    A derived class for spatial, Laves graphs.

    """

    def __init__(self, num_periods):
        """
        A constructor for laves crystal objects, setting default values
        for the interal graph objects and geometry.
        """
        super(NetworkxLaves, self).__init__()
        self.lattice_constant = 2.
        self.laves_lattice(num_periods)

    def laves_lattice(self, num_periods):

        """
        Set the internal graph as laves lattice.

        Args:
            num_periods (int):\n
                Repetition number for the unit cell.

        """

        # construct single box
        G_aux = nx.Graph()
        if type(num_periods) is not int:
            periods = [range(num_periods[i]) for i in range(3)]
        else:
            periods = [range(num_periods) for i in range(3)]

        fundamental_points = [
            [0, 0, 0],
            [1, 1, 0],
            [1, 2, 1],
            [0, 3, 1],
            [2, 2, 2],
            [3, 3, 2],
            [3, 0, 3],
            [2, 1, 3]
        ]

        for fp in fundamental_points:
            for i in periods[0]:
                for j in periods[1]:
                    for k in periods[2]:

                        pos_n = np.add(fp, [4.*i, 4.*j, 4.*k])
                        G_aux.add_node(tuple(pos_n), pos=pos_n)

        list_nodes = list(G_aux.nodes())
        self.G = nx.Graph()
        H = nx.Graph()

        for i, n in enumerate(G_aux.nodes()):
            H.add_node(n, pos=G_aux.nodes[n]['pos'])

        for i, n in enumerate(list_nodes[:-1]):
            for j, m in enumerate(list_nodes[(i+1):]):

                v = np.subtract(n, m)
                dist = np.dot(v, v)
                if dist == self.lattice_constant:
                    H.add_edge(n, m)

        dict_nodes = {}
        for idx_n, n in enumerate(H.nodes()):
            self.G.add_node(idx_n, pos=H.nodes[n]['pos'])
            dict_nodes.update({n: idx_n})

        for idx_e, e in enumerate(H.edges()):
            u, v = dict_nodes[e[0]], dict_nodes[e[1]]
            self.G.add_edge(u, v)


class NetworkxTriagonalStack(NetworkxCrystal):

    """
    A derived class for spatial, stacked, triangulated graphs, contained in
    hexagonal shapes.

    """

    def __init__(self, stacks, tiling_factor):
        """
        A constructor for stacked, triangulated crystal objects, setting
        default values for the interal graph objects and geometry.
        """
        super(NetworkxTriagonalStack, self).__init__()
        self.triangulated_hexagon_stack(stacks, tiling_factor)

    # define crosslinking procedure between the generated single-layers
    def crosslink_stacks(self):

        """
        Crosslink the stacked hexagons to closest layer neighbor.
        """

        for i, n in enumerate(self.G.nodes()):
            self.G.nodes[n]['label'] = i

        if self.stacks > 1:

            labels_n = nx.get_node_attributes(self.G, 'label')
            sorted_label_n_list = sorted(labels_n, key=labels_n.__getitem__)

            for n in sorted_label_n_list:
                if n[2] != self.stacks-1:

                    u = (n[0], n[1], n[2])
                    v = (n[0], n[1], n[2]+1)

                    self.G.add_edge(u, v)

    # auxillary function,  construct triangulated hex grid upper and lower
    # wings
    def construct_spine_stack(self, z, n):

        """
        Generate new nodes and connections for spines of stacked hexagons of
         the internal graph and set spine length internally.

        Args:
            z (float):\n
                The current stack indicator.
            n (int):\n
                Length of the hexagon's outer sites.

        """

        self.spine = 2*(n-1)
        self.G.add_node((0, 0, z), pos=(0., 0., z))
        for m in range(self.spine):

            self.G.add_node((m+1, 0, z), pos=((m+1), 0., z))
            u = (m, 0, z)
            v = (m+1, 0, z)

            self.G.add_edge(u, v)

    def construct_wing_stack(self, z, a, n):

        """
        Generate new nodes and connections from the spines for each stacked
        hexagon.

        Args:
            z (float):\n
                The current stack indicator.
            a (int):\n
                +-1, setting the currently constructed hemisphere.
            n (int):\n
                Length of the hexagon's outer sites.

        """

        for m in range(n-1):
            # m-th floor
            floor_m_nodes = self.spine-(m+1)

            u = (0, a*(m+1), z)
            v = (0, a*m, z)
            w = (1, a*m, z)

            self.G.add_node(u, pos=((m+1)/2., a*(np.sqrt(3.)/2.)*(m+1), z))

            self.G.add_edge(u, v)
            self.G.add_edge(u, w)

            for p in range(floor_m_nodes):
                # add 3-junctions
                u = (p+1, a*(m+1), z)
                v = (p+1, a*m, z)
                w = (p+2, a*m, z)
                x = (p, a*(m+1), z)

                ps = (((p+1)+(m+1)/2.), a*(np.sqrt(3.)/2.)*(m+1), z)
                self.G.add_node(u, pos=ps)

                self.G.add_edge(u, v)
                self.G.add_edge(u, w)
                self.G.add_edge(u, x)

    # construct full triangulated hex grids as skeleton of a stacked structure
    def triangulated_hexagon_stack(self, stacks, num_periods):

        """
        Set the internal graph as stacked, triangulated lattice, contained in
        hexagonal shapes.

        Args:
            stacks (int):\n
                The number of layers.
            num_periods (int):\n
                Length of the hexagon's spine.

        """

        self.stacks = stacks
        for z in range(self.stacks):

            # construct spine for different levels of lobule
            self.construct_spine_stack(z, num_periods)

            # construct lower/upper halfspace
            self.construct_wing_stack(z, -1,  num_periods)
            self.construct_wing_stack(z,  1,  num_periods)

        self.crosslink_stacks()


# 2D
class NetworkxSquare(NetworkxCrystal):

    """
    A derived class for spatial, simpley tiled graphs.

    """

    def __init__(self, tiling_factor):

        """
        A constructor for simple tiled crystal objects, setting default values
        for the interal graph objects and geometry
        """
        super(NetworkxSquare, self).__init__()
        self.square_grid(tiling_factor)

    def square_grid(self, num_periods):

        """
        Set the internal graph as square grid.

        """

        if type(num_periods) is not int:
            a = [range(0, num_periods[0]+1), range(0, num_periods[1]+1)]
        else:
            a = [range(0, num_periods+1), range(0, num_periods+1)]

        for x in a[0]:
            for y in a[1]:
                self.G.add_node((x, y), pos=(x, y, 0))

        list_n = list(self.G.nodes())
        dict_d = {}
        threshold = 1.
        for idx_n, n in enumerate(list_n[:-1]):
            for m in list_n[idx_n+1:]:
                p = np.array(self.G.nodes[n]['pos'])
                q = np.array(self.G.nodes[m]['pos'])
                dict_d[(n, m)] = np.linalg.norm(p-q)

        for nm in dict_d:
            if dict_d[nm] <= threshold:
                self.G.add_edge(*nm)


class NetworkxTriagonalPlanar(NetworkxCrystal):

    """
    A derived class for spatial, planar triangulated graphs.

    """

    def __init__(self,  tiling_factor):
        """
        A constructor for a planar triangulated crystal objects, setting
        default values for the interal graph objects and geometry
        """
        super(NetworkxTriagonalPlanar, self).__init__()
        self.triangulated_hexagon_lattice(tiling_factor)
    # I) construct and define one-layer hex
    # auxillary function,  construct triangulated hex grid upper and lower
    # wings

    def construct_wing(self, a, n):

        """
        Generate new nodes and connections from the spines of the hexagon.

        Args:
            a (int):\n
                +-1, setting the currently constructed hemisphere.
            n (int):\n
                Length of the hexagon's outer sites.

        """
        for m in range(n-1):
            # m-th floor
            floor_m_nodes = self.spine - (m+1)

            u = (0, a*(m+1))
            v = (0, a*m)
            w = (1, a*m)
            ps = np.array([(m+1)/2., a*(np.sqrt(3.)/2.)*(m+1)])

            self.G.add_node(u, pos=ps)
            self.G.add_edge(u, v)
            self.G.add_edge(u, w)

            for p in range(floor_m_nodes):
                # add 3-junctions
                u = (p+1, a*(m+1))
                v = (p+1, a*m)
                w = (p+2, a*m)
                x = (p, a*(m+1))
                ps = np.array([((p+1)+(m+1)/2.), a*(np.sqrt(3.)/2.)*(m+1)])

                self.G.add_node(u, pos=ps)

                self.G.add_edge(u, v)
                self.G.add_edge(u, w)
                self.G.add_edge(u, x)

    # construct full triangulated hex grid as skeleton
    def triangulated_hexagon_lattice(self, n):

        """
        Generate new nodes and connections for the spine of the hexagon.

        Args:
            n (int):\n
                Length of the hexagon's outer sites.

        """

        # construct spine
        self.spine = 2*(n-1)
        self.G.add_node((0, 0), pos=np.array([0., 0.]))

        for m in range(self.spine):

            self.G.add_node((m+1, 0), pos=np.array([(m+1), 0.]))
            u, v = (m, 0), (m+1, 0)
            self.G.add_edge(u, v)

        # construct lower/upper halfspace
        self.construct_wing(-1, n)
        self.construct_wing(1, n)


class NetworkxHexagonal(NetworkxCrystal):

    """
    A derived class for spatial, planar hexagonal graphs.

    """

    def __init__(self, tiling_factor, periodic=False):
        """
        A constructor for a planar, hexagonal crystal objects, setting default
        values for the interal graph objects and geometry
        """
        super(NetworkxHexagonal, self).__init__()
        self.hexagonal_grid(tiling_factor, periodic)

    def hexagonal_grid(self, tiling_factor, periodic_bool):

        """
        Set the internal graph as hexagonal grid, using the networkx graph
        generator.
        """

        # generate hexagonal grid
        m = 2*tiling_factor+1
        n = 2*tiling_factor
        opt = {
            'periodic': periodic_bool,
            'with_positions': True
        }
        self.G = nx.hexagonal_lattice_graph(m, n, **opt)

        # set embedding data
        for n in self.G.nodes():
            self.G.nodes[n]['pos'] = np.array(self.G.nodes[n]['pos'])
