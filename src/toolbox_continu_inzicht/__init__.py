## Voeg later dynamische setuptools toe
# import pkg_resources  # part of setuptools
# __version__ = pkg_resources.get_distribution("toolbox_continu_inzicht").version
__version__ = "0.0.3"
# in alpha release zijn de versie gelijk aan de sprint nummers.

# Hier alleen base functies
from base import config, data_adapter, fragility_curve
from base.config import Config
from base.data_adapter import DataAdapter
from base.fragility_curve import FragilityCurve

# hier de hoofd modules, sub modules in de mapjes zelf
from toolbox_continu_inzicht import (
    base,
    loads,
    sections,
    fragility_curves,
    proof_of_concept,
)


__all__ = [
    "__version__",
    "config",
    "data_adapter",
    "fragility_curve",
    "Config",
    "DataAdapter",
    "FragilityCurve",
    "base",
    "loads",
    "sections",
    "fragility_curves",
    "proof_of_concept",
]
