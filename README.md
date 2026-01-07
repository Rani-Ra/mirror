# AGN-GRB Distribution Analysis

中微子背景的AGN中GRB分布分析框架 / Framework for analyzing GRB distribution in AGN and their contribution to neutrino background

## 概述 / Overview

本项目提供了一套工具来计算活动星系核(AGN)中伽马射线暴(GRB)的分布，以及它们对中微子背景的贡献。

This project provides tools to calculate the distribution of Gamma-Ray Bursts (GRBs) in Active Galactic Nuclei (AGN) and their contribution to the neutrino background.

## 主要功能 / Main Features

### 1. AGN质量函数 / AGN Mass Function
- 基于Shankar et al. (2009)的超大质量黑洞质量函数
- 考虑红移演化
- Schechter函数形式的双幂律分布

Based on Shankar et al. (2009) supermassive black hole mass function with redshift evolution, using double power-law Schechter function.

### 2. AGN红移演化 / AGN Redshift Evolution
- 宇宙学计算（共动距离、共动体积）
- AGN数密度随红移的演化
- 支持自定义宇宙学参数(H0, Ωm, ΩΛ)

Cosmological calculations (comoving distance, volume) and AGN number density evolution with redshift. Supports custom cosmological parameters.

### 3. AGN中的GRB分布 / GRB Distribution in AGN
- GRB发生率与黑洞质量的关系
- GRB在AGN盘中的径向分布
- 可调节的模型参数

GRB occurrence rate as a function of black hole mass and radial distribution within AGN disk with adjustable model parameters.

### 4. 组合分布 / Combined Distribution
- 集成AGN-GRB种群模型
- 计算总GRB率密度
- 累积GRB率计算

Integrated AGN-GRB population model with total GRB rate density and cumulative rate calculations.

### 5. 中微子背景计算 / Neutrino Background Calculation
- 可扩展的中微子发射模型
- 支持用户自定义中微子光度函数
- 框架适用于TQM和SG模型

Extensible neutrino emission model supporting user-defined luminosity functions, applicable to TQM and SG models.

## 安装 / Installation

```bash
# 克隆仓库 / Clone repository
git clone https://github.com/Rani-Ra/mirror.git
cd mirror

# 安装依赖 / Install dependencies
pip install numpy scipy matplotlib
```

## 使用方法 / Usage

### 基本示例 / Basic Example

```python
from agn_grb_distribution import AGNGRBPopulation

# 创建种群模型 / Create population model
pop = AGNGRBPopulation()

# 计算特定红移下的GRB率密度 / Calculate GRB rate density at specific redshift
z = 1.0
M_bh = 1e8  # Solar masses
rate_density = pop.grb_rate_density(M_bh, z)
print(f"GRB rate density: {rate_density:.2e} Mpc^-3 yr^-1")

# 计算总GRB率 / Calculate total GRB rate
total_rate = pop.total_grb_rate_at_z(z)
print(f"Total GRB rate at z={z}: {total_rate:.2e} Mpc^-3 yr^-1")

# 累积GRB率 / Cumulative GRB rate
z_max = 3.0
cumulative_rate = pop.cumulative_grb_rate(z_max)
print(f"Cumulative rate (z < {z_max}): {cumulative_rate:.2e} yr^-1")
```

### 运行完整示例 / Run Complete Example

```bash
# 运行基本分析 / Run basic analysis
python agn_grb_distribution.py

# 生成可视化图表 / Generate visualization plots
python plot_agn_grb_distributions.py
```

### 中微子发射模型 / Neutrino Emission Model

```python
from agn_grb_distribution import NeutrinoBackgroundCalculator

# 创建计算器 / Create calculator
calc = NeutrinoBackgroundCalculator()

# 定义中微子光度函数（示例）/ Define neutrino luminosity function (example)
def my_neutrino_model(M_bh, a, z):
    """
    计算中微子光度 / Calculate neutrino luminosity
    
    Parameters:
    - M_bh: 黑洞质量 (M_sun) / Black hole mass
    - a: 半长轴 (r_g) / Semi-major axis (gravitational radii)
    - z: 红移 / Redshift
    
    Returns:
    - L_nu: 中微子光度 (erg/s) / Neutrino luminosity
    """
    # 在这里实现您的TQM或SG模型 / Implement your TQM or SG model here
    L_nu = 1e45 * (M_bh / 1e8)**0.5 * (a / 1e3)**(-1.0)
    return L_nu

# 设置模型 / Set model
calc.set_neutrino_emission_model(my_neutrino_model)

# 计算中微子流量贡献 / Calculate neutrino flux contribution
E_nu = 1e5  # GeV
flux = calc.neutrino_flux_contribution(E_nu, z_max=3.0)
```

