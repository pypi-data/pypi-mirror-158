"""This module implements the UTA algorithm.

Implementation and naming conventions are taken from :cite:p:`siskos2005uta`.
"""

__all__ = ["uta", "uta_star"]

from typing import Any, Dict, List, cast

import numpy as np
from pandas import Series
from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable, lpSum
from pulp import value as pulp_value

from ..core import performance_table as ptable
from ..core.aliases import (
    Function,
    NumericFunction,
    NumericValue,
    PerformanceTable,
)
from ..core.functions import PieceWiseFunction
from ..core.relations import Relation, RelationType
from ..core.scales import Scale, ScaledFunction, get_normalized_scale


def generate_criteria_values_matrix(
    criteria_segments: Dict[str, int],
) -> Dict[str, List[NumericValue]]:
    """Compute criteria values matrix.

    :param criteria_segments: number of segments per criteria
    :return:
    """
    return {
        criterion: np.linspace(0, 1, nb_segments + 1).tolist()
        for criterion, nb_segments in criteria_segments.items()
    }


def generate_marginal_utility_variables(
    criteria_segments: Dict[str, int],
) -> Dict[str, List[LpVariable]]:
    """Return initial marginal utility functions variables.

    :param criteria_segments: number of segments per criteria
    :return:
    """
    return {
        criterion: [
            LpVariable(f"u_{i}_{j}", lowBound=0, cat="continuous")
            for j in range(criteria_segments[criterion] + 1)
        ]
        for i, criterion in enumerate(criteria_segments.keys())
    }


def generate_alternatives_errors_variables(
    alternatives: List[str], prefix: str = "sigma"
) -> Dict[str, LpVariable]:
    """Return initial alternatives errors variables.

    :param alternatives:
    :param prefix: prefix for :class:`pulp.LpVariable` name
    :return:
    """
    return {
        alternative: LpVariable(f"{prefix}_{k}", lowBound=0, cat="continuous")
        for k, alternative in enumerate(alternatives)
    }


def generate_utility_variable(
    alternative_values: Series,
    u_var: Dict[str, List[LpVariable]],
    g_matrix: Dict[str, List[NumericValue]],
) -> Any:
    """Generate initial utility variable for a given alternative.

    :param alternative_values: performances of the given alternative
    :param u_var: utility function variables
    :param g_matrix: criteria values matrix
    :return:

    .. note:: Used by UTA algorithm
    """
    u_i_var = []
    for criterion, val in alternative_values.items():
        g_i = g_matrix[criterion]
        u_i = u_var[criterion]
        for j, g_ij in enumerate(g_i[1:]):
            if val <= g_ij:
                u_i_var.append(
                    u_i[j]
                    + (val - g_i[j])
                    * (u_i[j + 1] - u_i[j])
                    / (g_i[j + 1] - g_i[j])
                )
                break
    return lpSum(u_i_var)


def generate_utility_variable_star(
    alternative_values: Series,
    w_var: Dict[str, List[LpVariable]],
    g_matrix: Dict[str, List[NumericValue]],
) -> Any:
    """Generate initial step utility variable for a given alternative.

    `w_var` corresponds to step increases of the utility variables.

    :param alternative_values: performances of the given alternative
    :param w_var: differential utility function variables
    :param g_matrix: criteria values matrix
    :return:

    .. note:: Used by `UTA*` algorithm
    """
    w_i_var = []
    for criterion, val in alternative_values.items():
        g_i = g_matrix[criterion]
        w_i = w_var[criterion]
        prev_g_ij = g_i[0]
        for g_ij, w_ij in zip(g_i, w_i):
            if val >= g_ij:
                w_i_var.append(w_ij)
            else:
                w_i_var.append(w_ij * (val - prev_g_ij) / (g_ij - prev_g_ij))
                break
            prev_g_ij = g_ij
    return lpSum(w_i_var)


