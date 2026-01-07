"""
中微子发射模型模板 / Neutrino Emission Model Template

这个脚本展示了如何将您的TQM或SG模型集成到框架中
This script demonstrates how to integrate your TQM or SG model into the framework

使用说明 / Instructions:
1. 在下面的函数中实现您的中微子辐射模型
   Implement your neutrino radiation model in the functions below
2. 运行此脚本计算中微子背景贡献
   Run this script to calculate neutrino background contribution
3. 根据需要修改参数和能量范围
   Modify parameters and energy ranges as needed
"""

import numpy as np
from agn_grb_distribution import (
    AGNGRBPopulation, 
    NeutrinoBackgroundCalculator,
    AGNRedshiftEvolution
)
from scipy import integrate


# ============================================================================
# 第1部分: 定义您的中微子发射模型
# Part 1: Define your neutrino emission model
# ============================================================================

def neutrino_luminosity_TQM(M_bh, a, z, E_nu=1e5):
    """
    TQM (Thick Disk) 模型的中微子光度
    Neutrino luminosity for TQM (Thick Disk) model
    
    Parameters:
    -----------
    M_bh : float
        黑洞质量 [M_☉] / Black hole mass [M_sun]
    a : float
        GRB位置的半长轴 [r_g] / Semi-major axis of GRB location [r_g]
    z : float
        红移 / Redshift
    E_nu : float
        中微子能量 [GeV] / Neutrino energy [GeV]
        
    Returns:
    --------
    L_nu : float
        中微子光度 [erg/s/GeV] / Neutrino luminosity [erg/s/GeV]
        
    Notes:
    ------
    这是一个示例实现，请替换为您的实际模型！
    This is an example implementation, please replace with your actual model!
    
    典型的依赖关系 / Typical dependencies:
    - L_nu ∝ M_bh^α (黑洞质量依赖 / mass dependence)
    - L_nu ∝ a^β (径向依赖 / radial dependence)
    - L_nu ∝ E_nu^(-γ) (能谱 / energy spectrum)
    """
    
    # 示例实现 - 请替换为您的模型！
    # Example implementation - replace with your model!
    
    # 基本参数
    r_g = 1.48e5 * (M_bh / 1e8)  # cm, 引力半径
    r = a * r_g  # cm, 实际半径
    
    # 盘密度和温度（简化模型）
    # Disk density and temperature (simplified)
    Sigma = 1e5 * (r / 1e14)**(-0.75)  # g/cm^2, 表面密度
    T = 1e6 * (r / 1e14)**(-0.5)  # K, 温度
    
    # GRB喷流参数
    # GRB jet parameters
    L_jet = 1e52  # erg/s, 喷流光度
    Gamma_jet = 100  # 洛伦兹因子
    
    # 中微子产生效率（示例）
    # Neutrino production efficiency (example)
    f_nu = 0.1  # 10%的能量转化为中微子
    
    # 能谱（简单幂律）
    # Energy spectrum (simple power-law)
    E_break = 1e5  # GeV
    gamma = 2.0  # 谱指数
    L_nu = f_nu * L_jet / E_break * (E_nu / E_break)**(-gamma)
    
    # 径向依赖（来自喷流-盘相互作用）
    # Radial dependence (from jet-disk interaction)
    L_nu *= (a / 1e3)**(-0.5)
    
    # 质量依赖
    # Mass dependence
    L_nu *= (M_bh / 1e8)**0.5
    
    return L_nu


