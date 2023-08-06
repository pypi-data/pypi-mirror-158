# # @Author: Felix Kramer <kramer>
# # @Date:   23-06-2021
# # @Email:  kramer@mpi-cbg.de
# # @Project: phd_network_remodelling
# @Last modified by:   felix
# @Last modified time: 2022-07-02T13:51:06+02:00

import numpy as np
from dataclasses import dataclass, field
# custom
from .base import model


@dataclass
class meigel(model):
    """
    The network adaptation model according to Meigel/Horton et al, based on
    minimization of supply-demand mismatch, with a simplified metabolite uptake
    model though:
        Meigel et al, Flow rate of transport network controls uniform
        metabolite supply to tissue, Journal of the Royal Society Interface,
        2018\n
        Kramer&Modes, On biological flow networks: Antagonism between
        hydrodynamic and metabolic stimuli as driver of topological
        transitions, arXiv:2111.04326
    The system's cost function is given as:\n
    .. math::
        \\Gamma = \\sum_{e} \\left[ \\Phi_e-\\Phi_0 \\right]^2
    Attributes:
        pars (dict):\n
         The specific model parameters \\alpha_0, \\alpha_1 and demand \\Phi_0

        ivp_options (dict):\n
         Information to generate the internal solver_options. Providing t0,t1
         number of evaluation and x0.\n
        model_args (list):\n
         Model specific paramerets need to evaluate the update rules of the DS
         \n
        solver_options (dict):\n
         Specifying runtime and evaluation marks. \n
        events (dict):\n
         Events to consier, here in gernal flatlining events which allow for
         early termination of stiff simulations. \n
        null_decimals (in):\n
         description \n

    Methods:
        init()
            The model post_init function.
        update_event_func()
            Update the event function and ensures that solver_options are set.
        flatlining_default(t, x_0, *args)
            The default flatlining function for determining the terminal event
            of the dynamical system.
        flatlining_dynamic(t, x_0, *args)
            The dynamic flatlining function for determining the terminal event
            of the dynamical system.
        set_model_parameters(model_pars)
            Set internal model arguments array.
        set_solver_options(solv_opt)
            Set internal solver_options and update event function.
        calc_update_stimuli(t, x_0, *args)
            The dynamic system's temporal update rule, computing the gradient
            -dF for dx/dt.
        calc_cost_stimuli(t, x_0, *args)
            Computes the dynamic system's Lyapunov function and its gradient.
        get_stimuli_pars(self, flow, x_0)
            Update flow & pressure landscapes, recompute conductivity as well
            as squared quantities.

    """

    pars: dict = field(default_factory=dict, init=True, repr=True)

    def __post_init__(self):

        self.init()

        self.solver_options.update({'events': 'default'})
        if self.pars:
            self.set_model_parameters(self.pars)
        else:
            self.model_args = [1.]

    def calc_update_stimuli(self, t, x_0, flux, phi0):

        m = len(x_0)
        dx = np.zeros(m)
        # c, B_new = flux.calc_profile_concentration()
        flux.update_transport_matrix(x_0)
        flux.solve_absorbing_boundary()

        phi = flux.calc_absorption()
        J_phi = flux.calc_absorption_jacobian()
        phi0 = np.ones(m)*phi0

        for i in range(m):
            dx[i] = -2.*np.sum(
                    np.multiply(
                        np.subtract(phi, phi0),
                        J_phi[i, :])
                    )

        return dx

    def calc_cost_stimuli(self, t, x_0, flux, phi0):

        m = len(x_0)
        cnd, p_sq = self.get_stimuli_pars(flux, x_0)
        flux.circuit.C = cnd[:]
        flux.circuit.R = x_0[:]

        # c, B_new = flux.calc_profile_concentration()
        flux.update_transport_matrix(x_0)
        flux.solve_absorbing_boundary()
        phi = flux.calc_absorption()
        phi0 = np.ones(m)*phi0
        F = np.sum(np.power(np.subtract(phi, phi0), 2))

        # J_phi = flux.calc_absorption_jacobian()
        # dF = np.array([ 2.*np.sum(np.multiply(
        # np.subtract(phi, phi0), J_phi[j, :])) for j in range(m)])
        dF = -self.calc_update_stimuli(t, x_0, flux, phi0)

        return F, dF

    def calc_cost_system(self, t, x_0, flux, phi0):

        m = len(x_0)
        cnd, p_sq = self.get_stimuli_pars(flux, x_0)

        flux.circuit.C = cnd[:]
        flux.circuit.R = x_0[:]

        flux.update_transport_matrix(x_0)
        phi = flux.calc_absorption()
        phi0 = np.ones(m)*phi0
        F = np.sum(np.power(np.subtract(phi, phi0), 2))

        return F

    def get_stimuli_pars(self, flux, x_0):

        k = flux.circuit.scales['conductance']
        src = flux.circuit.nodes['source']

        x_sq = np.power(x_0, 2)
        cnd = flux.calc_conductivity_from_cross_section(x_sq, k)
        p_sq, q_sq = flux.calc_sq_flow(cnd, src)

        return cnd, p_sq