def add_uta_constraints(
    problem: LpProblem,
    performance_table: PerformanceTable,
    u_var: Dict[str, List[LpVariable]],
    sigma_var: Dict[str, LpVariable],
    g_matrix: Dict[str, List[NumericValue]],
    relations: List[Relation],
    delta: NumericValue = 0.001,
):
    """Add UTA constraints to LP problem.

    Each relation in `relations` parameter is a tuple:

    `(a1, a2, r)`

    where `a1` is the first alternative's index, `a2` the second one's and
    `r` a :class:`mcda.core.sorting.RelationType`.

    :param problem:
    :param performance_table:
    :param u_var: utility function variables
    :param sigma_var: alternatives errors variables
    :param g_matrix: criteria values matrix
    :param relations: pairwise relations between alternatives
    :param delta: discrimination threshold for preference relations
    :return:
    """
    # Preference constraints
    u_a = {}
    for k1, k2, relation in relations:
        for k in [k1, k2]:
            if k not in u_a:
                u_a[k] = generate_utility_variable(
                    ptable.get_alternative_values(performance_table, k),
                    u_var,
                    g_matrix,
                )
        if relation == RelationType.PREFERENCE:
            problem += (
                u_a[k1] + sigma_var[k1] - u_a[k2] - sigma_var[k2] >= delta
            )
        else:
            problem += u_a[k1] + sigma_var[k1] - u_a[k2] - sigma_var[k2] == 0

    # Marginal utility monotonicity constraints
    for u_i in u_var.values():
        problem += u_i[0] == 0
        for u_ij, u_ij1 in zip(u_i[:-1], u_i[1:]):
            problem += u_ij1 - u_ij >= 0

    # Utility normalization constraint
    problem += lpSum(u_i[-1] for u_i in u_var.values()) == 1


def add_uta_star_constraints(
    problem: LpProblem,
    performance_table: PerformanceTable,
    w_var: Dict[str, List[LpVariable]],
    sigma_p_var: Dict[str, LpVariable],
    sigma_n_var: Dict[str, LpVariable],
    g_matrix: Dict[str, List[NumericValue]],
    relations: List[Relation],
    delta: NumericValue = 0.001,
):
    """Add UTA constraints to LP problem.

    Each relation in `relations` parameter is a tuple:

    `(a1, a2, r)`

    where `a1` is the first alternative's index, `a2` the second one's and
    `r` a :class:`mcda.core.sorting.RelationType`.

    :param problem:
    :param performance_table:
    :param w_var: differential utility function variables
    :param sigma_p_var: positive alternatives errors variables
    :param sigma_n_var: negative alternatives errors variables
    :param g_matrix: criteria values matrix
    :param relations: pairwise relations between alternatives
    :param delta: discrimination threshold for preference relations
    :return:
    """

    # Preference constraints
    u_a = {}
    for k1, k2, relation in relations:
        for k in [k1, k2]:
            if k not in u_a:
                u_a[k] = generate_utility_variable_star(
                    ptable.get_alternative_values(performance_table, k),
                    w_var,
                    g_matrix,
                )
        if relation == RelationType.PREFERENCE:
            problem += (
                u_a[k1]
                + sigma_n_var[k1]
                + sigma_p_var[k2]
                - u_a[k2]
                - sigma_n_var[k2]
                - sigma_p_var[k1]
                >= delta
            )
        else:
            problem += (
                u_a[k1]
                + sigma_n_var[k1]
                + sigma_p_var[k2]
                - u_a[k2]
                - sigma_n_var[k2]
                - sigma_p_var[k1]
                == 0
            )

    # Normalized utility function
    problem += lpSum(w_ij for w_ij in (w_i for w_i in w_var.values())) == 1


