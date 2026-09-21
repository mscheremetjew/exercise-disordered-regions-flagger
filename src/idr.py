"""Import bridge so the supplied acceptance tests can use ``src.idr``."""

from disordered_regions_flagger.idr import find_disordered_regions

__all__ = ["find_disordered_regions"]
