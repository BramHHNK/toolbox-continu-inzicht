## Voeg later dynamische setuptools toe
# import pkg_resources  # part of setuptools
# __version__ = pkg_resources.get_distribution("toolbox_continu_inzicht").version
__version__ = "0.0.3"
# in alpha release zijn de versie gelijk aan de sprint nummers.

# Hier alleen base functies
# hier de hoofd modules, sub modules in de mapjes zelf
from toolbox_continu_inzicht import (
    base,
    fragility_curves,
    loads,
    proof_of_concept,
    sections,
)
from toolbox_continu_inzicht.base import config, data_adapter, fragility_curve
from toolbox_continu_inzicht.base.config import Config
from toolbox_continu_inzicht.base.data_adapter import DataAdapter
from toolbox_continu_inzicht.base.fragility_curve import FragilityCurve

__all__ = [
    "__version__",
    "config",
    "data_adapter",
    "Config",
    "DataAdapter",
    "fragility_curve",
    "FragilityCurve",
    "loads",
    "sections",
    "proof_of_concept",
    "base",
    "sections",
    "fragility_curves",
]
