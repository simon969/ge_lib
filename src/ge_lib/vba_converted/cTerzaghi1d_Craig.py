from dataclasses import dataclass
import math


@dataclass
class cTerzaghi1d_Craig:
    Cv: float = 0.0
    Mv: float = 0.0
    H: float = 0.0
    p1: float = 0.0
    Uc: float = 0.0
    timesteps: int = 0
    hsteps: int = 0
    _times: list[float] = None
    _degrees: list[float] = None

    def calc_Uc(self, dp1: float) -> float:
        self.Uc = self.Mv * self.H * dp1
        return self.Uc

    def sum_U(self, t: float, mcount: int = 100) -> float:
        Tv = self.Cv * t / self.H ** 2
        total = sum(math.exp(-(math.pi / 2 * (2 * m + 1)) ** 2 * Tv) * 2 / (math.pi / 2 * (2 * m + 1)) ** 2 for m in range(mcount + 1))
        return 1 - total

    def sum_dU(self, z: float, t: float, mcount: int = 100) -> float:
        Tv = self.Cv * t / self.H ** 2
        return sum(2 * self.p1 / (math.pi / 2 * (2 * m + 1)) * math.exp(-(math.pi / 2 * (2 * m + 1)) ** 2 * Tv) * math.sin(math.pi / 2 * (2 * m + 1) * z / self.H) for m in range(mcount + 1))

    def calc_dUProfileTime(self, time: float, hsteps: int, I: int = 0) -> list[list[float]]:
        self.hsteps = hsteps
        profile = [self.sum_dU(j * self.H / hsteps, time) for j in range(1, hsteps + 1)]
        return [[self.sum_U(time), *profile]]

    def calc_dUProfileAllTime(self, totaltime: float, timesteps: int, hsteps: int) -> None:
        self.timesteps = timesteps
        self.hsteps = hsteps
        self._times = [totaltime * i / timesteps for i in range(1, timesteps + 1)]
        self._degrees = [self.sum_U(t) for t in self._times]

    def get_timeTo(self, percUt: float) -> float:
        for time, degree in zip(self._times or [], self._degrees or []):
            if degree > percUt:
                return time
        return 0.0

    def get_t50(self) -> float:
        return self.get_timeTo(0.5)

    def get_t90(self) -> float:
        return self.get_timeTo(0.9)
