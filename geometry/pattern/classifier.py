from typing import Type

import numpy as np

from geometry.pattern.asanoha import AsanohaPattern
from geometry.pattern.collision import CollisionPattern
from geometry.pattern.pattern import Pattern
from geometry.pattern.ryuso import RyusoPattern
from geometry.pattern.sakura import SakuraPattern
from geometry.pattern.shippo import ShippoPattern
from geometry.pattern.tsumi import TsumiPattern
from geometry.pattern.ume import UmePattern
from geometry.pattern.yotsuba import YotsubaPattern


class PatternClassifier:

    @staticmethod
    def classify_feature(feature) -> Type[Pattern]:
        entropy = feature["mean_entropy"]
        gray_std = feature["std_gray"]
        grad_mean = feature["mean_gradient"]
        lbp_hist = feature["lbp_hist"]

        # Texture uniformity: how dominant a single bin is
        lbp_dominance = np.max(lbp_hist)
        lbp_spread = np.count_nonzero(lbp_hist > 0.05)

        # Decide pattern
        if entropy < 3 and gray_std < 0.1 and grad_mean < 0.03:
            return AsanohaPattern  # smooth & flat (sky, wall)
        elif entropy > 4.2 and gray_std > 0.12:
            return RyusoPattern  # very detailed (grass, blanket)
        elif lbp_dominance > 0.4 and lbp_spread < 3:
            return RyusoPattern  # consistent, repetitive texture
        elif gray_std > 0.15 and grad_mean > 0.05:
            return SakuraPattern  # high contrast, likely decorative
        elif entropy < 2.5 and grad_mean < 0.02:
            return TsumiPattern  # smooth, gentle transitions
        else:
            return ShippoPattern  # moderately varied
