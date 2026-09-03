# Apple 与 NVIDIA 训练成本比较

核查日期：2026-09-03。金额统一使用美元，硬件采用美国公开价格，不折算成中国大陆采购价。价格、设备规格、假设计算与训练实测分别标明；本项目尚无跨平台训练实测。

## 结论

**TAMOMO 的主场景是利用已经拥有、原本闲置的 Mac。成本只计训练额外造成的运行折旧与电费，历史购置支出和原本就会发生的时间折旧不再分摊。与 NVIDIA 租用比较时，决定结果的是两边达到相同质量的实际成本。**

当前 NVIDIA 最新一代训练平台是 Vera Rubin。其规格已公开，合作伙伴已有实机验证报告，但本次未核实到公开按需小时报价。因此最新架构作技术对照，成本计算使用已有公开报价的 Blackwell Ultra B300，并加入 RTX PRO 6000 Blackwell 与 B200 作为参照。

若仅作情景假设：某台已有 Mac 每运行小时增加 **0.05 美元折旧**，相对原本闲置状态增加 **250 W** 功率，电价为 **0.15 美元 / kWh**，其成本为 **0.0875 美元 / 训练小时**。按下列报价，RTX PRO 6000 租用需超过 **23.89 倍**、B300 需超过 **90.17 倍**的同质量达标速度，租金才更低。折旧、功耗和速度均未实测；这个算例不对应尚未交付的新 M5 Ultra。

## 硬件和可用性

| 对象 | 内存 / 显存 | 内存带宽 | 应如何理解 |
| --- | --- | --- | --- |
| Mac Studio M5 Ultra | 入门 96 GB，最高 512 GB 统一内存 | 1.2 TB/s | 完整个人工作台；最高内存需要另选配置 |
| RTX PRO 6000 Blackwell Workstation Edition | 96 GB GDDR7 ECC | 1.792 TB/s | 单张工作站 GPU，主机另计 |
| Blackwell Ultra / B300 | 架构最高 288 GB HBM3e，实际容量依 SKU / 服务商 | 最高 8 TB/s | 数据中心训练 GPU；已有公开云租用报价 |
| Rubin GPU | 288 GB HBM4 | 最高 22 TB/s | 最新代数据中心 GPU；官方规格仍标注为初步信息 |

