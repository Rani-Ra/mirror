"""
简单示例：计算不同模型参数下的AGN-GRB分布
Simple Example: Calculate AGN-GRB distributions with different model parameters

这个脚本展示如何使用框架来探索参数空间
This script demonstrates how to use the framework to explore parameter space
"""

import numpy as np
from agn_grb_distribution import AGNGRBPopulation, AGNMassFunction, GRBDistributionInAGN


def compare_mass_functions():
    """比较不同参数下的AGN质量函数 / Compare AGN mass functions with different parameters"""
    print("\n" + "="*60)
    print("1. AGN质量函数比较 / AGN Mass Function Comparison")
    print("="*60)
    
    # 创建两个不同参数的质量函数 / Create two mass functions with different parameters
    agn_mf_1 = AGNMassFunction()
    agn_mf_2 = AGNMassFunction()
    
    # 修改第二个模型的参数 / Modify parameters of the second model
    agn_mf_2.M_star = 5e7
    agn_mf_2.alpha = -0.7
    
    M_bh = 1e8  # Solar masses
    z = 1.0
    
    phi_1 = agn_mf_1.dn_dlogM_dVc(M_bh, z)
    phi_2 = agn_mf_2.dn_dlogM_dVc(M_bh, z)
    
    print(f"\n模型1 (标准参数) / Model 1 (standard parameters):")
    print(f"  M* = {agn_mf_1.M_star:.1e} M_sun, alpha = {agn_mf_1.alpha}")
    print(f"  phi(M={M_bh:.1e}, z={z}) = {phi_1:.2e} Mpc^-3")
    
    print(f"\n模型2 (修改参数) / Model 2 (modified parameters):")
    print(f"  M* = {agn_mf_2.M_star:.1e} M_sun, alpha = {agn_mf_2.alpha}")
    print(f"  phi(M={M_bh:.1e}, z={z}) = {phi_2:.2e} Mpc^-3")
    
    print(f"\n比率 / Ratio: {phi_2/phi_1:.2f}")


def compare_grb_rates():
    """比较不同质量指数下的GRB率 / Compare GRB rates with different mass indices"""
    print("\n" + "="*60)
    print("2. GRB率比较 / GRB Rate Comparison")
    print("="*60)
    
    # 创建不同质量依赖的GRB分布 / Create GRB distributions with different mass dependence
    grb_1 = GRBDistributionInAGN()
    grb_2 = GRBDistributionInAGN()
    grb_3 = GRBDistributionInAGN()
    
    grb_1.mass_index = 0.0  # No mass dependence
    grb_2.mass_index = 0.5  # Standard
    grb_3.mass_index = 1.0  # Strong mass dependence
    
    M_array = np.array([1e7, 1e8, 1e9])
    
    print("\nGRB率 vs 黑洞质量 / GRB rate vs black hole mass:")
    print(f"{'M_BH [M_sun]':<15} {'Index=0.0':<15} {'Index=0.5':<15} {'Index=1.0':<15}")
    print("-" * 60)
    
    for M in M_array:
        r1 = grb_1.grb_rate_per_agn(M)
        r2 = grb_2.grb_rate_per_agn(M)
        r3 = grb_3.grb_rate_per_agn(M)
        print(f"{M:<15.1e} {r1:<15.2e} {r2:<15.2e} {r3:<15.2e}")


def explore_redshift_dependence():
    """探索红移依赖性 / Explore redshift dependence"""
    print("\n" + "="*60)
    print("3. 红移依赖性分析 / Redshift Dependence Analysis")
    print("="*60)
    
    pop = AGNGRBPopulation()
    
    z_array = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    
    print("\nGRB率密度 vs 红移 / GRB rate density vs redshift:")
    print(f"{'z':<10} {'Rate [Mpc^-3 yr^-1]':<25} {'Relative to z=1':<20}")
    print("-" * 55)
    
    rates = []
    for z in z_array:
        rate = pop.total_grb_rate_at_z(z)
        rates.append(rate)
    
    rate_at_z1 = rates[2]  # z=1.0
    
    for z, rate in zip(z_array, rates):
        rel = rate / rate_at_z1 if rate_at_z1 > 0 else 0
        print(f"{z:<10.1f} {rate:<25.2e} {rel:<20.2f}")