def neutrino_luminosity_SG(M_bh, a, z, E_nu=1e5):
    """
    SG (Self-Gravity) 模型的中微子光度
    Neutrino luminosity for SG (Self-Gravity) model
    
    Parameters: 同TQM模型 / Same as TQM model
    
    Notes:
    ------
    SG模型通常假设盘在某些区域自引力不稳定
    SG model typically assumes disk self-gravity instability in some regions
    """
    
    # 示例实现 - 请替换为您的模型！
    # Example implementation - replace with your model!
    
    # 自引力区域的判据
    # Self-gravity criterion
    r_g = 1.48e5 * (M_bh / 1e8)  # cm
    r = a * r_g
    
    # 盘参数（自引力盘更厚）
    # Disk parameters (self-gravity disk is thicker)
    H_over_r = 0.3  # 较大的纵横比
    Sigma = 1e6 * (r / 1e14)**(-1.0)  # 更陡的密度轮廓
    
    # 中微子产生（假设更强的相互作用）
    # Neutrino production (assuming stronger interaction)
    L_jet = 1e52  # erg/s
    f_nu = 0.15  # 更高的效率
    
    # 能谱
    E_break = 1e5  # GeV
    gamma = 2.2
    L_nu = f_nu * L_jet / E_break * (E_nu / E_break)**(-gamma)
    
    # 径向和质量依赖
    L_nu *= (a / 1e3)**(-0.7)  # 更强的径向依赖
    L_nu *= (M_bh / 1e8)**0.6
    
    return L_nu


# ============================================================================
# 第2部分: 计算中微子背景
# Part 2: Calculate neutrino background
# ============================================================================

def calculate_neutrino_background(model='TQM', E_nu=1e5, z_max=3.0):
    """
    计算中微子背景流量
    Calculate neutrino background flux
    
    Parameters:
    -----------
    model : str
        'TQM' 或 'SG' / 'TQM' or 'SG'
    E_nu : float
        中微子能量 [GeV] / Neutrino energy [GeV]
    z_max : float
        最大红移 / Maximum redshift
        
    Returns:
    --------
    flux : float
        中微子流量 [GeV^-1 cm^-2 s^-1 sr^-1]
        Neutrino flux
    """
    
    print(f"\n计算 {model} 模型的中微子背景...")
    print(f"Calculating neutrino background for {model} model...")
    print(f"中微子能量 / Neutrino energy: E_ν = {E_nu:.1e} GeV")
    print(f"红移范围 / Redshift range: 0 < z < {z_max}")
    
    # 选择模型
    if model == 'TQM':
        L_nu_func = neutrino_luminosity_TQM
    elif model == 'SG':
        L_nu_func = neutrino_luminosity_SG
    else:
        raise ValueError(f"Unknown model: {model}")
    
    # 初始化
    pop = AGNGRBPopulation()
    cosmo = AGNRedshiftEvolution()
    
    # 物理常数
    c = 3e10  # cm/s
    
    # 积分参数
    M_bh_array = np.logspace(7, 9, 20)  # M_sun
    z_array = np.linspace(0.1, z_max, 20)
    a_array = np.logspace(2, 4, 15)  # r_g
    
    flux_total = 0.0
    
    # 三重积分: over z, M_bh, a
    print("\n积分计算中...")
    print("Integration in progress...")
    
    for i, z in enumerate(z_array):
        if i % 5 == 0:
            print(f"  z = {z:.2f} ({i+1}/{len(z_array)})")
        
        # 共动光度距离
        d_L = cosmo.comoving_distance(z) * (1 + z) * 3.086e24  # cm
        
        # 体积元
        dV_dz = cosmo.comoving_volume(z) * 3.086e73  # cm^3
        
        for M_bh in M_bh_array:
            # AGN数密度
            n_agn = pop.agn_mf.dn_dlogM_dVc(M_bh, z)  # Mpc^-3
            n_agn *= (3.086e24)**(-3)  # cm^-3
            
            # GRB率
            R_grb = pop.grb_dist.grb_rate_per_agn(M_bh) / (365.25 * 86400)  # s^-1
            
            for a in a_array:
                # 径向分布概率
                P_a = pop.grb_dist.radial_distribution(a, M_bh)
                
                # 中微子光度
                L_nu = L_nu_func(M_bh, a, z, E_nu)
                
                # 贡献到流量
                # Φ = (L_nu / 4πd_L^2) × n_agn × R_grb × P_a × dV/dz × dz × dlogM × da
                dflux = (L_nu / (4 * np.pi * d_L**2)) * n_agn * R_grb * P_a
                
                # 累加
                flux_total += dflux
    
    # 归一化（近似）
    dz = z_array[1] - z_array[0]
    dlogM = np.log10(M_bh_array[1]) - np.log10(M_bh_array[0])
    dloga = np.log10(a_array[1]) - np.log10(a_array[0])
    
    flux_total *= dz * dlogM * dloga
    
    # 转换为每球面度
    flux_total /= (4 * np.pi)
    
    print(f"\n结果 / Result:")
    print(f"中微子流量 / Neutrino flux:")
    print(f"  Φ_ν(E={E_nu:.1e} GeV) = {flux_total:.2e} GeV^-1 cm^-2 s^-1 sr^-1")
    
    # 与IceCube对比（粗略）
    # Comparison with IceCube (rough)
    E_squared_flux = E_nu**2 * flux_total * 1.6e-3  # GeV cm^-2 s^-1 sr^-1
    print(f"  E^2 Φ_ν = {E_squared_flux:.2e} GeV cm^-2 s^-1 sr^-1")
    print(f"\nIceCube观测约束（参考）:")
    print(f"IceCube constraint (reference):")
    print(f"  E^2 Φ_ν ~ 10^-8 GeV cm^-2 s^-1 sr^-1 (弥散背景)")
    print(f"  E^2 Φ_ν ~ 10^-8 GeV cm^-2 s^-1 sr^-1 (diffuse background)")
    
    return flux_total


