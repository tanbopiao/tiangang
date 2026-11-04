"""守护自愈引擎 —— 道统算子谱（tiangang）
道统出处：火斗讳·天罡，雨头火斗，斩邪破煞
工程映射：巡检-发现-处置-上报的守护循环
生长纪律：本地生长自由，推送远端需治理决议发令。
内核本体在 guard.py（TiangangGuard：探针巡检→交九枢→越阈上报），
本文件保留种子外壳 API（Guardian.describe/run），委托内核执行。
# 生长记录 2026-11-02：种子外壳接通 guard.py 内核，stage 升 m1。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from guard import TiangangGuard as _KernelGuard  # noqa: E402


class Guardian(_KernelGuard):
    """守护自愈引擎：外壳 API 委托 guard.py 内核，只增不覆盖。"""

    def describe(self) -> dict:
        return {"name": "tiangang", "role": "巡检-发现-处置-上报的守护循环", "stage": "m1"}

    def run(self, *args, **kwargs):
        """兼容种子 API：默认执行一巡（sweep）。"""
        return self.sweep()