def estimate_neutrino_background():
    """估算中微子背景贡献 / Estimate neutrino background contribution"""
    print("\n" + "="*60)
    print("4. 中微子背景估算 / Neutrino Background Estimation")
    print("="*60)
    
    pop = AGNGRBPopulation()
    
    # 计算不同红移范围的累积GRB率 / Calculate cumulative GRB rate for different redshift ranges
    z_ranges = [1.0, 2.0, 3.0, 4.0]
    
    print("\n累积GRB率 / Cumulative GRB rate:")
    print(f"{'z_max':<10} {'Total Rate [yr^-1]':<25} {'Contribution %':<20}")
    print("-" * 55)
    
    total_rate_max = None
    cumulative_rates = []
    
    for z_max in z_ranges:
        rate = pop.cumulative_grb_rate(z_max, z_bins=20)
        cumulative_rates.append(rate)
        if z_max == max(z_ranges):
            total_rate_max = rate
    
    for z_max, rate in zip(z_ranges, cumulative_rates):
        contrib = (rate / total_rate_max * 100) if total_rate_max > 0 else 0
        print(f"{z_max:<10.1f} {rate:<25.2e} {contrib:<20.1f}")
    
    print(f"\n总GRB率 (z < {max(z_ranges)}) / Total GRB rate: {total_rate_max:.2e} yr^-1")
    
    # 估算中微子事件率 / Estimate neutrino event rate
    # 假设每个GRB产生N个可探测的中微子 / Assume each GRB produces N detectable neutrinos
    N_nu_per_grb = 0.1  # 示例值 / Example value
    nu_event_rate = total_rate_max * N_nu_per_grb
    
    print(f"\n假设每个GRB产生 {N_nu_per_grb} 个可探测中微子:")
    print(f"Assuming {N_nu_per_grb} detectable neutrinos per GRB:")
    print(f"预期中微子事件率 / Expected neutrino event rate: {nu_event_rate:.2e} yr^-1")


def parameter_sensitivity():
    """参数敏感性分析 / Parameter sensitivity analysis"""
    print("\n" + "="*60)
    print("5. 参数敏感性分析 / Parameter Sensitivity Analysis")
    print("="*60)
    
    pop = AGNGRBPopulation()
    z = 1.0
    
    # 基准值 / Baseline
    baseline_rate = pop.total_grb_rate_at_z(z)
    
    print(f"\n基准GRB率密度 (z={z}) / Baseline GRB rate density: {baseline_rate:.2e} Mpc^-3 yr^-1")
    print("\n参数变化的影响 / Impact of parameter variations:")
    print(f"{'Parameter':<25} {'Change':<15} {'New Rate':<20} {'Ratio':<10}")
    print("-" * 70)
    
    # 测试不同参数 / Test different parameters
    
    # GRB率归一化 / GRB rate normalization
    pop.grb_dist.R_GRB_norm *= 2.0
    rate_new = pop.total_grb_rate_at_z(z)
    print(f"{'R_GRB_norm':<25} {'×2':<15} {rate_new:<20.2e} {rate_new/baseline_rate:<10.2f}")
    pop.grb_dist.R_GRB_norm /= 2.0  # 恢复 / Reset
    
    # 质量指数 / Mass index
    pop.grb_dist.mass_index = 1.0
    rate_new = pop.total_grb_rate_at_z(z)
    print(f"{'mass_index':<25} {'0.5→1.0':<15} {rate_new:<20.2e} {rate_new/baseline_rate:<10.2f}")
    pop.grb_dist.mass_index = 0.5  # 恢复 / Reset
    
    # AGN质量函数归一化 / AGN mass function normalization
    pop.agn_mf.phi_star *= 1.5
    rate_new = pop.total_grb_rate_at_z(z)
    print(f"{'phi_star':<25} {'×1.5':<15} {rate_new:<20.2e} {rate_new/baseline_rate:<10.2f}")
    pop.agn_mf.phi_star /= 1.5  # 恢复 / Reset


def main():
    """运行所有示例 / Run all examples"""
    print("\n" + "="*60)
    print("AGN-GRB分布分析示例 / AGN-GRB Distribution Analysis Examples")
    print("="*60)
    
    compare_mass_functions()
    compare_grb_rates()
    explore_redshift_dependence()
    estimate_neutrino_background()
    parameter_sensitivity()
    
    print("\n" + "="*60)
    print("分析完成！/ Analysis complete!")
    print("="*60)
    print("\n提示 / Tips:")
    print("- 运行 python plot_agn_grb_distributions.py 生成图表")
    print("- Run python plot_agn_grb_distributions.py to generate plots")
    print("- 修改参数以探索不同的物理场景")
    print("- Modify parameters to explore different physical scenarios")
    print("- 添加您自己的中微子发射模型")
    print("- Add your own neutrino emission model")
    print()


if __name__ == "__main__":
    main()
