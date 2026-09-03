"""绘制等基准总算力集群的相交成本曲线，并输出可复算数据。"""
import argparse
import csv
import json
import math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, ticker

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--font", help="包含中文的字体文件路径")
args = parser.parse_args()
config = json.loads((ROOT / "docs/data/engineering-efficiency-assumptions.json").read_text())
font_paths = [args.font] if args.font else [
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]
for path in font_paths:
    if path and Path(path).is_file():
        font_manager.fontManager.addfont(path)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=path).get_name()
        break
else:
    raise SystemExit("需要中文字体；使用 --font /path/to/font.ttf 指定。")
plt.rcParams.update({
    "font.size": 14, "axes.unicode_minus": False, "svg.fonttype": "path",
    "svg.hashsalt": "tamomo-efficiency-cost",
    "axes.labelcolor": "#233342", "text.color": "#233342",
    "xtick.color": "#52616E", "ytick.color": "#52616E",
})
mac_wear_hourly = config["mac_extra_wear_usd_per_hour"]
mac_electricity_hourly = config["mac_extra_power_kw"] * config["electricity_usd_per_kwh"]
mac_unit_hourly = mac_wear_hourly + mac_electricity_hourly
gpu_count = config["central_cluster_gpu_count"]
macs_per_gpu = config["macs_per_b300_at_equal_reference_compute"]
mac_count = gpu_count * macs_per_gpu
mac_cluster_hourly = mac_count * mac_unit_hourly
central_cluster_hourly = gpu_count * config["central_usd_per_gpu_hour"]
hourly_cost_ratio = mac_cluster_hourly / central_cluster_hourly
central_index = config["central_task_cost_index"]
low, high = config["efficiency_ratio_min"], config["efficiency_ratio_max"]
ratios = [low + (high - low) * i / 900 for i in range(901)]
if low <= hourly_cost_ratio <= high:
    ratios = sorted(set(ratios + [hourly_cost_ratio]))

def mac_cost_index(efficiency_ratio):
    return central_index * hourly_cost_ratio / efficiency_ratio

assert math.isclose(mac_cost_index(hourly_cost_ratio), central_index, rel_tol=1e-12)
assert all(mac_cost_index(b) < mac_cost_index(a) for a, b in zip(ratios, ratios[1:]))
assert math.isclose(mac_count / macs_per_gpu, gpu_count)
data_dir = ROOT / "docs/data"
fig_dir = ROOT / "docs/figures"
fig_dir.mkdir(parents=True, exist_ok=True)
with (data_dir / "engineering-efficiency-cost.csv").open("w", newline="") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(["mac_to_b300_cluster_efficiency_ratio", "efficiency_ratio_percent",
                     "mac_task_cost_index", "b300_task_cost_index", "mac_to_b300_task_cost_ratio",
                     "mac_to_b300_task_running_time_ratio"])
    for ratio in ratios:
        writer.writerow([ratio, 100 * ratio, mac_cost_index(ratio), central_index,
                         hourly_cost_ratio / ratio, 1 / ratio])

green, blue, neutral = "#16816B", "#315EAD", "#233342"
grid = "#DCE3E8"
fig, ax = plt.subplots(figsize=(12.6, 9.2))
fig.patch.set_facecolor("white")
fig.subplots_adjust(left=0.115, right=0.955, top=0.76, bottom=0.325)
fig.text(0.115, 0.945, "等算力集群：工程效率比与训练成本", fontsize=24, weight="bold")
fig.text(0.115, 0.895, "固定两边基准总算力，用 B300 集群作为参照，比较完成同一任务的成本。", fontsize=14)
fig.text(0.115, 0.849,
         f"构成假设：{mac_count:g} 台 Mac ≈ {gpu_count:g} 张 B300 的基准总算力    |    情景分析，非实测", fontsize=13, color="#52616E")
