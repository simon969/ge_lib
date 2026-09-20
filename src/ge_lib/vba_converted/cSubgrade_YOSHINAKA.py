from dataclasses import dataclass
import math

@dataclass
class cSubgrade_YOSHINAKA:
    mB: float = 0.0
    mBh: float = 0.0
    mAh: float = 0.0
    malphak: float = 0.0
    mbeta: float = 0.0
    mEI: float = 0.0
    mEs: float = 0.0
    mEo: float = 0.0
    mE30: float = 0.0
    mIp: float = 0.0
    mPoisson: float = 0.0
    mEf: float = 0.0
    mkh: float = 0.0
    mk30: float = 0.0
mkh = mE30 / (2.34 * (1 - mPoisson ^ 2) * mIp * mB ^ (3 / 4))
