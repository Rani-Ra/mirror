#!/usr/bin/env python3
"""
IceCube IC86 Effective Area Calculator

This module provides the average effective area of the IceCube IC86 detector
as a function of neutrino energy. The effective area is used to calculate
neutrino detection rates.

The data is based on typical IceCube IC86 configuration performance for
muon neutrinos (νμ) in the energy range from ~100 GeV to ~100 PeV.
"""

import numpy as np
import matplotlib.pyplot as plt


class IceCubeIC86EffectiveArea:
    """
    IceCube IC86 average effective area calculator.
    
    Provides effective area as a function of neutrino energy for the
    IceCube IC86 detector configuration (86 strings).
    """
    
    def __init__(self):
        """
        Initialize with typical IceCube IC86 effective area data.
        
        Energy range: 10^2 GeV to 10^8 GeV
        Effective area values are approximate averages for muon neutrinos
        """
        # Log10(Energy in GeV) vs Effective Area (in m^2)
        # These are representative values based on IceCube publications
        self.log_energies_gev = np.array([
            2.0,   # 100 GeV
            2.5,   # ~316 GeV
            3.0,   # 1 TeV
            3.5,   # ~3.16 TeV
            4.0,   # 10 TeV
            4.5,   # ~31.6 TeV
            5.0,   # 100 TeV
            5.5,   # ~316 TeV
            6.0,   # 1 PeV
            6.5,   # ~3.16 PeV
            7.0,   # 10 PeV
            7.5,   # ~31.6 PeV
            8.0    # 100 PeV
        ])
        
        # Effective area in m^2 (approximate values for muon neutrinos)
        # Based on typical IceCube IC86 performance
        self.effective_area_m2 = np.array([
            1e-3,    # 100 GeV - very small, near threshold
            0.01,    # ~316 GeV
            0.1,     # 1 TeV
            0.5,     # ~3.16 TeV
            2.0,     # 10 TeV
            8.0,     # ~31.6 TeV
            20.0,    # 100 TeV
            35.0,    # ~316 TeV
            45.0,    # 1 PeV
            50.0,    # ~3.16 PeV
            52.0,    # 10 PeV
            53.0,    # ~31.6 PeV
            53.5     # 100 PeV - approaches plateau
        ])
    
    def get_effective_area(self, energy_gev):
        """
        Get effective area at given neutrino energy.
        
        Parameters:
        -----------
        energy_gev : float or array-like
            Neutrino energy in GeV
            
        Returns:
        --------
        float or array
            Effective area in m^2
            
        Raises:
        -------
        ValueError
            If energy_gev contains non-positive values
        """
        energy_gev = np.atleast_1d(energy_gev)
        
        # Validate input
        if np.any(energy_gev <= 0):
            raise ValueError("Energy must be positive (> 0 GeV)")
        
        # Check bounds and warn if extrapolating
        min_energy = 10**self.log_energies_gev[0]
        max_energy = 10**self.log_energies_gev[-1]
        if np.any(energy_gev < min_energy) or np.any(energy_gev > max_energy):
            import warnings
            warnings.warn(
                f"Energy values outside calibrated range "
                f"({min_energy:.0e} - {max_energy:.0e} GeV). "
                f"Results will be extrapolated and may be inaccurate.",
                UserWarning
            )
        
        log_energy = np.log10(energy_gev)
        
        # Interpolate in log space
        effective_area = np.interp(
            log_energy,
            self.log_energies_gev,
            self.effective_area_m2
        )
        
        # Return scalar if input was scalar
        if len(energy_gev) == 1:
            return float(effective_area[0])
        return effective_area
    
    def calculate_detection_rate(self, energy_gev, flux_per_gev_cm2_s_sr):
        """
        Calculate neutrino detection rate.
        
        Parameters:
        -----------
        energy_gev : float or array-like
            Neutrino energy in GeV
        flux_per_gev_cm2_s_sr : float or array-like
            Differential neutrino flux in units of 1/(GeV cm^2 s sr)
            
        Returns:
        --------
        float or array
            Detection rate in events per second per steradian
        """
        effective_area = self.get_effective_area(energy_gev)
        # Convert effective area from m^2 to cm^2
        effective_area_cm2 = effective_area * 1e4
        
        # Detection rate = flux × effective area
        rate = flux_per_gev_cm2_s_sr * effective_area_cm2
        
        return rate
    
    def plot_effective_area(self, save_path=None):
        """
        Plot effective area vs energy.
        
        Parameters:
        -----------
        save_path : str, optional
            If provided, save the plot to this path
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        energies_gev = 10**self.log_energies_gev
        
        ax.loglog(energies_gev, self.effective_area_m2, 'o-', linewidth=2, markersize=8)
        ax.set_xlabel('Neutrino Energy (GeV)', fontsize=12)
        ax.set_ylabel('Effective Area (m²)', fontsize=12)
        ax.set_title('IceCube IC86 Average Effective Area for Muon Neutrinos', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        # Add secondary x-axis with TeV/PeV labels
        ax2 = ax.twiny()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_xscale('log')
        ax2.set_xlabel('Energy (TeV / PeV)', fontsize=12)
        tev_ticks = [0.1, 1, 10, 100, 1000, 10000, 100000]
        tev_labels = ['0.1 TeV', '1 TeV', '10 TeV', '100 TeV', '1 PeV', '10 PeV', '100 PeV']
        ax2.set_xticks([t*1e3 for t in tev_ticks])
        ax2.set_xticklabels(tev_labels, rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        return fig, ax
    
    def export_data(self, filename='ic86_effective_area.csv'):
        """
        Export effective area data to CSV file.
        
        Parameters:
        -----------
        filename : str
            Output filename
            
        Raises:
        -------
        IOError
            If file cannot be written
        """
        energies_gev = 10**self.log_energies_gev
        
        try:
            with open(filename, 'w') as f:
                f.write('# IceCube IC86 Average Effective Area\n')
                f.write('# Energy (GeV), Log10(Energy/GeV), Effective Area (m²)\n')
                for e, log_e, a in zip(energies_gev, self.log_energies_gev, self.effective_area_m2):
                    f.write(f'{e:.6e},{log_e:.2f},{a:.6e}\n')
            
            print(f"Data exported to {filename}")
        except (IOError, OSError) as e:
            raise IOError(f"Failed to write data to {filename}: {e}")


def main():
    """Example usage of IceCube IC86 effective area calculator."""
    print("=" * 60)
    print("IceCube IC86 Effective Area Calculator")
    print("=" * 60)
    
    # Create calculator instance
    ic86 = IceCubeIC86EffectiveArea()
    
    # Example 1: Get effective area at specific energies
    print("\n1. Effective Area at Specific Energies:")
    print("-" * 60)
    test_energies = [1e3, 1e4, 1e5, 1e6]  # GeV
    for energy in test_energies:
        area = ic86.get_effective_area(energy)
        print(f"  E = {energy:.0e} GeV ({energy/1e3:.0f} TeV): A_eff = {area:.2f} m²")
    
    # Example 2: Calculate detection rate for a simple flux
    print("\n2. Detection Rate Calculation:")
    print("-" * 60)
    # Assume a power-law flux: E^-2.5 with normalization
    energy = 1e5  # 100 TeV
    flux_norm = 1e-18  # GeV^-1 cm^-2 s^-1 sr^-1 at 100 TeV
    flux = flux_norm * (energy / 1e5)**(-2.5)
    rate = ic86.calculate_detection_rate(energy, flux)
    print(f"  Energy: {energy:.0e} GeV")
    print(f"  Flux: {flux:.2e} GeV^-1 cm^-2 s^-1 sr^-1")
    print(f"  Detection rate: {rate:.2e} events/s/sr")
    
    # Example 3: Export data
    print("\n3. Exporting Data:")
    print("-" * 60)
    ic86.export_data('ic86_effective_area.csv')
    
    # Example 4: Plot (if matplotlib is available)
    print("\n4. Generating Plot:")
    print("-" * 60)
    try:
        ic86.plot_effective_area('ic86_effective_area.png')
        print("  Plot generated successfully!")
    except Exception as e:
        print(f"  Could not generate plot: {e}")
    
    print("\n" + "=" * 60)
    print("完成！可以使用这些数据计算中微子探测率。")
    print("Completed! You can use this data to calculate neutrino detection rates.")
    print("=" * 60)


if __name__ == '__main__':
    main()
