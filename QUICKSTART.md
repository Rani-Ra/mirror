# 快速开始指南 / Quick Start Guide

## 简介 / Introduction

这个框架帮助您研究AGN中GRB的分布以及它们对中微子背景的贡献。
This framework helps you study the distribution of GRBs in AGN and their contribution to the neutrino background.

## 5分钟入门 / 5-Minute Quickstart

### 1. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 运行基本示例 / Run Basic Example

```bash
# 查看AGN-GRB分布的基本计算
# View basic AGN-GRB distribution calculations
python agn_grb_distribution.py
```

输出示例 / Example output:
```
AGN Mass Function
z = 0.0: Total AGN density = 1.78e-04 Mpc^-3
z = 1.0: Total AGN density = 3.70e-04 Mpc^-3

GRB Rate vs Black Hole Mass
M_BH = 1.0e+08 M_sun: R_GRB = 1.00e-03 yr^-1

Total GRB rate (z < 3.0): 1.30e+05 yr^-1
```

### 3. 生成可视化图表 / Generate Visualizations

```bash
# 生成6种不同类型的图表
# Generate 6 different types of plots
python plot_agn_grb_distributions.py
```

生成的图表 / Generated plots:
- `agn_mass_function.png` - AGN质量函数
- `redshift_evolution.png` - 红移演化
- `grb_radial_distribution.png` - 径向分布
- `grb_rate_vs_mass.png` - GRB率vs质量
- `combined_rate_density_2d.png` - 2D率密度图
- `cumulative_grb_rate.png` - 累积GRB率

### 4. 参数研究 / Parameter Study

```bash
# 探索不同参数的影响
# Explore impact of different parameters
python example_analysis.py
```

### 5. 集成您的中微子模型 / Integrate Your Neutrino Model

编辑 `neutrino_model_template.py` 中的函数:
Edit functions in `neutrino_model_template.py`:

```python
def neutrino_luminosity_TQM(M_bh, a, z, E_nu=1e5):
    # 在这里实现您的TQM模型
    # Implement your TQM model here
    
    # 示例: 从您的研究中获取中微子光度
    # Example: Get neutrino luminosity from your research
    L_nu = your_tqm_function(M_bh, a, z, E_nu)
    
    return L_nu
```

然后运行 / Then run:
```bash
python neutrino_model_template.py
```

## 主要功能 / Main Features

### 计算GRB率密度 / Calculate GRB Rate Density

```python
from agn_grb_distribution import AGNGRBPopulation

pop = AGNGRBPopulation()

# 特定红移和黑洞质量的GRB率
# GRB rate for specific redshift and black hole mass
rate = pop.grb_rate_density(M_bh=1e8, z=1.0)
print(f"Rate: {rate:.2e} Mpc^-3 yr^-1")

# 总GRB率密度
# Total GRB rate density
total = pop.total_grb_rate_at_z(z=1.0)
print(f"Total: {total:.2e} Mpc^-3 yr^-1")
```

### 修改模型参数 / Modify Model Parameters

```python
# 调整GRB率归一化
# Adjust GRB rate normalization
pop.grb_dist.R_GRB_norm = 5e-3  # 增加5倍 / 5x increase

# 修改质量依赖指数
# Modify mass dependence index
pop.grb_dist.mass_index = 1.0  # 更强的质量依赖

# 调整AGN质量函数
# Adjust AGN mass function
pop.agn_mf.M_star = 5e7  # 改变特征质量
pop.agn_mf.phi_star = 2e-5  # 改变归一化
```

### 计算累积GRB率 / Calculate Cumulative GRB Rate

```python
# 计算到红移z_max的总GRB率
# Calculate total GRB rate up to redshift z_max
cumulative_rate = pop.cumulative_grb_rate(z_max=3.0, z_bins=50)
print(f"Cumulative rate (z<3): {cumulative_rate:.2e} yr^-1")
```

## 常见任务 / Common Tasks

### 任务1: 估算中微子事件率 / Task 1: Estimate Neutrino Event Rate

```python
# 假设每个GRB产生N个可探测中微子
# Assume each GRB produces N detectable neutrinos
N_nu_per_grb = 0.1
total_grb_rate = pop.cumulative_grb_rate(z_max=3.0)
nu_event_rate = total_grb_rate * N_nu_per_grb

print(f"Expected neutrino events: {nu_event_rate:.2e} yr^-1")
```

### 任务2: 参数扫描 / Task 2: Parameter Scan

```python
import numpy as np

# 扫描不同的GRB率归一化
# Scan different GRB rate normalizations
R_norms = np.logspace(-4, -2, 10)
results = []

for R_norm in R_norms:
    pop.grb_dist.R_GRB_norm = R_norm
    rate = pop.total_grb_rate_at_z(z=1.0)
    results.append(rate)
    print(f"R_norm={R_norm:.2e}: rate={rate:.2e}")
```

### 任务3: 比较不同红移 / Task 3: Compare Different Redshifts

```python
# 计算不同红移的GRB率
# Calculate GRB rate at different redshifts
for z in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
    rate = pop.total_grb_rate_at_z(z)
    print(f"z={z:.1f}: {rate:.2e} Mpc^-3 yr^-1")
```

## 下一步 / Next Steps

1. **详细文档** / Detailed Documentation
   - 阅读 `README.md` 了解完整功能
   - 查看 `DOCUMENTATION_CN.md` 获取详细说明

2. **自定义模型** / Customize Models
   - 修改 `agn_grb_distribution.py` 中的参数
   - 在 `neutrino_model_template.py` 中实现您的中微子模型

3. **数据分析** / Data Analysis
   - 使用 `plot_agn_grb_distributions.py` 生成图表
   - 使用 `example_analysis.py` 进行参数研究

4. **与观测比较** / Compare with Observations
   - 导入IceCube数据
   - 进行统计分析
   - 评估模型约束

## 故障排除 / Troubleshooting

### 问题: 导入错误 / Issue: Import Error
```bash
# 确保安装了所有依赖
# Make sure all dependencies are installed
pip install -r requirements.txt
```

### 问题: 计算太慢 / Issue: Calculation Too Slow
```python
# 减少积分采样点数
# Reduce integration sampling points
pop.cumulative_grb_rate(z_max=3.0, z_bins=20)  # 使用更少的点
```

### 问题: 结果不合理 / Issue: Unrealistic Results
```python
# 检查参数设置
# Check parameter settings
print(f"R_GRB_norm: {pop.grb_dist.R_GRB_norm}")
print(f"mass_index: {pop.grb_dist.mass_index}")
print(f"M_star: {pop.agn_mf.M_star}")
```

## 支持 / Support

- 查看GitHub Issues
- 阅读详细文档
- 运行示例脚本理解用法

祝研究顺利！/ Good luck with your research!