来源：[Apple 技术规格](https://www.apple.com/mac-studio/specs/) · [RTX PRO 6000 规格](https://www.nvidia.com/en-us/products/workstations/professional-desktop-gpus/rtx-pro-6000/) · [Blackwell Ultra 架构](https://developer.nvidia.com/blog/inside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era/) · [Rubin 规格](https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/)。统一内存与 GPU 专用显存的可用容量和占用方式不同，不能按标称容量直接等同。

Rubin 官方给出的单 GPU 稠密 BF16/FP16 峰值为 4 PFLOPS，NVLink 带宽为 3.6 TB/s；NVFP4 训练的 35 PFLOPS 是另一种精度口径。Apple 目前核查到的资料没有可直接配对的持续 BF16 训练吞吐，不能用其 AI 宣传倍数或上一份文档的假设 TFLOP/s 计算跨平台性价比。

[NVIDIA 对 CoreWeave 的报告](https://blogs.nvidia.com/blog/vera-rubin/)描述了 Rubin 实机的 DeepSeek-R1 推理验证。该结果不能转换成 TAMOMO 的从零训练收益。[DGX B300 官方页面](https://www.nvidia.com/en-us/data-center/dgx-b300/)则明确标注系统正在出货。新 M5 Ultra Mac Studio 计划 9 月 22 日开始交付，512 GB 配置预计 10 月下旬交付。

## 可以核查的价格

### 购置

- **Mac Studio M5 Ultra：5,499 美元起，整机。** 对应 30 核 CPU、64 核 GPU、96 GB 内存和 1 TB SSD；不是 256 GB 或 512 GB 的报价。[美国发布稿](https://www.apple.com/newsroom/2026/08/apple-introduces-new-mac-studio-with-m5-max-and-m5-ultra/) · [配置规格](https://www.apple.com/mac-studio/specs/)
- **RTX PRO 6000 Workstation Edition：本次官方 Marketplace 页面列价 16,000 美元，显示缺货。** 这是单卡价目观察，不是可成交的整机报价；还需要主机、内存、存储、电源和散热。本文不据此宣称 NVIDIA 工作站的最低购置成本。[官方商店页面](https://marketplace.nvidia.com/en-us/enterprise/laptops-workstations/nvidia-rtx-pro-6000-blackwell-workstation-edition/)
- **B300 / Rubin 完整训练系统：本次没有核实到可用于采购的统一公开整机报价。** 它们涉及服务器、互联和部署配置，保留为待报价项，不使用传闻中的单芯片或整柜价格填补。

### 租用

以下为核查时 [Runpod Pods 定价页](https://www.runpod.io/pricing)显示的单 GPU 实例小时价。B300 的 [型号页](https://www.runpod.io/gpu-models/b300)同时列明 Secure Cloud 为 7.89 美元 / 小时；更低价的其他服务档位不混入此表。

| GPU 实例 | 页面标注显存 | 页面所列配套 CPU / RAM | 展示价 / 小时 | 1,000 GPU 小时租金 |
| --- | --- | --- | ---: | ---: |
| RTX PRO 6000 | 96 GB | 16 vCPU / 188 GB RAM | $2.09 | $2,090 |
| B200 | 180 GB | 28 vCPU / 283 GB RAM | $6.79 | $6,790 |
| B300 | 288 GB | 32 vCPU / 251 GB RAM | $7.89 | $7,890 |
| Rubin | 未核实相同按需口径报价 | — | 待报价 | — |

这些是运行时租金，不是完整训练项目总价；存储、适用税费及其他实际收费需另计。云服务价格已经承担该服务的设备和供电成本，不再额外叠加一个自估 GPU 电费。公开目录不等于某地区即时有货。租用的 RTX PRO 6000 具体版型、功率配置与互联还需在选实例时确认，不能默认等同于桌面 Workstation Edition。

报价交叉检查发现不同日期和档位的数字并不相同。本文采用当前定价页；不混用较早指南中的 B300 7.39 美元报价。[Lambda 定价页](https://lambda.ai/pricing)的 B200 单 GPU 实例为 6.99 美元 / GPU 小时，8 GPU 实例所列 6.69 美元是每 GPU 价格，不是整机价。[CoreWeave 定价页](https://www.coreweave.com/pricing)对 B300 的按需价格要求询价，部分机型规格列为每卡 270 GB，说明必须核对服务商实际可用配置；本次在该页未找到 Rubin 公共价格。

## 相同训练任务的成本分界点

等基准总算力集群的相交成本曲线见[工程效率比与训练成本](./engineering-efficiency-cost.md)。横轴统一为 Mac 集群有效效率占 B300 集群的比例，并把组成等算力集群所需的全部设备计入成本。

### 明确假设

以下模型比较“一台已有闲置 Mac 的新增运行成本”与“按需租用一台 GPU 实例的租金”，用于设计实验，不代表设备实测结果：

- 原设备已经拥有，训练使用原本不会产生其他收益、也不会被日常工作占用的闲置时段。历史购置支出和日历时间带来的自然贬值不计入。
- **运行折旧 `d`** 仅指训练额外造成的损耗或剩余寿命、剩余价值减少，按实际运行小时估算。它不能用“购机价 / 三年 / 训练占用率”替代。暂缺可靠测量，因此下表的 `d` 全部是敏感性参数。
- **新增平均功率 `ΔP`** 暂设为 **250 W**，电价 `e` 暂设为 **0.15 美元 / kWh**。新增功率是训练整机功率减去同等时段原本闲置状态的功率；若原本会休眠或关机，应使用该基线。
- 两边必须能够运行同一模型、数据和质量目标；运行时间与电量包含通信等待、恢复、失败尝试及重算。
- 主模型只包含运行折旧与新增电费。已有网络、设备的固定支出和未被使用的闲置时间不另行分摊。云端按实际租金比较，电费已包含其中。

```text
单台 Mac 每运行小时成本 c = d + (ΔP / 1000) × e
单项任务成本 = Σ各设备 [额外运行折旧 + (训练电量 - 原闲置基线电量) × 电价]
速度倍数 S = Mac 达标时间 / NVIDIA 达标时间
单台 Mac 与单 GPU 实例比较：NVIDIA 租金更低的条件为 S > NVIDIA 小时租价 / c
```

| 假设运行折旧 / 小时 | Mac 运行折旧 + 新增电费 / 小时 | RTX PRO 6000 需要超过的速度倍数 | B200 需要超过的速度倍数 | B300 需要超过的速度倍数 |
| ---: | ---: | ---: | ---: | ---: |
| $0.02 | $0.0575 | 36.35× | 118.09× | 137.22× |
| $0.05 | $0.0875 | 23.89× | 77.60× | 90.17× |
| $0.10 | $0.1375 | 15.20× | 49.38× | 57.38× |

三行的新增电费均为 **0.0375 美元 / 小时**。0.02–0.10 美元的折旧区间只是展示判断如何随参数变化，没有证据表明真实折旧一定落在其中。尚未取得折旧依据前，应保留参数，不把中间一行当成实测成本。

这里比较的是设备拥有者选择“利用闲置设备”或“付费租用”的支出，不是 NVIDIA 云运营商的边际成本。若比较双方已经拥有的闲置硬件，两边都应采用运行折旧加新增电费。

多机训练必须累加每台 Mac 的实际成本。例如 100 台同成本 Mac 同时运行一小时，成本是单台的一百倍；不能把网络的总吞吐与单台的小时成本配对。闲置比例仍会影响日历工期，但不再作为购机摊销分母。

### 一项 Mac 需要 100 小时的任务

假设任务能在某台已有 Mac 内运行，实际运行 100 小时，并采用中间一行的折旧与新增功率假设，则 Mac 的运行折旧为 **5.00 美元**、新增电费为 **3.75 美元**，合计 **8.75 美元**。

| 假设 B300 相对 Mac 的实际达标速度 | B300 时间 | B300 租金 | 相对上述 Mac 新增运行成本 |
| ---: | ---: | ---: | --- |
| 20× | 5 小时 | $39.45 | 更高 |
| 50× | 2 小时 | $15.78 | 更高 |
| 100× | 1 小时 | $7.89 | 更低 |

100 小时和这些速度倍数是算例，不是训练结果。电费对应新增现金支出，运行折旧是额外损耗的经济估算；两者都需要给出依据。

前文的 **10B 模型约 160 GB 固定训练状态**无法放入 96 GB Mac。比较该任务必须选择内存足够的已有设备或有效的分片方案，并重新测量相应运行成本；同时检查 GPU 方案的激活、优化器和临时空间。多卡显存需要通过并行或分片方案才能使用，其等待和额外电量应进入记录。

## NVIDIA 不同代际之间也要比较达标速度

按同一报价表，B300 的小时价是 B200 的 **1.162 倍**。对于两者都能运行的任务，B300 只要以超过 1.162 倍的达标速度运行，对应计算租金就更低；如果它主要增加了未用到的内存，成本可能更高。

B300 的小时价是 RTX PRO 6000 的 **3.775 倍**。这给出了另一个可直接实验验证的分界点。若任务原本无法放进 96 GB，则需比较完整的多卡或卸载方案，不能按单卡小时价得出结论。

Rubin 在取得有效报价后可以使用同一方法。其更高带宽、训练算力和 NVLink 能力支持开展比较，但尚不能确定单位达标成本。不同精度、稀疏率和推理宣传数据不用于推算训练倍数。

## 功耗规格与新增电量

NVIDIA 官方列出 RTX PRO 6000 Workstation Edition 的板卡功率上限为 600 W；8 GPU 的 DGX B300 系统约 14 kW。两者覆盖的系统范围不同，也不是 TAMOMO 任务的平均功耗。前者还要加上主机耗电，后者的自建成本还要考虑配电、散热、网络与机房。[RTX 规格](https://www.nvidia.com/en-us/products/workstations/professional-desktop-gpus/rtx-pro-6000/) · [DGX B300 规格](https://www.nvidia.com/en-us/data-center/dgx-b300/)

已有闲置设备应同时测量训练整机电量与同等时段原闲置基线电量，差额才是新增电量。若完整 NVIDIA 方案的新增平均功率是完整 Mac 方案的 `k` 倍，在相同电价下，只有当达标速度超过 `k` 倍时，其新增电费才更低。不能拿板卡功率上限与 Mac 的假设平均功耗直接相除。

## 对 TAMOMO 的价值判断

TAMOMO 以第一种情形作为主成本模型，其他决策单独比较：

- **已经拥有且可闲时使用的 Mac**：以运行额外折旧与新增电费为成本，检验能否把闲置能力转化为低成本的有效训练；累加全部参与设备的实际消耗。
- **为训练专门购置 Mac**：必须面对 NVIDIA 按需租用及完整工作站方案的成本竞争，不能只凭大内存或低额定功率宣称便宜。
- **持续的大规模预训练**：应把 B300 等实际可用的集中式 GPU 方案作为成本和时间对照；Rubin 待报价与相同任务测试后纳入。

已有闲置设备使 TAMOMO 有机会用较低的新增支出组织训练。要进一步证明任务成本优势，需要展示在明确工作负载、设备来源、运行折旧假设与电量测量下，达到同等质量的成本优于可获得的租用方案。注册设备数或廉价的单机运行小时不能独立证明这一点。

下一项最小成本实验可以选两边均能运行的小模型，从同一初始化、数据和质量标准出发，记录端到端达标时间、实际云账单、Mac 训练与原闲置状态的插座电量、恢复开销与配置。以测得的新增电量和明确的折旧区间重算成本分界点，再判断实际速度是否跨过分界。本文不增加采购、租用或云资源。

若以后专门购置训练设备，应独立评估购置价、残值、使用期及预计训练量；上文的产品起售价仅为这类决策提供参考，不进入已有闲置 Mac 的主成本公式。

### 算术复核

```sh
python3 - <<'PY'
rates = {"RTX PRO 6000": 2.09, "B200": 6.79, "B300": 7.89}
delta_power_kw, electricity_rate = 0.250, 0.15
for wear_hourly in (0.02, 0.05, 0.10):
    mac_hourly = wear_hourly + delta_power_kw * electricity_rate
    print("wear USD/hour", wear_hourly, "Mac USD/hour", round(mac_hourly, 6))
    print({gpu: round(rate / mac_hourly, 4) for gpu, rate in rates.items()})
print("Mac 100 hours: wear USD", 100 * 0.05,
      "electricity USD", 100 * delta_power_kw * electricity_rate,
      "total USD", 100 * (0.05 + delta_power_kw * electricity_rate))
for speedup in (20, 50, 100):
    hours = 100 / speedup
    print("B300 speedup", speedup, "hours", hours, "USD", round(hours * rates["B300"], 2))
print("B300/B200 hourly-price ratio", rates["B300"] / rates["B200"])
print("B300/RTX PRO hourly-price ratio", rates["B300"] / rates["RTX PRO 6000"])
PY
```