def generate_uta_problem(
    performance_table: PerformanceTable,
    u_var: Dict[str, List[LpVariable]],
    sigma_var: Dict[str, LpVariable],
    g_matrix: Dict[str, List[NumericValue]],
    relations: List[Relation],
    delta: NumericValue = 0.001,
) -> LpProblem:
    """Return initialized UTA problem.

    :param performance_table:
    :param u_var: utility function variables
    :param sigma_var: alternatives errors variables
    :param g_matrix: criteria values matrix
    :param relations: pairwise relations between alternatives
    :param delta: discrimination threshold for preference relations
    :return:
    """
    # Create LP Problem
    prob = LpProblem("UTA", LpMinimize)

    # Add objective function
    prob += lpSum(sigma_var.values())

    # Add constraints
    add_uta_constraints(
        prob, performance_table, u_var, sigma_var, g_matrix, relations, delta
    )

    return prob


def generate_uta_star_problem(
    performance_table: PerformanceTable,
    w_var: Dict[str, List[LpVariable]],
    sigma_p_var: Dict[str, LpVariable],
    sigma_n_var: Dict[str, LpVariable],
    g_matrix: Dict[str, List[NumericValue]],
    relations: List[Relation],
    delta: NumericValue = 0.001,
) -> LpProblem:
    """Return initialized UTA problem.

    :param performance_table:
    :param w_var: differential utility function variables
    :param sigma_p_var: positive alternatives errors variables
    :param sigma_n_var: negative alternatives errors variables
    :param g_matrix: criteria values matrix
    :param relations: pairwise relations between alternatives
    :param delta: discrimination threshold for preference relations
    :return:
    """
    # Create LP Problem
    prob = LpProblem("UTA_star", LpMinimize)

    # Add objective function
    prob += lpSum(sigma_p_var.values()) + lpSum(sigma_n_var.values())

    # Add constraints
    add_uta_star_constraints(
        prob,
        performance_table,
        w_var,
        sigma_p_var,
        sigma_n_var,
        g_matrix,
        relations,
        delta,
    )

    return prob


def normalized_uta(
    performance_table: PerformanceTable,
    criteria_segments: Dict[str, int],
    relations: List[Relation],
    delta: NumericValue = 0.001,
    post_optimality_: bool = False,
    post_optimality_coeff: NumericValue = 0,
    solver_args: dict = None,
) -> Dict[str, NumericFunction]:
    """Compute UTA algorithm on normalized performances.

    :param performance_table:
    :param criteria_segments: number of segments per criteria
    :param relations: pairwise relations between alternatives
    :param delta: discrimination threshold for preference relations
    :param post_optimality_: if ``True``, post-optimality is applied
    :param post_optimality_coeff:
        coefficient used to compute threshold on UTA objective function cost
        when performing post-optimality
    :param solver_args: extra arguments supplied to the solver
    :return: utility functions as criteria functions

    .. note::
        * criteria functions returned are in normalized scales
        * Post-optimality threshold is computed as follows:
          (1 + `post_optimality_coeff`) * F_star
          where F_star is the optimum objective cost computed by UTA
    """
    solver_args = {} if solver_args is None else solver_args

    # Create all UTA variables
    g = generate_criteria_values_matrix(criteria_segments)
    u_var = generate_marginal_utility_variables(criteria_segments)
    sigma_var = generate_alternatives_errors_variables(
        performance_table.index.tolist()
    )

    # Create LP Problem
    prob = generate_uta_problem(
        performance_table, u_var, sigma_var, g, relations, delta
    )

    # Solve problem
    prob.solve(**solver_args)

    # Compute optimum solution
    u_star = {
        criterion: [u_ij.varValue for u_ij in u_i]
        for criterion, u_i in u_var.items()
    }
    F_star = pulp_value(prob.objective)

    if not post_optimality_:
        # Compute optimum utility functions
        criteria_functions: Dict[str, NumericFunction] = {}
        for criterion in u_star.keys():
            points = [
                [g_ij, u_ij]
                for g_ij, u_ij in zip(g[criterion], u_star[criterion])
            ]
            segments = [[p1, p2] for p1, p2 in zip(points[:-1], points[1:])]
            criteria_functions[criterion] = PieceWiseFunction(
                segments=segments
            )
        return criteria_functions

    # Compute post-optimal utility functions
    max_cost = F_star * (1 + post_optimality_coeff)
    return post_optimality(
        performance_table,
        criteria_segments,
        relations,
        delta,
        max_cost,
        solver_args,
    )


