#!/usr/bin/env python3
"""
示例：使用IceCube IC86有效面积计算中微子探测率
Example: Calculate neutrino detection rates using IceCube IC86 effective area

这个脚本演示如何使用有效面积数据来计算不同中微子源的探测率。
This script demonstrates how to use the effective area data to calculate 
detection rates for different neutrino sources.
"""

import numpy as np
import matplotlib.pyplot as plt
from icecube_ic86_effective_area import IceCubeIC86EffectiveArea


def atmospheric_neutrino_flux(energy_gev):
    """
    大气中微子通量的简化模型 (E^-3.7)
    Simplified atmospheric neutrino flux model (E^-3.7)
    
    Parameters:
    -----------
    energy_gev : float or array
        Neutrino energy in GeV
        
    Returns:
    --------
    float or array
        Flux in GeV^-1 cm^-2 s^-1 sr^-1
    """
    # 归一化常数 (在1 TeV处)
    # Normalization constant (at 1 TeV)
    norm = 1.5e-11  # GeV^-1 cm^-2 s^-1 sr^-1
    E0 = 1e3  # GeV (1 TeV)
    return norm * (energy_gev / E0)**(-3.7)


def astrophysical_neutrino_flux(energy_gev):
    """
    天体物理中微子通量 (E^-2.5) - 类似IceCube观测
    Astrophysical neutrino flux (E^-2.5) - similar to IceCube observations
    
    Parameters:
    -----------
    energy_gev : float or array
        Neutrino energy in GeV
        
    Returns:
    --------
    float or array
        Flux in GeV^-1 cm^-2 s^-1 sr^-1
        
    Notes:
    ------
    Based on IceCube measurements of astrophysical neutrino flux.
    References:
    - IceCube Collaboration, Science 342, 1242856 (2013)
      DOI: 10.1126/science.1242856
    - IceCube Collaboration, ApJ 809, 98 (2015)
      DOI: 10.1088/0004-637X/809/1/98
    """
    # IceCube观测到的天体物理中微子通量
    # Astrophysical neutrino flux observed by IceCube
    norm = 6.7e-18  # GeV^-1 cm^-2 s^-1 sr^-1 at 100 TeV
    E0 = 1e5  # GeV (100 TeV)
    return norm * (energy_gev / E0)**(-2.5)


def calculate_event_rate(ic86, energies, flux_func, label):
    """
    计算给定通量的事例率
    Calculate event rate for a given flux
    """
    print(f"\n{label}:")
    print("-" * 60)
    
    # 计算通量和探测率
    flux = flux_func(energies)
    rates = ic86.calculate_detection_rate(energies, flux)
    
    # 对能量积分得到总事例率 (每秒每立体角)
    # Integrate over energy to get total event rate (per second per steradian)
    total_rate_per_sr = np.trapz(rates, energies)
    
    # 假设全天空覆盖 (4π立体角)
    # Assume full sky coverage (4π steradians)
    total_rate_per_year = total_rate_per_sr * 4 * np.pi * 365.25 * 24 * 3600
    
    print(f"  能量范围 / Energy range: {energies[0]:.0e} - {energies[-1]:.0e} GeV")
    print(f"  总事例率 / Total rate: {total_rate_per_sr:.2e} events/s/sr")
    print(f"  全天年事例率 / Full sky yearly rate: {total_rate_per_year:.2f} events/year")
    
    return flux, rates, total_rate_per_year


