# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from __future__ import annotations

from typing import Any, Callable, Iterator, Optional, Sequence, Tuple

import json_any.json_any as jsnr
import networkx as grph

from cell_tracking_BC.standard.issue import ISSUE_SEPARATOR
from cell_tracking_BC.type.cell.cell import cell_t


TIME_POINT = "time_point"  # Leave it here (as opposed to making it a class variable) since it is used "everywhere"


class unstructured_track_t(grph.DiGraph):
    in_degree: Callable[[cell_t], int]
    out_degree: Callable[[cell_t], int]

    @classmethod
    def __NewFromJsonDescription__(
        cls,
        description: grph.DiGraph,
        /,
    ) -> unstructured_track_t:
        """"""
        return cls(description)

    def __DescriptionForJSON__(self) -> Any:
        """"""
        return grph.DiGraph(self)

    def Issues(self) -> Optional[Sequence[str]]:
        """"""
        output = []

        for cell in self.nodes:
            if (n_predecessors := self.in_degree(cell)) > 1:
                output.append(
                    f"Cell {self.nodes[cell][TIME_POINT]}.{cell.label}{ISSUE_SEPARATOR}{n_predecessors} predecessors. "
                    f"Expected=0 or 1."
                )

        if output.__len__() == 0:
            output = None

        return output

    def RootCellWithTimePoint(self) -> Tuple[cell_t, int]:
        """"""
        output = tuple(
            _rcd for _rcd in self.nodes.data(TIME_POINT) if self.in_degree(_rcd[0]) == 0
        )

        if (n_roots := output.__len__()) != 1:
            raise ValueError(
                f"{n_roots}{ISSUE_SEPARATOR}Invalid number of root cells. Expected=1."
            )

        return output[0]

    def LeafCellsWithTimePoints(self) -> Tuple[Sequence[cell_t], Sequence[int]]:
        """"""
        # TODO: Contact the Networkx team about the following comment (or check code on github)
        #     /!\ It seems that networkx.DiGraph.nodes.data does not guarantee the node enumeration order. This could be
        #     inconvenient for reproducibility checks.
        # The following sorting is undefined for 2 cells with the same centroid in the same frame, but this should not
        # happen in practice.
        records = sorted(
            (
                _rcd
                for _rcd in self.nodes.data(TIME_POINT)
                if self.out_degree(_rcd[0]) == 0
            ),
            key=lambda _rcd: str(_rcd[1]) + str(_rcd[0].centroid),
        )
        leaves, time_points = zip(*records)

        return tuple(leaves), tuple(time_points)

    @property
    def labels(self) -> Sequence[int]:
        """"""
        return (-1,)  # Note: this is a tuple

    @property
    def segments_iterator(self) -> Iterator[Tuple[int, cell_t, cell_t, bool]]:
        """"""
        time_points = grph.get_node_attributes(self, TIME_POINT)

        for edge in self.edges:
            time_point = time_points[edge[0]]
            is_last = self.out_degree(edge[1]) == 0
            yield time_point, *edge, is_last

    def __eq__(self, other: Any, /) -> bool:
        """"""
        return jsnr.JsonStringOf(self) == jsnr.JsonStringOf(other)