def normalized_uta_star(
    performance_table: PerformanceTable,
    criteria_segments: Dict[str, int],
    relations: List[Relation],
    delta: NumericValue = 0.001,
    post_optimality_: bool = False,
    post_optimality_coeff: NumericValue = 0,
    solver_args: dict = None,
) -> Dict[str, NumericFunction]:
    """Compute `UTA*` algorithm on normalized performances.

    :param performance_table:
    :param criteria_segments: number of segments per criteria
    :param relations: pairwise relations between alternatives
    :param delta: discrimination threshold for preference relations
    :param post_optimality_: if ``True``, post-optimality is applied
    :param post_optimality_coeff:
        coefficient used to compute threshold on UTA objective function cost
        when performing post-optimality
    :param solver_args: extra arguments supplied to the solver
    :return: utility functions as criteria functions

    .. note::
        * criteria functions returned are in normalized scales
        * Post-optimality threshold is computed as follows:
          (1 + `post_optimality_coeff`) * F_star
          where F_star is the optimum objective cost computed by `UTA*`
    """
    solver_args = {} if solver_args is None else solver_args

    # Create all UTA variables
    g = generate_criteria_values_matrix(criteria_segments)
    w_var = generate_marginal_utility_variables(criteria_segments)
    sigma_p_var = generate_alternatives_errors_variables(
        performance_table.index.tolist(), "sigma_p"
    )
    sigma_n_var = generate_alternatives_errors_variables(
        performance_table.index.tolist(), "sigma_n"
    )

    # Create LP Problem
    prob = generate_uta_star_problem(
        performance_table, w_var, sigma_p_var, sigma_n_var, g, relations, delta
    )

    # Solve problem
    prob.solve(**solver_args)

    # Compute optimum solution
    w_star = {
        criterion: [w_ij.varValue for w_ij in w_i]
        for criterion, w_i in w_var.items()
    }
    F_star = pulp_value(prob.objective)

    if not post_optimality_:
        # Compute optimum utility functions
        criteria_functions: Dict[str, NumericFunction] = {}
        for criterion in w_star.keys():
            points = [
                [g_ij, sum(w_star[criterion][: (j + 1)])]
                for j, g_ij in enumerate(g[criterion])
            ]
            segments = [[p1, p2] for p1, p2 in zip(points[:-1], points[1:])]
            criteria_functions[criterion] = PieceWiseFunction(
                segments=segments
            )
        return criteria_functions

    # Compute post-optimal utility functions
    max_cost = F_star * (1 + post_optimality_coeff)
    return post_optimality(
        performance_table,
        criteria_segments,
        relations,
        delta,
        max_cost,
        solver_args,
    )