## 模型参数 / Model Parameters

### AGN质量函数参数 / AGN Mass Function Parameters
- `phi_star`: 归一化常数 / Normalization (1e-5 Mpc^-3 dex^-1)
- `M_star`: 特征质量 / Characteristic mass (1e8 M_sun)
- `alpha`: 暗端斜率 / Faint-end slope (-0.5)
- `beta`: 亮端斜率 / Bright-end slope (-2.5)

### GRB分布参数 / GRB Distribution Parameters
- `R_GRB_norm`: GRB率归一化 / GRB rate normalization (1e-3 per AGN per year)
- `mass_index`: 质量依赖指数 / Mass dependence index (0.5)
- `a_min`, `a_max`: 盘半长轴范围 / Disk semi-major axis range (100-10000 r_g)

### 宇宙学参数 / Cosmological Parameters
- `H0`: 哈勃常数 / Hubble constant (70 km/s/Mpc)
- `Om0`: 物质密度参数 / Matter density (0.3)
- `OL0`: 暗能量密度参数 / Dark energy density (0.7)

## 输出图表 / Output Plots

运行 `plot_agn_grb_distributions.py` 将生成以下图表：

1. `agn_mass_function.png` - AGN质量函数随红移的演化
2. `redshift_evolution.png` - AGN和GRB种群的红移演化
3. `grb_radial_distribution.png` - GRB在AGN盘中的径向分布
4. `grb_rate_vs_mass.png` - GRB率与黑洞质量的关系
5. `combined_rate_density_2d.png` - 二维GRB率密度图
6. `cumulative_grb_rate.png` - 累积GRB率

## 物理模型说明 / Physical Model Description

### AGN-GRB连接 / AGN-GRB Connection

本模型基于以下物理图景：
- GRB喷流在AGN盘中传播
- 喷流与盘物质相互作用产生中微子
- GRB发生率依赖于AGN性质（黑洞质量、吸积率）
- 空间分布遵循AGN盘的径向结构

Based on the physical picture where:
- GRB jets propagate through AGN disk
- Jet-disk interaction produces neutrinos
- GRB rate depends on AGN properties
- Spatial distribution follows AGN disk radial structure

### 观测约束 / Observational Constraints

模型参数选择考虑了：
- AGN光度函数和质量函数的观测数据
- GRB率的观测约束
- 中微子探测的实验数据

Model parameters are chosen considering:
- AGN luminosity and mass function observations
- GRB rate observational constraints
- Neutrino detection experimental data

## 扩展建议 / Extension Suggestions

1. **精细化模型** / Refine Models
   - 考虑AGN吸积率的影响
   - 包含GRB光度函数
   - 添加尘埃吸收效应

2. **中微子物理** / Neutrino Physics
   - 实现详细的中微子产生机制
   - 考虑振荡效应
   - 包含不同能量段

3. **统计分析** / Statistical Analysis
   - 蒙特卡洛采样
   - 参数不确定性分析
   - 与IceCube数据比较

## 参考文献 / References

1. Hopkins et al. (2007) - AGN luminosity function
2. Shankar et al. (2009) - SMBH mass function
3. Perna et al. (2021) - GRB-AGN connection
4. 根据您的具体研究添加相关文献 / Add relevant papers from your research

## 作者 / Author

项目用于研究AGN中GRB产生的中微子辐射及其对中微子背景的贡献。

Project for studying neutrino radiation from GRBs in AGN and their contribution to the neutrino background.

## 许可证 / License

MIT License

## 联系方式 / Contact

如有问题或建议，请通过GitHub Issues联系。

For questions or suggestions, please contact via GitHub Issues.
