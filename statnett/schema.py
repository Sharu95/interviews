from dataclasses import dataclass
from typing import Optional

@dataclass
class MeasurementRecord:
    Minutes1UTC: str
    Minutes1DK: str
    CO2Emission: float
    ProductionGe100MW: float
    ProductionLt100MW: float
    SolarPower: float
    OffshoreWindPower: float
    OnshoreWindPower: float
    Exchange_Sum: float
    Exchange_DK1_DE: float
    Exchange_DK1_NL: float
    Exchange_DK1_GB: float
    Exchange_DK1_NO: float
    Exchange_DK1_SE: float
    Exchange_DK1_DK2: float
    Exchange_DK2_DE: float
    Exchange_DK2_SE: float
    Exchange_Bornholm_SE: float
    aFRR_ActivatedDK1: float
    aFRR_ActivatedDK2: float
    mFRR_ActivatedDK1: Optional[float]
    mFRR_ActivatedDK2: Optional[float]
    ImbalanceDK1: Optional[float]
    ImbalanceDK2: Optional[float]