def post_optimality(
    performance_table: PerformanceTable,
    criteria_segments: Dict[str, int],
    relations: List[Relation],
    delta: NumericValue = 0.001,
    max_cost: NumericValue = 0,
    solver_args: dict = None,
) -> Dict[str, NumericFunction]:
    """Compute post-optimality for UTA.

    :param performance_table:
    :param criteria_segments: number of segments per criteria
    :param relations: pairwise relations between alternatives
    :param delta: discrimination threshold for preference relations
    :param max_cost:
        threshold on UTA objective function cost used when performing
        post-optimality
    :param solver_args: extra arguments supplied to the solver
    :return: post optimal utility functions as criteria functions
    """
    solver_args = {} if solver_args is None else solver_args

    g = generate_criteria_values_matrix(criteria_segments)
    u = {
        criterion: [0.0 for _ in range(n + 1)]
        for criterion, n in criteria_segments.items()
    }
    for ci, criterion in enumerate(g.keys()):
        for k, sense in zip(["min", "max"], [LpMinimize, LpMaximize]):
            # Create all UTA variables
            u_var = generate_marginal_utility_variables(criteria_segments)
            sigma_var = generate_alternatives_errors_variables(
                performance_table.index.tolist()
            )

            # Create post-optimality subproblem
            prob = LpProblem(f"post-Optimality-{ci}-{k}", sense)

            # Add objective function
            prob += u_var[criterion][-1]

            # Add post-optimality constraint on UTA objective value
            prob += lpSum(sigma_var.values()) <= max_cost

            # Add regular UTA constraints
            add_uta_constraints(
                prob, performance_table, u_var, sigma_var, g, relations, delta
            )

            # Solve post-optimality subproblem
            prob.solve(**solver_args)

            # Add solution to compounded post-optimality solution
            for i, u_i in u_var.items():
                for j, u_ij in enumerate(u_i):
                    u[i][j] += u_ij.varValue
    # Average solutions
    for i in u:
        for j in range(len(u[i])):
            u[i][j] /= 2 * len(g)

    criteria_functions: Dict[str, NumericFunction] = {}
    for criterion in g.keys():
        points = [
            [g_ij, u_ij] for g_ij, u_ij in zip(g[criterion], u[criterion])
        ]
        segments = [[p1, p2] for p1, p2 in zip(points[:-1], points[1:])]
        criteria_functions[criterion] = PieceWiseFunction(segments=segments)

    return criteria_functions


def star_post_optimality(
    performance_table: PerformanceTable,
    criteria_segments: Dict[str, int],
    relations: List[Relation],
    delta: NumericValue = 0.001,
    max_cost: NumericValue = 0,
    solver_args: dict = None,
) -> Dict[str, NumericFunction]:
    """Compute post-optimality for `UTA*`.

    :param performance_table:
    :param criteria_segments: number of segments per criteria
    :param relations: pairwise relations between alternatives
    :param delta: discrimination threshold for preference relations
    :param max_cost:
        threshold on UTA objective function cost used when performing
        post-optimality
    :param solver_args: extra arguments supplied to the solver
    :return: post optimal utility functions as criteria functions
    """
    solver_args = {} if solver_args is None else solver_args

    g = generate_criteria_values_matrix(criteria_segments)
    w = {
        criterion: [0.0 for _ in range(n + 1)]
        for criterion, n in criteria_segments.items()
    }
    for ci, criterion in enumerate(g.keys()):
        for k, sense in zip(["min", "max"], [LpMinimize, LpMaximize]):
            # Create all UTA variables
            w_var = generate_marginal_utility_variables(criteria_segments)
            sigma_p_var = generate_alternatives_errors_variables(
                performance_table.index.tolist(), "sigma_p"
            )
            sigma_n_var = generate_alternatives_errors_variables(
                performance_table.index.tolist(), "sigma_n"
            )

            # Create post-optimality subproblem
            prob = LpProblem(f"post-Optimality-{ci}-{k}", sense)

            # Add objective function
            prob += lpSum(w_var[criterion])

            # Add post-optimality constraint on UTA objective value
            prob += (
                lpSum(sigma_p_var.values()) + lpSum(sigma_n_var.values())
                <= max_cost
            )

            # Add regular UTA constraints
            add_uta_star_constraints(
                prob,
                performance_table,
                w_var,
                sigma_p_var,
                sigma_n_var,
                g,
                relations,
                delta,
            )

            # Solve post-optimality subproblem
            prob.solve(**solver_args)

            # Add solution to compounded post-optimality solution
            for i, w_i in w_var.items():
                for j, w_ij in enumerate(w_i):
                    w[i][j] += w_ij.varValue
    # Average solutions
    for i in w:
        for j in range(len(w[i])):
            w[i][j] /= 2 * len(g)

    # Compute optimum utility functions
    criteria_functions: Dict[str, NumericFunction] = {}
    for criterion in g.keys():
        points = [
            [g_ij, sum(w[criterion][: (j + 1)])]
            for j, g_ij in enumerate(g[criterion])
        ]
        segments = [[p1, p2] for p1, p2 in zip(points[:-1], points[1:])]
        criteria_functions[criterion] = PieceWiseFunction(segments=segments)
    return criteria_functions


