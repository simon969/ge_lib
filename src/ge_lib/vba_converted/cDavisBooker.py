from dataclasses import dataclass


@dataclass
class cDavisBooker:
    WithSurfaceLayer: int = 0
    So: float = 0.0
    M: float = 0.0
    B: float = 0.0
    mBSo: float = 0.0
    R: float = 0.0

    def calc_mBSo(self) -> float:
        self.mBSo = self.M * self.B / self.So
        return self.mBSo

    def calc_R(self) -> float:
        self.calc_mBSo()
        if self.WithSurfaceLayer == 1:
            return self.calc_R_WithSurfaceLayer()
        return self.calc_R_WithoutSurfaceLayer()

    def calc_R_WithSurfaceLayer(self) -> float:
        x = self.mBSo
        self.R = 0.0000001493276 * x ** 6 - 0.00001045768 * x ** 5 + 0.0002892158 * x ** 4 - 0.003978953 * x ** 3 + 0.02748431 * x ** 2 - 0.0681465 * x + 1.000241
        return self.R

    def calc_R_WithoutSurfaceLayer(self) -> float:
        x = self.mBSo
        self.R = -0.0000002412675 * x ** 6 + 0.00001720708 * x ** 5 - 0.0004881619 * x ** 4 + 0.007059503 * x ** 3 - 0.05631348 * x ** 2 + 0.2641849 * x + 1.003264
        return self.R