@dataclass
class link(meigel):
    """
    The network adaptation model according to Meigel/Horton et al, based on
    flow dissipation-volume minimization in combination with supply-demand
    competition of conductivity costs as published for example:
        Kramer&Modes, On biological flow networks: Antagonism between
        hydrodynamic and metabolic stimuli as driver of topological
        transitions, arXiv:2111.04326

    The system's cost function is given as:\n
    .. math::
        \\Gamma = \\sum_{e}\\left( \\alpha_1 r_e^4\\Delta p_e^2 +
        \\alpha_0 r_e^2 + \\left[ \\Phi_e-\\Phi_0 \\right]^2 \\right)
    Attributes:
        pars (dict):\n
         The specific model parameters \\alpha_0, \\alpha_1 and demand \\Phi_0

        ivp_options (dict):\n
         Information to generate the internal solver_options. Providing t0,t1
         number of evaluation and x0.\n
        model_args (list):\n
         Model specific paramerets need to evaluate the update rules of the DS
         \n
        solver_options (dict):\n
         Specifying runtime and evaluation marks. \n
        events (dict):\n
         Events to consier, here in gernal flatlining events which allow for
         early termination of stiff simulations. \n
        null_decimals (in):\n
         description \n

    Methods:
        init()
            The model post_init function.
        update_event_func()
            Update the event function and ensures that solver_options are set.
        flatlining_default(t, x_0, *args)
            The default flatlining function for determining the terminal event
            of the dynamical system.
        flatlining_dynamic(t, x_0, *args)
            The dynamic flatlining function for determining the terminal event
            of the dynamical system.
        set_model_parameters(model_pars)
            Set internal model arguments array.
        set_solver_options(solv_opt)
            Set internal solver_options and update event function.
        calc_update_stimuli(t, x_0, *args)
            The dynamic system's temporal update rule, computing the gradient
            -dF for dx/dt.
        calc_cost_stimuli(t, x_0, *args)
            Computes the dynamic system's Lyapunov function and its gradient.
        get_stimuli_pars(self, flow, x_0)
            Update flow & pressure landscapes, recompute conductivity as well
            as squared quantities.

    """

    def __post_init__(self):

        self.init()

        self.solver_options.update({'events': 'default'})
        if self.pars:
            self.set_model_parameters(self.pars)
        else:
            self.model_args = [1., 1., 1.]

    def calc_update_stimuli(self, t, x_0, flux, phi0, alpha_0, alpha_1):

        m = len(x_0)

        # calc absorption stimulus
        dx1 = np.zeros(m)

        flux.update_transport_matrix(x_0)
        flux.solve_absorbing_boundary()

        phi = flux.calc_absorption()
        J_phi = flux.calc_absorption_jacobian()
        phi0 = np.ones(m)*phi0

        for i in range(m):
            dx1[i] = -2.*np.sum(
                    np.multiply(
                        np.subtract(phi, phi0),
                        J_phi[i, :])
                )

        # calc hydrodynamic stimulus
        r_sq = np.power(x_0, 2)
        k = flux.circuit.scales['conductance']
        src = flux.circuit.nodes['source']
        conductivity = flux.calc_conductivity_from_cross_section(r_sq, k)
        dP, P = flux.calc_pressure(conductivity, src)

        s1 = 2.*alpha_1*np.multiply(np.power(dP, 2), r_sq)
        s2 = alpha_0*np.ones(m)
        ds = np.subtract(s1, s2)
        dx2 = 2*np.multiply(ds, x_0)

        return np.add(dx1, dx2)

    def calc_cost_stimuli(self, t, x_0, flux, phi0, alpha_0, alpha_1):

        m = len(x_0)
        cnd, p_sq = self.get_stimuli_pars(flux, x_0)
        flux.circuit.C = cnd[:]
        flux.circuit.R = x_0[:]

        # c, B_new = flux.calc_profile_concentration()
        flux.update_transport_matrix(x_0)
        flux.solve_absorbing_boundary()
        phi = flux.calc_absorption()
        phi0 = np.ones(m)*phi0
        F = np.sum(np.power(np.subtract(phi, phi0), 2))

        f1 = alpha_1*np.multiply(p_sq, np.power(x_0, 4))
        f2 = alpha_0*np.power(x_0, 2)
        c2 = np.sum(np.add(f1, f2))

        F += c2
        # J_phi = flux.calc_absorption_jacobian()
        # dF = np.array([ 2.*np.sum(
        # np.multiply(np.subtract(phi, phi0), J_phi[j, :])) for j in range(m)])
        dF = -self.calc_update_stimuli(t, x_0, flux, phi0, alpha_0, alpha_1)

        return F, dF

    def calc_cost_system(self, t, x_0, flux, phi0, alpha_0, alpha_1):

        m = len(x_0)
        cnd, p_sq = self.get_stimuli_pars(flux, x_0)

        flux.circuit.C = cnd[:]
        flux.circuit.R = x_0[:]

        flux.update_transport_matrix(x_0)
        phi = flux.calc_absorption()
        phi0 = np.ones(m)*phi0
        F = np.sum(np.power(np.subtract(phi, phi0), 2))

        f1 = alpha_1*np.multiply(p_sq, np.power(x_0, 4))
        f2 = alpha_0*np.power(x_0, 2)
        c2 = np.sum(np.add(f1, f2))
        F += c2

        return F

    def get_stimuli_pars(self, flux, x_0):

        k = flux.circuit.scales['conductance']
        src = flux.circuit.nodes['source']

        x_sq = np.power(x_0, 2)
        cnd = flux.calc_conductivity_from_cross_section(x_sq, k)
        p_sq, q_sq = flux.calc_sq_flow(cnd, src)

        return cnd, p_sq