ax.spines[["top", "right"]].set_visible(False)
ax.spines[["left", "bottom"]].set_color(grid)
ax.grid(axis="y", color=grid, linewidth=0.7)
ax.set_axisbelow(True)
ax.tick_params(length=0, pad=8)
if low < hourly_cost_ratio < high:
    ax.axvspan(low * 100, hourly_cost_ratio * 100, color=blue, alpha=0.045)
    ax.axvspan(hourly_cost_ratio * 100, high * 100, color=green, alpha=0.045)
    ax.text((low + hourly_cost_ratio) * 50, 560, "中心化 B300 成本更低", ha="center", fontsize=13)
    ax.text((high + hourly_cost_ratio) * 50, 560, "分布式 Mac 成本更低", ha="center", fontsize=13)
x = [ratio * 100 for ratio in ratios]
ax.plot(x, [mac_cost_index(ratio) for ratio in ratios], color=green, linewidth=3.2)
ax.axhline(central_index, color=blue, linewidth=2.8)
ax.set_xlim(low * 100, high * 100)
ax.set_ylim(40, 650)
ax.set_yscale("log")
ax.set_xticks([10, 20, 40, 60, 80, 100])
ax.set_yticks([50, 100, 200, 400, 600])
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
ax.yaxis.set_minor_locator(ticker.NullLocator())
ax.set_xlabel("Mac 集群有效效率 / B300 集群有效效率（%）", labelpad=14, fontsize=15)
ax.set_ylabel("同一任务的成本指数（B300 = 100；对数刻度）", labelpad=12, fontsize=14)
ax.text(82, central_index * 1.10, "B300 成本基准 = 100", ha="center", fontsize=13)
ax.annotate("分布式 Mac 成本", (24, mac_cost_index(0.24)), xytext=(34, 360),
            arrowprops={"arrowstyle": "-", "color": green}, fontsize=14)
if low <= hourly_cost_ratio <= high:
    cross_x = 100 * hourly_cost_ratio
    ax.vlines(cross_x, 40, central_index, color=neutral, linewidth=1.2, linestyle=(0, (4, 4)))
    ax.scatter([cross_x], [central_index], s=105, color=neutral, marker="D", zorder=5)
    ax.annotate(f"成本交点：{cross_x:.1f}%\n两边完成同一任务的成本相同", (cross_x, central_index),
                xytext=(61, 185), fontsize=14,
                arrowprops={"arrowstyle": "-", "color": neutral})
ax.scatter([100], [mac_cost_index(1)], s=58, color=green, zorder=5, clip_on=False)
ax.text(98, 45, f"效率相同：Mac 成本 {mac_cost_index(1):.1f}", ha="right", fontsize=12.5)
fig.text(0.115, 0.195,
         f"小时成本假设：Mac 集群 {mac_cluster_hourly:,.2f} 美元；B300 集群 {central_cluster_hourly:,.2f} 美元。比值为 {hourly_cost_ratio:.1%}。", fontsize=13)
fig.text(0.115, 0.147,
         f"Mac 单台：运行折旧 {mac_wear_hourly:g} + 新增电费 {mac_electricity_hourly:g} = {mac_unit_hourly:.4f} 美元/小时；不含购机款。", fontsize=12)
fig.text(0.115, 0.099,
         f"B300 单价参数：{config['central_usd_per_gpu_hour']} 美元/GPU 小时，来自 Runpod 单 GPU 实例报价（{config['as_of']}）。", fontsize=11.5, color="#52616E")
fig.text(0.115, 0.055,
         f"{macs_per_gpu:g} 台 Mac 对应 1 张 B300 基准算力为假设；效率比包含通信、等待、恢复和重算，未作实测。", fontsize=11.5, color="#52616E")
for extension in ("png", "svg"):
    output_path = fig_dir / f"engineering-efficiency-cost.{extension}"
    fig.savefig(output_path, dpi=190,
                facecolor="white", metadata={"Date": config["as_of"]})
    if extension == "svg":
        output_path.write_text("\n".join(line.rstrip() for line in output_path.read_text().splitlines()) + "\n")
plt.close(fig)
print(json.dumps({"mac_count": mac_count, "b300_count": gpu_count,
                  "mac_cluster_usd_per_hour": mac_cluster_hourly,
                  "b300_cluster_usd_per_hour": central_cluster_hourly,
                  "break_even_efficiency_ratio": hourly_cost_ratio,
                  "mac_cost_index_at_100_percent_efficiency_ratio": mac_cost_index(1)}, indent=2))
