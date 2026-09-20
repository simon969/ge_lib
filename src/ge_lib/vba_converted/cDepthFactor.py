from dataclasses import dataclass, field


@dataclass
class cDepthFactor:
    values: list[list[float]] = field(default_factory=lambda: [
        [0.93, 0.91, 0.895, 0.875, 0.86, 0.85, 0.75, 0.69, 0.65, 0.625, 0.558],
        [0.87, 0.85, 0.83, 0.81, 0.795, 0.78, 0.675, 0.62, 0.585, 0.565, 0.51],
        [0.86, 0.822, 0.79, 0.765, 0.745, 0.725, 0.625, 0.59, 0.57, 0.555, 0.525],
        [0.775, 0.74, 0.715, 0.69, 0.67, 0.65, 0.565, 0.53, 0.515, 0.5, 0.5],
    ])

    def get_x(self, depth_ratio: float, offset: int) -> float:
        index = min(max(int(depth_ratio), 1), 11) - 1
        return self.values[offset - 1][index]

    @staticmethod
    def getXOffset(length_ratio: float, poisson: float) -> int:
        if length_ratio == 5 and poisson == 0.5:
            return 1
        if length_ratio == 5 and poisson == 0.3:
            return 2
        if length_ratio == 1 and poisson == 0.5:
            return 3
        if length_ratio == 1 and poisson == 0.3:
            return 4
        return 0

    def get_DepthFactor(self, LoverB: float, Poisson: float, DoverB: float) -> float:
        poisson = min(max(Poisson, 0.3), 0.5)
        length_ratio = min(max(LoverB, 1.0), 5.0)
        offset = self.getXOffset(length_ratio, poisson)
        if offset:
            return self.get_x(DoverB, offset)

        lb1p3 = self.get_x(DoverB, 4)
        lb5p3 = self.get_x(DoverB, 2)
        lb1p5 = self.get_x(DoverB, 3)
        lb5p5 = self.get_x(DoverB, 1)
        length_factor = (length_ratio - 1) / 4
        poisson_factor = (poisson - 0.3) / 0.2
        value_p3 = (lb5p3 - lb1p3) * length_factor + lb1p3
        value_p5 = (lb5p5 - lb1p5) * length_factor + lb1p5
        return (value_p5 - value_p3) * poisson_factor + value_p3