# @dataclass
# class volume(link):
#
#     def __post_init__(self):
#
#         self.init()
#
#         self.solver_options.update({'events': 'default'})
#         if self.pars:
#             self.set_model_parameters(self.pars)
#         else:
#             self.model_args = [1., 1., 1.]
#
#     # def hexagonal_grid(self, *args):
#     #
#     #     tiling_factor, sidelength, conductance,flow,periodic_bool=args
#     #     self.k=conductance
#     #     self.l=sidelength
#     #     self.f=flow
#     #
#     #     m=2*tiling_factor+1
#     #     n=2*tiling_factor
#     #     self.G=nx.hexagonal_lattice_graph(
#           m, n, periodic=periodic_bool, with_positions=True)
#     #     for n in self.G.nodes():
#     #         self.G.nodes[n]['label']=self.count_n
#     #         self.G.nodes[n]['pos']=self.l*np.array(self.G.nodes[n]['pos'])
#     #     for e in self.G.edges():
#     #
#     #         self.G.edges[e]['label']=self.count_e
#     #         self.G.edges[e]['slope']=[
# self.G.nodes[e[0]]['pos'],
# self.G.nodes[e[1]]['pos']
# ]
#     #
#     #     # initialze circuit & add attributes
#     #     self.initialize_circuit()
#     #
#     # def set_up_volumes(self,periodic_bool):
#     #
#     #     # set up volumes be aware to work on properly iniced systems
#     #     if periodic_bool:
#     #         T=analyze_graph.tool_box()
#     #         cycle_basis=T.construct_minimum_basis(self.G)
#     #         dict_volumes={}
#     #         dict_idx={}
#     #         dict_counter={}
#     #         for i,e in enumerate(self.G.edges()):
#     #             dict_idx[e]=i
#     #             dict_counter[e]=0
#     #         for i,c in enumerate(cycle_basis):
#     #                 dict_volumes[i]=[]
#     #                 for j,e in enumerate( c.edges() ):
#     #
#     #                     if e in dict_idx:
#     #                         dict_volumes[i].append(dict_idx[e])
#     #                         dict_counter[e]+=1
#     #                     else:
#     #                         dict_volumes[i].append(dict_idx[(e[-1],e[0])])
#     #                         dict_counter[(e[-1],e[0])]+=1
#     #         dict_volumes[len(cycle_basis)]=[]
#     #         for i,e in enumerate(self.G.edges()):
#     #             if dict_counter[e]<2:
#     #                 dict_volumes[len(cycle_basis)].append(dict_idx[e])
#     #
#     #         keys=list(dict_volumes.keys())
#     #         for k in keys:
#     #             if len(dict_volumes[k])>6:
#     #                 del dict_volumes[k]
#     #         self.dict_volumes=dict_volumes
#     #     else:
#     #         print('why bother?')
#
#
#     def calc_update_stimuli(self, t, x_0, flux, phi0, alpha_0, alpha_1):
#
#         m = len(x_0)
#         # calc absorption stimulus
#         dx1 = np.zeros(m)
#
#         flux.update_transport_matrix(x_0)
#         flux.solve_absorbing_boundary()
#         phi0 = np.ones(m)*phi0
#         phi = flux.calc_absorption()
#         J_phi = flux.calc_absorption_jacobian()
#         dphi = np.ones(m)
#
#         # FIX
#         # for i, v in enumerate(K.dict_volumes.keys()):
#         #     dphi[i] = np.sum(phi[K.dict_volumes[v]])-phi0[i]
#         #
#         # for j, e in enumerate(self.list_e):
#         #     for i, v in enumerate(K.dict_volumes.keys()):
#         #         dr[j] -=2.*dphi[i]*np.sum(J_phi[j, K.dict_volumes[v]])
#
#         # calc hydrodynamic stimulus
#         r_sq = np.power(x_0, 2)
#         k = flux.circuit.scales['conductance']
#         src = flux.circuit.nodes['source']
#         conductivity = flux.calc_conductivity_from_cross_section(r_sq, k)
#         dP, P = flux.calc_pressure(conductivity,src)
#
#         s1 = 2.*alpha_1*np.multiply( np.power(dP,2), r_sq)
#         s2 = alpha_0*np.ones(m)
#         ds = np.subtract(s1, s2)
#         dx2 = 2*np.multiply(ds, x_0)
#
#         return np.add(dx1,dx2)
#
#     def calc_cost_stimuli(self, t, x_0, flux, phi0, alpha_0, alpha_1):
#
#         m = len(x_0)
#         cnd, p_sq = self.get_stimuli_pars(flux, x_0)
#         flux.circuit.C = cnd[:]
#         flux.circuit.R = x_0[:]
#
#         # c, B_new = flux.calc_profile_concentration()
#         flux.update_transport_matrix(x_0)
#         flux.solve_absorbing_boundary()
#         phi = flux.calc_absorption()
#         phi0 = np.ones(m)*phi0
#         F = np.sum(np.power(np.subtract(phi, phi0), 2))
#
#         f1 = alpha_1*np.multiply(p_sq, np.power(x_0, 4))
#         f2 = alpha_0 *np.power(x_0, 2)
#         c2 = np.sum(np.add(f1, f2))
#
#         F+=c2
#         # J_phi = flux.calc_absorption_jacobian()
#         # dF = np.array([ 2.*np.sum(np.multiply(
# np.subtract(phi, phi0), J_phi[j, :])) for j in range(m)])
#         dF = -self.calc_update_stimuli(t, x_0, flux, phi0, alpha_0, alpha_1)
#
#         return F, dF
#
#     def calc_cost_system(self, t, x_0, flux, phi0):
#
#         m = len(x_0)
#         cnd, p_sq = self.get_stimuli_pars(flux, x_0)
#
#         flux.circuit.C = cnd[:]
#         flux.circuit.R = x_0[:]
#
#         flux.update_transport_matrix(x_0)
#         phi = flux.calc_absorption()
#         phi0 = np.ones(m)*phi0
#         F = np.sum(np.power(np.subtract(phi, phi0), 2))
#
#         f1 = alpha_1*np.multiply(p_sq, np.power(x_0, 4))
#         f2 = alpha_0 *np.power(x_0, 2)
#         c2 = np.sum(np.add(f1, f2))
#         F+=c2
#
#         return F
#
#     def get_stimuli_pars(self, flux, x_0):
#
#         k = flux.circuit.scales['conductance']
#         src = flux.circuit.nodes['source']
#
#         x_sq = np.power(x_0, 2)
#         cnd = flux.calc_conductivity_from_cross_section(x_sq, k)
#         p_sq, q_sq =flux.calc_sq_flow(cnd, src)
#
#         return cnd, p_sq
