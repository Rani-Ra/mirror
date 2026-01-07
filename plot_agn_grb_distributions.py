"""
Visualization and analysis tools for AGN-GRB distributions.

This script provides plotting utilities to visualize:
1. AGN mass function at different redshifts
2. Redshift evolution of AGN and GRB populations
3. GRB radial distribution in AGN disks
4. Combined AGN-GRB rate densities
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from agn_grb_distribution import (
    AGNMassFunction, AGNRedshiftEvolution, 
    GRBDistributionInAGN, AGNGRBPopulation
)


def plot_agn_mass_function():
    """Plot AGN mass function at different redshifts."""
    agn_mf = AGNMassFunction()
    
    M_bh = np.logspace(6, 10, 100)
    redshifts = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    colors = cm.viridis(np.linspace(0, 1, len(redshifts)))
    
    for z, color in zip(redshifts, colors):
        phi = agn_mf.dn_dlogM_dVc(M_bh, z)
        ax.plot(M_bh, phi, label=f'z = {z}', color=color, linewidth=2)
    
    ax.set_xlabel(r'$M_{\rm BH}$ [$M_{\odot}$]', fontsize=14)
    ax.set_ylabel(r'$dn/d\log M$ [Mpc$^{-3}$]', fontsize=14)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_title('AGN Mass Function vs Redshift', fontsize=16)
    ax.legend(loc='best', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('agn_mass_function.png', dpi=150)
    print("Saved: agn_mass_function.png")
    plt.close()


def plot_redshift_evolution():
    """Plot redshift evolution of AGN and GRB populations."""
    pop = AGNGRBPopulation()
    
    z_array = np.linspace(0, 3, 50)
    
    # Calculate total AGN density and GRB rate at each redshift
    grb_rate = []
    comoving_volume = []
    
    for z in z_array:
        # GRB rate density
        rate = pop.total_grb_rate_at_z(z)
        grb_rate.append(rate)
        
        # Comoving volume element
        dV = pop.agn_z.comoving_volume(z)
        comoving_volume.append(dV)
    
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))
    
    # Plot 1: GRB rate density
    ax1 = axes[0]
    
    line1 = ax1.plot(z_array, grb_rate, 'r-', linewidth=2, 
                     label='GRB Rate Density')
    
    ax1.set_xlabel('Redshift z', fontsize=14)
    ax1.set_ylabel('GRB Rate Density [Mpc$^{-3}$ yr$^{-1}$]', fontsize=14, color='r')
    ax1.tick_params(axis='y', labelcolor='r')
    ax1.set_title('Redshift Evolution of GRB Population in AGN', fontsize=16)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left', fontsize=12)
    
    # Comoving volume element
    ax2 = axes[1]
    ax2.plot(z_array, np.array(comoving_volume) / 1e9, 'g-', linewidth=2)
    ax2.set_xlabel('Redshift z', fontsize=14)
    ax2.set_ylabel('dV/dz [10$^9$ Mpc$^3$]', fontsize=14)
    ax2.set_title('Comoving Volume Element', fontsize=16)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('redshift_evolution.png', dpi=150)
    print("Saved: redshift_evolution.png")
    plt.close()


def plot_grb_radial_distribution():
    """Plot GRB radial distribution in AGN disk."""
    grb_dist = GRBDistributionInAGN()
    
    a_array = np.logspace(2, 4, 200)  # 100 to 10000 r_g
    M_bh = 1e8  # Solar masses
    
    prob_density = grb_dist.radial_distribution(a_array, M_bh)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    ax.plot(a_array, prob_density, 'b-', linewidth=2)
    ax.fill_between(a_array, 0, prob_density, alpha=0.3)
    
    ax.set_xlabel(r'Semi-major Axis [r$_g$]', fontsize=14)
    ax.set_ylabel('Probability Density', fontsize=14)
    ax.set_xscale('log')
    ax.set_title(f'GRB Radial Distribution in AGN Disk (M$_{{BH}}$ = {M_bh:.1e} M$_\\odot$)', 
                 fontsize=16)
    ax.grid(True, alpha=0.3)
    
    # Add shaded regions
    ax.axvspan(grb_dist.a_min, 1e3, alpha=0.1, color='red', 
               label='Inner disk')
    ax.axvspan(1e3, grb_dist.a_max, alpha=0.1, color='blue', 
               label='Outer disk')
    ax.legend(loc='best', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('grb_radial_distribution.png', dpi=150)
    print("Saved: grb_radial_distribution.png")
    plt.close()


def plot_grb_rate_vs_mass():
    """Plot GRB rate as function of black hole mass."""
    grb_dist = GRBDistributionInAGN()
    
    M_bh = np.logspace(6, 10, 100)
    rate = grb_dist.grb_rate_per_agn(M_bh)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    ax.plot(M_bh, rate, 'r-', linewidth=2)
    ax.set_xlabel(r'$M_{\rm BH}$ [$M_{\odot}$]', fontsize=14)
    ax.set_ylabel(r'GRB Rate [yr$^{-1}$]', fontsize=14)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_title('GRB Rate per AGN vs Black Hole Mass', fontsize=16)
    ax.grid(True, alpha=0.3)
    
    # Add reference lines
    ax.axhline(grb_dist.R_GRB_norm, color='k', linestyle='--', 
               label=f'Reference rate at M = {grb_dist.M_ref:.1e} M$_\\odot$')
    ax.legend(loc='best', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('grb_rate_vs_mass.png', dpi=150)
    print("Saved: grb_rate_vs_mass.png")
    plt.close()


def plot_combined_rate_density():
    """Plot combined AGN-GRB rate density as 2D map."""
    pop = AGNGRBPopulation()
    
    # Create 2D grid
    M_bh_array = np.logspace(6, 10, 30)
    z_array = np.linspace(0, 3, 30)
    
    M_grid, z_grid = np.meshgrid(M_bh_array, z_array)
    rate_grid = np.zeros_like(M_grid)
    
    for i in range(len(z_array)):
        for j in range(len(M_bh_array)):
            rate_grid[i, j] = pop.grb_rate_density(M_grid[i, j], z_grid[i, j])
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Use logarithmic color scale
    pcm = ax.pcolormesh(M_grid, z_grid, np.log10(rate_grid + 1e-20), 
                        cmap='viridis', shading='auto')
    
    ax.set_xlabel(r'$M_{\rm BH}$ [$M_{\odot}$]', fontsize=14)
    ax.set_ylabel('Redshift z', fontsize=14)
    ax.set_xscale('log')
    ax.set_title('GRB Rate Density: log$_{10}$(dR/dV/dlogM) [Mpc$^{-3}$ yr$^{-1}$]', 
                 fontsize=16)
    
    cbar = plt.colorbar(pcm, ax=ax)
    cbar.set_label('log$_{10}$(Rate Density)', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('combined_rate_density_2d.png', dpi=150)
    print("Saved: combined_rate_density_2d.png")
    plt.close()


def plot_cumulative_grb_rate():
    """Plot cumulative GRB rate vs redshift."""
    pop = AGNGRBPopulation()
    
    z_max_array = np.linspace(0.1, 3.0, 20)
    cumulative_rates = []
    
    print("Calculating cumulative rates...")
    for z_max in z_max_array:
        rate = pop.cumulative_grb_rate(z_max, z_bins=20)
        cumulative_rates.append(rate)
        print(f"  z_max = {z_max:.2f}: R_total = {rate:.2e} yr^-1")
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    ax.plot(z_max_array, cumulative_rates, 'b-', linewidth=2, marker='o')
    ax.set_xlabel('Maximum Redshift z$_{max}$', fontsize=14)
    ax.set_ylabel('Cumulative GRB Rate [yr$^{-1}$]', fontsize=14)
    ax.set_yscale('log')
    ax.set_title('Cumulative GRB Rate in AGN', fontsize=16)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('cumulative_grb_rate.png', dpi=150)
    print("Saved: cumulative_grb_rate.png")
    plt.close()


def main():
    """Generate all plots."""
    print("Generating AGN-GRB Distribution Plots")
    print("=" * 50)
    
    try:
        print("\n1. AGN Mass Function...")
        plot_agn_mass_function()
        
        print("\n2. Redshift Evolution...")
        plot_redshift_evolution()
        
        print("\n3. GRB Radial Distribution...")
        plot_grb_radial_distribution()
        
        print("\n4. GRB Rate vs Mass...")
        plot_grb_rate_vs_mass()
        
        print("\n5. Combined Rate Density (2D)...")
        plot_combined_rate_density()
        
        print("\n6. Cumulative GRB Rate...")
        plot_cumulative_grb_rate()
        
        print("\n" + "=" * 50)
        print("All plots generated successfully!")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