def compare_models():
    """比较TQM和SG模型 / Compare TQM and SG models"""
    
    print("\n" + "="*70)
    print("中微子背景模型比较 / Neutrino Background Model Comparison")
    print("="*70)
    
    # 能量点
    energies = [1e4, 1e5, 1e6]  # GeV
    
    results = {'TQM': [], 'SG': []}
    
    for E_nu in energies:
        print(f"\n{'='*70}")
        print(f"能量 / Energy: E_ν = {E_nu:.1e} GeV")
        print(f"{'='*70}")
        
        for model in ['TQM', 'SG']:
            flux = calculate_neutrino_background(model, E_nu, z_max=2.0)
            results[model].append(flux)
    
    # 汇总
    print(f"\n{'='*70}")
    print("汇总结果 / Summary")
    print(f"{'='*70}")
    print(f"\n{'能量 [GeV]':<15} {'TQM流量':<25} {'SG流量':<25} {'比率 SG/TQM':<15}")
    print("-"*80)
    
    for i, E_nu in enumerate(energies):
        ratio = results['SG'][i] / results['TQM'][i] if results['TQM'][i] > 0 else 0
        print(f"{E_nu:<15.1e} {results['TQM'][i]:<25.2e} {results['SG'][i]:<25.2e} {ratio:<15.2f}")


# ============================================================================
# 第3部分: 主程序
# Part 3: Main program
# ============================================================================

def main():
    """主程序 / Main program"""
    
    print("\n" + "="*70)
    print("AGN中GRB的中微子背景计算")
    print("Neutrino Background from GRBs in AGN")
    print("="*70)
    
    print("\n提示 / Note:")
    print("这是一个模板脚本，展示了如何集成您的中微子模型")
    print("This is a template script showing how to integrate your neutrino model")
    print("\n请在函数 neutrino_luminosity_TQM 和 neutrino_luminosity_SG 中")
    print("实现您的实际中微子辐射模型！")
    print("\nPlease implement your actual neutrino radiation model in functions")
    print("neutrino_luminosity_TQM and neutrino_luminosity_SG!")
    
    # 单个模型计算
    print("\n" + "-"*70)
    print("示例1: 单个模型计算 / Example 1: Single model calculation")
    print("-"*70)
    
    flux_tqm = calculate_neutrino_background('TQM', E_nu=1e5, z_max=2.0)
    
    # 模型比较
    print("\n" + "-"*70)
    print("示例2: 模型比较 / Example 2: Model comparison")
    print("-"*70)
    
    compare_models()
    
    print("\n" + "="*70)
    print("计算完成！/ Calculation complete!")
    print("="*70)
    
    print("\n下一步 / Next steps:")
    print("1. 用您的实际模型替换示例函数")
    print("   Replace example functions with your actual model")
    print("2. 调整积分参数以获得更高精度")
    print("   Adjust integration parameters for higher precision")
    print("3. 与观测数据比较")
    print("   Compare with observational data")
    print("4. 进行参数空间扫描")
    print("   Perform parameter space scan")
    print()


if __name__ == "__main__":
    main()