def uta(
    performance_table: PerformanceTable,
    criteria_scales: Dict[str, Scale],
    criteria_segments: Dict[str, int],
    relations: List[Relation],
    delta: NumericValue = 0.001,
    post_optimality_: bool = False,
    post_optimality_coeff: NumericValue = 0,
    solver_args: dict = None,
) -> Dict[str, Function]:
    """Compute UTA algorithm.

    :param performance_table:
    :param criteria_scales:
    :param criteria_segments: number of segments per criteria
    :param relations: pairwise relations between alternatives
    :param delta: discrimination threshold for preference relations
    :param post_optimality_: if ``True``, post-optimality is applied
    :param post_optimality_coeff:
        coefficient used to compute threshold on UTA objective function cost
        when performing post-optimality
    :param solver_args: extra arguments supplied to the solver
    :return: utility functions as criteria functions

    .. note::
        Post-optimality threshold is computed as follows:
        (1 + `post_optimality_coeff`) * F_star
        where F_star is the optimum objective cost computed by UTA
    """
    _performance_table = ptable.normalize(performance_table, criteria_scales)

    normalized_functions = normalized_uta(
        _performance_table,
        criteria_segments,
        relations,
        delta,
        post_optimality_,
        post_optimality_coeff,
        solver_args,
    )

    normalized_scale = get_normalized_scale()
    criteria_functions: Dict[str, Function] = {}
    # Denormalize utility functions
    for c in normalized_functions.keys():
        f = cast(Function, normalized_functions[c])
        criteria_functions[c] = ScaledFunction(
            f, normalized_scale
        ).transform_to(criteria_scales[c])

    return criteria_functions


def uta_star(
    performance_table: PerformanceTable,
    criteria_scales: Dict[str, Scale],
    criteria_segments: Dict[str, int],
    relations: List[Relation],
    delta: NumericValue = 0.001,
    post_optimality_: bool = False,
    post_optimality_coeff: NumericValue = 0,
    solver_args: dict = None,
) -> Dict[str, Function]:
    """Compute `UTA*` algorithm.

    :param performance_table:
    :param criteria_scales:
    :param criteria_segments: number of segments per criteria
    :param relations: pairwise relations between alternatives
    :param delta: discrimination threshold for preference relations
    :param post_optimality_: if ``True``, post-optimality is applied
    :param post_optimality_coeff:
        coefficient used to compute threshold on UTA objective function cost
        when performing post-optimality
    :param solver_args: extra arguments supplied to the solver
    :return: utility functions as criteria functions

    .. note::
        Post-optimality threshold is computed as follows:
        (1 + `post_optimality_coeff`) * F_star
        where F_star is the optimum objective cost computed by UTA
    """
    _performance_table = ptable.normalize(performance_table, criteria_scales)

    normalized_functions = normalized_uta_star(
        _performance_table,
        criteria_segments,
        relations,
        delta,
        post_optimality_,
        post_optimality_coeff,
        solver_args,
    )

    normalized_scale = get_normalized_scale()
    criteria_functions: Dict[str, Function] = {}
    # Denormalize utility functions
    for c in normalized_functions.keys():
        f = cast(Function, normalized_functions[c])
        criteria_functions[c] = ScaledFunction(
            f, normalized_scale
        ).transform_to(criteria_scales[c])

    return criteria_functions