def main():
    """主函数 / Main function"""
    print("=" * 60)
    print("IceCube IC86 中微子探测率计算示例")
    print("IceCube IC86 Neutrino Detection Rate Calculation Example")
    print("=" * 60)
    
    # 创建有效面积计算器
    # Create effective area calculator
    ic86 = IceCubeIC86EffectiveArea()
    
    # 定义能量范围：100 GeV 到 10 PeV
    # Define energy range: 100 GeV to 10 PeV
    energies = np.logspace(2, 7, 200)  # GeV
    
    # 计算大气中微子探测率
    # Calculate atmospheric neutrino detection rate
    flux_atm, rates_atm, total_atm = calculate_event_rate(
        ic86, energies, atmospheric_neutrino_flux, 
        "大气中微子 / Atmospheric Neutrinos"
    )
    
    # 计算天体物理中微子探测率
    # Calculate astrophysical neutrino detection rate
    flux_astro, rates_astro, total_astro = calculate_event_rate(
        ic86, energies, astrophysical_neutrino_flux,
        "天体物理中微子 / Astrophysical Neutrinos"
    )
    
    # 绘制结果
    # Plot results
    print("\n" + "=" * 60)
    print("生成图表 / Generating plots...")
    print("=" * 60)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # 图1：通量对比
    # Plot 1: Flux comparison
    ax1.loglog(energies, flux_atm, 'b-', linewidth=2, label='大气中微子 / Atmospheric')
    ax1.loglog(energies, flux_astro, 'r-', linewidth=2, label='天体物理 / Astrophysical')
    ax1.set_xlabel('中微子能量 / Neutrino Energy (GeV)', fontsize=11)
    ax1.set_ylabel('通量 / Flux (GeV⁻¹ cm⁻² s⁻¹ sr⁻¹)', fontsize=11)
    ax1.set_title('中微子通量对比 / Neutrino Flux Comparison', fontsize=13)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # 图2：探测率对比
    # Plot 2: Detection rate comparison
    ax2.loglog(energies, rates_atm, 'b-', linewidth=2, 
               label=f'大气 / Atmospheric ({total_atm:.0f} events/year)')
    ax2.loglog(energies, rates_astro, 'r-', linewidth=2, 
               label=f'天体物理 / Astrophysical ({total_astro:.0f} events/year)')
    ax2.set_xlabel('中微子能量 / Neutrino Energy (GeV)', fontsize=11)
    ax2.set_ylabel('探测率 / Detection Rate (events s⁻¹ sr⁻¹)', fontsize=11)
    ax2.set_title('IceCube IC86 探测率 / Detection Rate', fontsize=13)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    try:
        plt.savefig('neutrino_detection_rates.png', dpi=300, bbox_inches='tight')
        print("图表已保存至 / Plot saved to: neutrino_detection_rates.png")
    except (IOError, OSError) as e:
        print(
            f"警告：无法保存图表 / Warning: Could not save plot: {e}\n"
            f"请检查文件权限和磁盘空间 / Please check file permissions and disk space."
        )
    
    # 额外示例：计算特定能量的探测率
    # Additional example: calculate detection rate at specific energies
    print("\n" + "=" * 60)
    print("特定能量点的详细信息 / Details at Specific Energies")
    print("=" * 60)
    
    test_energies = [1e3, 1e4, 1e5, 1e6]  # GeV
    for E in test_energies:
        A_eff = ic86.get_effective_area(E)
        flux_a = atmospheric_neutrino_flux(E)
        flux_b = astrophysical_neutrino_flux(E)
        rate_a = ic86.calculate_detection_rate(E, flux_a)
        rate_b = ic86.calculate_detection_rate(E, flux_b)
        
        print(f"\n能量 / Energy: {E:.0e} GeV ({E/1e3:.0f} TeV)")
        print(f"  有效面积 / Effective area: {A_eff:.2f} m²")
        print(f"  大气通量 / Atm. flux: {flux_a:.2e} GeV⁻¹ cm⁻² s⁻¹ sr⁻¹")
        print(f"  天体通量 / Astro. flux: {flux_b:.2e} GeV⁻¹ cm⁻² s⁻¹ sr⁻¹")
        print(f"  大气探测率 / Atm. rate: {rate_a:.2e} events s⁻¹ sr⁻¹")
        print(f"  天体探测率 / Astro. rate: {rate_b:.2e} events s⁻¹ sr⁻¹")
    
    print("\n" + "=" * 60)
    print("完成！/ Completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
