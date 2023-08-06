"""Functions for creating supercells for defect calculations."""

from __future__ import annotations

import logging

import numpy as np
from pymatgen.analysis.structure_matcher import ElementComparator, StructureMatcher

# from ase.build import find_optimal_cell_shape, get_deviation_from_optimal_cell_shape
# from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.core import Structure

__author__ = "Jimmy Shen"
__copyright__ = "Copyright 2022, The Materials Project"
__maintainer__ = "Jimmy Shen @jmmshn"
__date__ = "Feb 11, 2022"

logger = logging.getLogger(__name__)


def get_sc_fromstruct(
    base_struct: Structure,
    min_atoms: int = 80,
    max_atoms: int = 240,
    min_length: float = 10.0,
) -> np.ndarray | np.array | None:
    """Generate the best supercell from a unitcell.

    The CubicSupercellTransformation from PMG is much faster but don't iterate over as many
    supercell configurations so it's less able to find the best configuration in a give cell size.
    We try the PMG's cubic supercell transformation with a cap on the number of atoms (max_atoms).
    The min_length is decreased by 10% (geometrically) until a supercell can be constructed.

    Args:
        base_struct: structure of the unit cell
        max_atoms: Maximum number of atoms allowed in the supercell.
        min_atoms: Minimum number of atoms allowed in the supercell.
        min_length: Minimum length of the smallest supercell lattice vector.

    Returns:
        struc_sc: Supercell that is as close to cubic as possible
    """
    m_len = min_length
    sc_mat = None
    while sc_mat is None:
        sc_mat = _cubic_cell(base_struct, min_atoms, max_atoms, m_len)
        max_atoms += 1
    return sc_mat


def get_matched_structure_mapping(uc_struct: Structure, sc_struct: Structure, sm: StructureMatcher | None = None):
    """
    Get the mapping from the inserted structure onto the base structure,
    assuming that the inserted structure sans the working ion is some kind
    of SC of the base.

    Args:
        uc_struct: host structure, smaller cell
        sc_struct: bigger cell
        sm: StructureMatcher instance
    Returns:
        sc_m : supercell matrix to apply to s1 to get s2
        total-t : translation to apply on s1 * sc_m to get s2
    """
    if sm is None:
        sm = StructureMatcher(primitive_cell=False, comparator=ElementComparator())
    s1, s2 = sm._process_species([uc_struct, sc_struct])
    fu, _ = sm._get_supercell_size(s1, s2)
    try:
        val, dist, sc_m, total_t, mapping = sm._strict_match(s1, s2, fu=fu, s1_supercell=True)
    except TypeError:
        return None
    return sc_m, total_t


def _cubic_cell(
    base_struct: Structure,
    min_atoms: int = 80,
    max_atoms: int = 240,
    min_length: float = 10.0,
) -> np.ndarray | None:
    """Generate the best supercell from a unit cell using the pymatgen CubicSupercellTransformation.

    Args:
        base_struct: structure of the unit cell
        max_atoms: Maximum number of atoms allowed in the supercell.
        min_atoms: Minimum number of atoms allowed in the supercell.
        min_length: Minimum length of the smallest supercell lattice vector.

    Returns:
        3x3 matrix: supercell matrix
    """
    from pymatgen.transformations.advanced_transformations import (
        CubicSupercellTransformation,
    )

    cst = CubicSupercellTransformation(min_atoms=min_atoms, max_atoms=max_atoms, min_length=min_length)

    try:
        cst.apply_transformation(base_struct)
    except BaseException:
        return None
    return cst.transformation_matrix
