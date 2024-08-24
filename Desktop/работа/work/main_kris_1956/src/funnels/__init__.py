from .base import BaseFunnelConfig
from .funnel import EnergyFunnel
from .finance import FinanceFunnel
from .general import GeneralFunnel
from .health import HealthFunnel
from .relationship import RelationshipFunnel


# noinspection PyTypeChecker
funnels = [EnergyFunnel(), FinanceFunnel(), GeneralFunnel(), HealthFunnel(), RelationshipFunnel()]

funnels: dict[str, BaseFunnelConfig] = {funnel.title: funnel for funnel in funnels}
