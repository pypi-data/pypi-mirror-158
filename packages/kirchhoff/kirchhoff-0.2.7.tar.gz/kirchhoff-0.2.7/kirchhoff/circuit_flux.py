# @Author: Felix Kramer <kramer>
# @Date:   07-11-2021
# @Email:  felixuwekramer@proton.me
# @Last modified by:   kramer
# @Last modified time: 08-07-2022


import numpy as np
import sys
import pandas as pd
from dataclasses import dataclass
from kirchhoff.circuit_flow import FlowCircuit
import kirchhoff.init_crystal as init_crystal
import kirchhoff.init_random as init_random


def initialize_flux_circuit_from_random(
        random_type='default',
        periods=10,
        sidelength=1
        ):

    """
    Initialize a flux circuit from a random, spatially embedded networkx graph.

    Args:
        random_type (string):\n
            The type of random lattice to be constructed(voronoi_planar,
            voronoi_volume).
        periods (int):\n
            Number of random points.
        sidelength (float):\n
            The box size into which random points in space are generated.

    Returns:
        flux_circuit: A flux_circuit object.

    """

    input_graph = init_random.init_graph_from_random(
            random_type,
            periods,
            sidelength
            )
    kirchhoff_graph = FluxCircuit(input_graph)
    kirchhoff_graph.info = kirchhoff_graph.set_info(input_graph, random_type)

    return kirchhoff_graph


def initialize_flux_circuit_from_crystal(crystal_type='default', periods=1):

    """
    Initialize a flux circuit from a spatially embedded, crystal networkx
    graph.

    Args:
        crystal_type (string):\n
            The type of crystal skeleton (default, simple, chain, bcc, fcc,
            diamond, laves, square, hexagonal, trigonal_planar).
        periods (int):\n
            Repetition number of the lattice's unit cell.

    Returns:
        flux_circuit: A flux_circuit object.

    """

    input_graph = init_crystal.init_graph_from_crystal(crystal_type, periods)
    kirchhoff_graph = FluxCircuit(input_graph)
    kirchhoff_graph.info = kirchhoff_graph.set_info(input_graph, crystal_type)

    return kirchhoff_graph


def setup_default_flux_circuit(skeleton=None, diffusion=None, absorption=None):

    """
    Initialize a flux circuit from a given networkx graph.

    Args:
        skeleton (nx.Graph):\n
            A networkx graph.
        diffusion (float):\n
            Diffusion constant.
        absorption (float):\n
            Absorption rate.

    Returns:
        flux_circuit: A flow_circuit object.

    """

    kirchhoff_graph = FluxCircuit(skeleton)
    kirchhoff_graph.set_source_landscape(mode='dipole_point')
    kirchhoff_graph.set_plexus_landscape()
    kirchhoff_graph.set_solute_landscape()

    kirchhoff_graph.scales['diffusion'] = diffusion
    kirchhoff_graph.scales['absorption'] = absorption
    kirchhoff_graph.set_absorption_landscape()
    kirchhoff_graph.set_geom_landscape()

    idx = np.where(kirchhoff_graph.nodes['solute'] > 0.)[0]
    sol = kirchhoff_graph.nodes['solute'][idx]
    kirchhoff_graph.scales['sum_flux'] = np.sum(sol)

    return kirchhoff_graph


