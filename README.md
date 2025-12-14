# IceCube IC86 有效面积计算器 / Effective Area Calculator

## 中文说明

### 概述
这个仓库提供了IceCube IC86探测器的平均有效面积随中微子能量的变化数据，用于计算中微子探测率。

IceCube IC86是IceCube中微子探测器的标准配置，包含86条探测器串。有效面积是计算中微子探测率的关键参数。

### 功能特性
- 提供100 GeV到100 PeV能量范围内的有效面积数据
- 支持单个能量点或能量数组的查询
- 内置探测率计算功能
- 可导出数据为CSV格式
- 可生成有效面积随能量变化的图表

### 快速开始

#### 安装依赖
```bash
pip install numpy matplotlib
```

#### 基本使用
```python
from icecube_ic86_effective_area import IceCubeIC86EffectiveArea

# 创建计算器实例
ic86 = IceCubeIC86EffectiveArea()

# 获取特定能量的有效面积
energy = 1e5  # 100 TeV (单位: GeV)
effective_area = ic86.get_effective_area(energy)
print(f"在 {energy/1e3:.0f} TeV 处的有效面积: {effective_area:.2f} m²")

# 计算探测率
flux = 1e-18  # 中微子通量 (GeV^-1 cm^-2 s^-1 sr^-1)
rate = ic86.calculate_detection_rate(energy, flux)
print(f"探测率: {rate:.2e} events/s/sr")
```

#### 运行示例
```bash
python icecube_ic86_effective_area.py
```

这将会：
1. 显示多个能量点的有效面积
2. 演示探测率计算
3. 导出数据到CSV文件
4. 生成有效面积图表

### 数据说明

有效面积数据基于IceCube IC86配置对缪子中微子(νμ)的典型性能：

| 能量 | 有效面积 |
|------|----------|
| 100 GeV | ~0.001 m² |
| 1 TeV | ~0.1 m² |
| 10 TeV | ~2 m² |
| 100 TeV | ~20 m² |
| 1 PeV | ~45 m² |
| 10 PeV | ~52 m² |
| 100 PeV | ~53.5 m² |

### 应用示例

#### 计算天体物理中微子的探测率
```python
import numpy as np
from icecube_ic86_effective_area import IceCubeIC86EffectiveArea

ic86 = IceCubeIC86EffectiveArea()

# 能量范围
energies = np.logspace(3, 7, 100)  # 1 TeV 到 10 PeV

# 假设一个E^-2.5的能谱
flux_norm = 1e-18  # GeV^-1 cm^-2 s^-1 sr^-1 在 100 TeV
E_norm = 1e5  # GeV
flux = flux_norm * (energies / E_norm)**(-2.5)

# 计算探测率
rates = ic86.calculate_detection_rate(energies, flux)

# 总探测率（积分）
total_rate = np.trapz(rates, energies)
print(f"总探测率: {total_rate:.2e} events/s/sr")
```

### 注意事项
1. 数据为近似值，基于IceCube公开发表的典型性能数据
2. 有效面积对缪子中微子最准确，其他味道的中微子可能有所不同
3. 实际有效面积会受到探测器配置、数据处理方法等因素影响
4. 用于精确科学分析时，建议使用IceCube官方发布的详细数据

---

## English Documentation

### Overview
This repository provides the average effective area of the IceCube IC86 detector as a function of neutrino energy, for calculating neutrino detection rates.

IceCube IC86 is the standard configuration of the IceCube Neutrino Observatory, consisting of 86 detector strings. The effective area is a key parameter for calculating neutrino detection rates.

### Features
- Provides effective area data for energy range from 100 GeV to 100 PeV
- Supports queries for single energy points or energy arrays
- Built-in detection rate calculation
- Export data to CSV format
- Generate plots of effective area vs energy

### Quick Start

#### Install Dependencies
```bash
pip install numpy matplotlib
```

#### Basic Usage
```python
from icecube_ic86_effective_area import IceCubeIC86EffectiveArea

# Create calculator instance
ic86 = IceCubeIC86EffectiveArea()

# Get effective area at specific energy
energy = 1e5  # 100 TeV (in GeV)
effective_area = ic86.get_effective_area(energy)
print(f"Effective area at {energy/1e3:.0f} TeV: {effective_area:.2f} m²")

# Calculate detection rate
flux = 1e-18  # Neutrino flux (GeV^-1 cm^-2 s^-1 sr^-1)
rate = ic86.calculate_detection_rate(energy, flux)
print(f"Detection rate: {rate:.2e} events/s/sr")
```

#### Run Example
```bash
python icecube_ic86_effective_area.py
```

This will:
1. Display effective areas at multiple energy points
2. Demonstrate detection rate calculation
3. Export data to CSV file
4. Generate effective area plot

### Data Description

Effective area data is based on typical IceCube IC86 performance for muon neutrinos (νμ):

| Energy | Effective Area |
|--------|----------------|
| 100 GeV | ~0.001 m² |
| 1 TeV | ~0.1 m² |
| 10 TeV | ~2 m² |
| 100 TeV | ~20 m² |
| 1 PeV | ~45 m² |
| 10 PeV | ~52 m² |
| 100 PeV | ~53.5 m² |

### Application Example

#### Calculate Astrophysical Neutrino Detection Rate
```python
import numpy as np
from icecube_ic86_effective_area import IceCubeIC86EffectiveArea

ic86 = IceCubeIC86EffectiveArea()

# Energy range
energies = np.logspace(3, 7, 100)  # 1 TeV to 10 PeV

# Assume E^-2.5 spectrum
flux_norm = 1e-18  # GeV^-1 cm^-2 s^-1 sr^-1 at 100 TeV
E_norm = 1e5  # GeV
flux = flux_norm * (energies / E_norm)**(-2.5)

# Calculate detection rates
rates = ic86.calculate_detection_rate(energies, flux)

# Total rate (integrated)
total_rate = np.trapz(rates, energies)
print(f"Total detection rate: {total_rate:.2e} events/s/sr")
```

### Important Notes
1. Data are approximate values based on publicly available IceCube performance data
2. Effective area is most accurate for muon neutrinos; other flavors may differ
3. Actual effective area depends on detector configuration, data processing methods, etc.
4. For precise scientific analysis, use official IceCube detailed data releases

### References
- IceCube Collaboration official website: https://icecube.wisc.edu/
- IceCube publications on effective area and detector performance

---

## License
This code is provided for educational and research purposes.