@dataclass
class FluxCircuit(FlowCircuit):

    """
    A derived class for flux circuits.

    Attributes
    ----------

        solute_mode (dictionary):\n
            A dictionary of custom solute outflux/influx boundaries.
        absorption_mode (dictionary):\n
            A dictionary of custom absorption rate initializations.
        geom_mode (dictionary):\n
            A dictionary of custom plexus geometrical initializations.

    """

    def __post_init__(self):

        self.init_circuit()
        self.set_flowModes()

        e = self.G.number_of_edges()
        n = self.G.number_of_nodes()

        newNodeAttr = ['solute', 'concentration']
        for k in newNodeAttr:
            self.nodes[k] = np.zeros(n)

        newEdgeAttr = [
            'peclet',
            'absorption',
            'length',
            'radius',
            'radius_sq',
            'uptake'
            ]
        for k in newEdgeAttr:
            self.edges[k] = np.zeros(e)

        newScaleAttr = ['flux', 'sum_flux', 'diffusion', 'absorption']
        for k in newScaleAttr:
            self.scales.update({k: 1})

        newGraphAttr = [
            'solute_mode',
            'absorption_mode',
            'geom_mode'
            ]

        for k in newGraphAttr:
            self.graph.update({k: ''})

        self.solute_mode = {
            'default': self.init_solute_default,
            'custom': self.init_solute_custom
        }

        self.absorption_mode = {
            'default': self.init_absorption_default,
            'random': self.init_absorption_random,
            'custom': self.init_absorption_custom
        }

        self.geom_mode = {
            'default': self.init_geom_default,
            'random': self.init_geom_random,
            'custom': self.init_geom_custom
        }

    # set injection and outlet of metabolites
    def set_solute_landscape(self, mode='default', **kwargs):

        """
        Set the internal bounday state of sinks and sources.

        Args:
            mode (string):\n
                The specific solute mode.
            kwargs (dictonary):\n
                Solute attribute specifiers, optional.

        """

        # optional keywords
        if 'solute' in kwargs:
            self.custom = kwargs['solute']

        # call init sources
        if mode in self.solute_mode.keys():

            self.solute_mode[mode]()

        else:
            sys.exit(
                'Whooops, Error: Define Input/output-flows for the network.'
                )

        self.graph['solute_mode'] = mode

    def init_solute_default(self):

        """
        Set solute out/influx accordingly to the sinks-sources boundaries.
        """

        vals = [1, -1, 0]

        for j, n in enumerate(self.list_graph_nodes):

            if self.nodes['source'][j] > 0:
                self.set_solute(j, n, vals[0])

            elif self.nodes['source'][j] < 0:
                self.set_solute(j, n, vals[1])

            else:
                self.set_solute(j, n, vals[2])

    def init_solute_custom(self):

        """
        Set custom solute out/influx boundaries.
        """

        if len(self.custom.keys()) == len(self.list_graph_nodes):

            for j, node in enumerate(self.list_graph_nodes):

                f = self.custom[node]*self.scales['flux']
                self.nodes.at[j, 'solute'] = f
                self.G.nodes[node]['solute'] = f

        else:

            print(
                'Warning, custom solute values ill defined, setting default!'
                )
            self.init_solute_default()

    def set_solute(self, idx, nodes, vals):

        """
        Set nodal solute in/outflux attributes.

        Args:
            idx (int): The dataframe vertex indicator.
            nodes (int): The corresponding networkx graph node.
            vals (float): Solute value to be set.
        """

        f = self.scales['flux']*vals
        self.nodes.at[idx, 'solute'] = f
        self.G.nodes[nodes]['solute'] = f

    # set spatial pattern of solute absorption rate
    def set_absorption_landscape(self, mode='default', **kwargs):

        """
        Set the internal bounday state of sinks and sources.

        Args:
            mode (string):\n
                The specific absorption mode.
            kwargs (dictonary):\n
                Absorption attribute specifiers, optional.

        """

        # optional keywords
        if 'absorption' in kwargs:
            self.custom = kwargs['absorption']

        # call init sources
        if mode in self.absorption_mode.keys():

            self.absorption_mode[mode]()

        else:
            sys.exit(
                '''
                Whooops, Error: Define absorption rate pattern for the network.
                '''
                )

        self.graph['absorption_mode'] = mode

    def init_absorption_default(self):
        """
        Set a constant absorption rate landscape.
        """

        num_e = self.G.number_of_edges()
        self.edges['absorption'] = np.ones(num_e)*self.scales['absorption']

    def init_absorption_random(self):
        """
        Set a random absorption rate landscape.
        """

        num_e = self.G.number_of_edges()
        rnd = np.random.rand(num_e)
        self.edges['absorption'] = rnd*self.scales['absorption']

    def init_absorption_custom(self):

        """
        Set a custom absorption rate landscape.
        """

        if len(self.custom.keys()) == len(self.list_graph_edges):
            for j, edge in enumerate(self.list_graph_edges):

                c = self.custom[edge]*self.scales['absorption']
                self.edges['absorption'][j] = c
        else:

            print(
                '''
                Warning, custom absorption values ill defined, setting default!
                '''
                )
            self.init_absorption_default()

    # set spatial pattern of length and radii
    def set_geom_landscape(self, mode='default', **kwargs):

        """
        Set the internal bounday state of sinks and sources.

        Args:
            mode (string):\n
                The specific geometric initialization mode.
            kwargs (dictonary):\n
                Geometric initialization specifiers, optional.

        """

        # optional keywords
        if 'geom' in kwargs:
            self.custom = kwargs['geom']

        # call init sources
        if mode in self.geom_mode.keys():

            self.geom_mode[mode]()

        else:
            sys.exit(
                'Whooops, Error: Define micro geometrics for the network.'
                )

        self.graph['geom_mode'] = mode

    def init_geom_default(self):

        """
        Set a constant length for all connections.
        """

        num_e = self.G.number_of_edges()
        self.edges['length'] = np.ones(num_e)*self.scales['length']
        conductivity = self.edges['conductivity']
        k = self.scales['conductance']
        self.edges['radius'] = np.power(conductivity/k, 0.25)
        self.edges['radius_sq'] = np.sqrt(conductivity/k)

    def init_geom_random(self):

        """
        Set a random length for all connections.
        """

        num_e = self.G.number_of_edges()
        self.edges['length'] = np.random.rand(num_e)*self.scales['length']

    def init_geom_custom(self, flux):

        """
        Set a custom length for all connections.
        """

        if len(self.custom.keys()) == len(self.list_graph_edges):
            for j, edge in enumerate(self.list_graph_edges):

                c = self.custom[edge]*self.scales['length']
                self.edges['length'][j] = c
        else:
            print(
                '''
                Warning, custom absorption values ill defined, setting default!
                '''
                )
            self.init_geom_default()

    def get_nodes_data(self):

        """
        Get internal nodal DataFrame columns by keywords.

        Args:
            args (list):\n
                A list of keywords to check for in the internal DataFrames.

        Returns:
            pd.DataFrame: A cliced DataFrame.

        Raises:
            Exception: description

        """

        dn = pd.DataFrame(self.nodes[['source', 'solute', 'concentration']])

        return dn

    def get_edges_data(self, **kwargs):

        """
        Get internal nodal DataFrame columns by keywords.

        Args:
            args (list):\n
                A list of keywords to check for in the internal DataFrames.

        Returns:
            pd.DataFrame: A cliced DataFrame.

        Raises:
            Exception: description

        """

        de = pd.DataFrame(
            self.edges[
                [
                    'conductivity',
                    'flow_rate',
                    'absorption',
                    'uptake',
                    'peclet',
                    'length'
                    ]
                ]
            )

        if 'width' in kwargs:
            w = np.absolute(self.edges[kwargs['width']].to_numpy())
            de['weight'] = w*self.draw_weight_scaling
        else:
            w = np.power(self.edges['conductivity'].to_numpy(), 0.25)
            de['weight'] = w*self.draw_weight_scaling

        return de
