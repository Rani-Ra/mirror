"""
AGN-GRB Distribution Analysis Module

This module provides tools to calculate the distribution of Gamma-Ray Bursts (GRBs)
in Active Galactic Nuclei (AGN) and their contribution to the neutrino background.

The framework considers:
1. AGN mass function: distribution of supermassive black hole (SMBH) masses
2. AGN redshift evolution: how AGN population changes with cosmic time
3. GRB occurrence rate in AGN: probability of GRBs in different AGN environments
4. Combined distribution for neutrino background calculations

References:
- AGN luminosity function: Hopkins et al. (2007)
- SMBH mass function: Shankar et al. (2009)
- GRB-AGN connection: Perna et al. (2021)
"""

import numpy as np
from scipy import integrate, interpolate
from scipy.special import erf


class AGNMassFunction:
    """
    AGN supermassive black hole mass function.
    
    Based on observational constraints from Shankar et al. (2009) and 
    subsequent works. Provides the number density of AGN as a function
    of black hole mass and redshift.
    """
    
    def __init__(self):
        """Initialize AGN mass function parameters."""
        # Schechter function parameters (approximate values for z~0-3)
        self.phi_star = 1e-5  # Mpc^-3 dex^-1, normalization
        self.M_star = 1e8  # M_sun, characteristic mass
        self.alpha = -0.5  # faint-end slope
        self.beta = -2.5   # bright-end slope
        
    def schechter_function(self, M_bh, z=0):
        """
        Double power-law Schechter function for SMBH mass distribution.
        
        Parameters:
        -----------
        M_bh : float or array
            Black hole mass in solar masses
        z : float or array
            Redshift
            
        Returns:
        --------
        phi : float or array
            Number density in Mpc^-3 dex^-1
        """
        # Redshift evolution of characteristic mass
        M_star_z = self.M_star * (1 + z)**0.5
        
        # Redshift evolution of normalization
        phi_star_z = self.phi_star * (1 + z)**1.5 * np.exp(-z/2.0)
        
        x = M_bh / M_star_z
        
        # Double power-law form
        phi = phi_star_z / (x**(-self.alpha) + x**(-self.beta))
        
        return phi
    
    def dn_dlogM_dVc(self, M_bh, z):
        """
        Comoving number density per log mass interval.
        
        Parameters:
        -----------
        M_bh : float or array
            Black hole mass in solar masses
        z : float or array
            Redshift
            
        Returns:
        --------
        float or array
            dn/d(logM)/dVc in Mpc^-3
        """
        return self.schechter_function(M_bh, z) * np.log(10)
    

class AGNRedshiftEvolution:
    """
    AGN redshift evolution and cosmological calculations.
    
    Provides tools to convert between redshift and comoving volume,
    and to calculate AGN number density evolution.
    """
    
    def __init__(self, H0=70.0, Om0=0.3, OL0=0.7):
        """
        Initialize cosmological parameters.
        
        Parameters:
        -----------
        H0 : float
            Hubble constant in km/s/Mpc
        Om0 : float
            Matter density parameter
        OL0 : float
            Dark energy density parameter
        """
        self.H0 = H0
        self.Om0 = Om0
        self.OL0 = OL0
        self.c = 2.998e5  # speed of light in km/s
        
    def E(self, z):
        """Dimensionless Hubble parameter."""
        return np.sqrt(self.Om0 * (1+z)**3 + self.OL0)
    
    def comoving_distance(self, z):
        """
        Comoving distance in Mpc.
        
        Parameters:
        -----------
        z : float
            Redshift
            
        Returns:
        --------
        float
            Comoving distance in Mpc
        """
        if np.isscalar(z):
            result, _ = integrate.quad(lambda zp: 1/self.E(zp), 0, z)
        else:
            result = np.array([integrate.quad(lambda zp: 1/self.E(zp), 0, zi)[0] 
                             for zi in z])
        return (self.c / self.H0) * result
    
    def comoving_volume(self, z):
        """
        Comoving volume element dV/dz in Mpc^3.
        
        Parameters:
        -----------
        z : float or array
            Redshift
            
        Returns:
        --------
        float or array
            dV/dz in Mpc^3
        """
        dc = self.comoving_distance(z)
        dVdz = 4 * np.pi * dc**2 * (self.c / self.H0) / self.E(z)
        return dVdz
    

class GRBDistributionInAGN:
    """
    GRB occurrence rate distribution within AGN.
    
    Models the rate at which GRBs occur in AGN environments as a function
    of AGN properties (black hole mass, accretion rate) and position within
    the AGN disk.
    """
    
    def __init__(self):
        """Initialize GRB-AGN model parameters."""
        # GRB rate normalization
        self.R_GRB_norm = 1e-3  # per AGN per year
        
        # Dependence on black hole mass
        self.mass_index = 0.5  # R_GRB ~ M_bh^mass_index
        self.M_ref = 1e8  # reference mass in M_sun
        
        # Radial distribution in AGN disk (semi-major axis)
        self.a_min = 1e2  # minimum semi-major axis in gravitational radii
        self.a_max = 1e4  # maximum semi-major axis in gravitational radii
        
    def grb_rate_per_agn(self, M_bh):
        """
        GRB rate per individual AGN.
        
        Parameters:
        -----------
        M_bh : float or array
            Black hole mass in solar masses
            
        Returns:
        --------
        float or array
            GRB rate in yr^-1
        """
        rate = self.R_GRB_norm * (M_bh / self.M_ref)**self.mass_index
        return rate
    
    def radial_distribution(self, a, M_bh):
        """
        Probability distribution of GRB position in AGN disk.
        
        Uses a log-normal distribution centered at intermediate radii.
        
        Parameters:
        -----------
        a : float or array
            Semi-major axis in gravitational radii (r_g = GM/c^2)
        M_bh : float
            Black hole mass in solar masses
            
        Returns:
        --------
        float or array
            Probability density (normalized)
        """
        # Log-normal distribution
        log_a = np.log10(a)
        mu = 0.5 * (np.log10(self.a_min) + np.log10(self.a_max))
        sigma = 0.5 * (np.log10(self.a_max) - np.log10(self.a_min)) / 2.355
        
        prob = (1.0 / (np.sqrt(2*np.pi) * sigma)) * \
               np.exp(-(log_a - mu)**2 / (2 * sigma**2))
        
        # Normalize
        norm, _ = integrate.quad(lambda log_a_val: 
            (1.0 / (np.sqrt(2*np.pi) * sigma)) * 
            np.exp(-(log_a_val - mu)**2 / (2 * sigma**2)),
            np.log10(self.a_min), np.log10(self.a_max))
        
        return prob / norm
    

class AGNGRBPopulation:
    """
    Combined AGN-GRB population model.
    
    Integrates AGN mass function, redshift evolution, and GRB occurrence
    to calculate the total GRB rate in AGN across cosmic time.
    """
    
    def __init__(self):
        """Initialize population model."""
        self.agn_mf = AGNMassFunction()
        self.agn_z = AGNRedshiftEvolution()
        self.grb_dist = GRBDistributionInAGN()
        
    def grb_rate_density(self, M_bh, z):
        """
        GRB rate density in comoving volume.
        
        Parameters:
        -----------
        M_bh : float or array
            Black hole mass in solar masses
        z : float
            Redshift
            
        Returns:
        --------
        float or array
            dR/dV/dlogM in Mpc^-3 yr^-1
        """
        # AGN number density
        n_agn = self.agn_mf.dn_dlogM_dVc(M_bh, z)
        
        # GRB rate per AGN
        R_grb = self.grb_dist.grb_rate_per_agn(M_bh)
        
        return n_agn * R_grb
    
    def total_grb_rate_at_z(self, z, M_min=1e6, M_max=1e10):
        """
        Total GRB rate at a given redshift.
        
        Parameters:
        -----------
        z : float
            Redshift
        M_min, M_max : float
            Black hole mass range in solar masses
            
        Returns:
        --------
        float
            Total GRB rate in Mpc^-3 yr^-1
        """
        def integrand(log_M):
            M = 10**log_M
            return self.grb_rate_density(M, z)
        
        result, _ = integrate.quad(integrand, np.log10(M_min), np.log10(M_max))
        return result
    
    def cumulative_grb_rate(self, z_max, M_min=1e6, M_max=1e10, z_bins=50):
        """
        Cumulative GRB rate up to redshift z_max.
        
        Parameters:
        -----------
        z_max : float
            Maximum redshift
        M_min, M_max : float
            Black hole mass range in solar masses
        z_bins : int
            Number of redshift bins for integration
            
        Returns:
        --------
        float
            Total GRB rate in yr^-1 (integrated over volume)
        """
        z_array = np.linspace(0, z_max, z_bins)
        rates = []
        
        for z in z_array:
            dV_dz = self.agn_z.comoving_volume(z)
            rate_density = self.total_grb_rate_at_z(z, M_min, M_max)
            rates.append(rate_density * dV_dz)
        
        # Integrate over redshift
        total_rate = integrate.trapezoid(rates, z_array)
        return total_rate
    

class NeutrinoBackgroundCalculator:
    """
    Calculate neutrino background from AGN-GRB population.
    
    This class combines the AGN-GRB population model with neutrino
    emission properties to calculate the contribution to the diffuse
    neutrino background.
    """
    
    def __init__(self, population_model=None):
        """
        Initialize calculator.
        
        Parameters:
        -----------
        population_model : AGNGRBPopulation, optional
            Population model instance. Creates new one if None.
        """
        if population_model is None:
            self.population = AGNGRBPopulation()
        else:
            self.population = population_model
            
        # Neutrino emission properties (to be set by user)
        self.neutrino_energy = None  # Energy in GeV
        self.neutrino_luminosity_function = None  # Function of (M_bh, a, z)
        
    def set_neutrino_emission_model(self, luminosity_func):
        """
        Set neutrino emission model.
        
        Parameters:
        -----------
        luminosity_func : callable
            Function that takes (M_bh, a, z) and returns neutrino
            luminosity in erg/s
        """
        self.neutrino_luminosity_function = luminosity_func
    
    def neutrino_flux_contribution(self, E_nu, z_max=3.0, 
                                  M_min=1e6, M_max=1e10):
        """
        Calculate neutrino flux contribution.
        
        Parameters:
        -----------
        E_nu : float
            Neutrino energy in GeV
        z_max : float
            Maximum redshift to integrate
        M_min, M_max : float
            Black hole mass range
            
        Returns:
        --------
        float
            Neutrino flux in GeV^-1 cm^-2 s^-1 sr^-1
        """
        if self.neutrino_luminosity_function is None:
            raise ValueError("Neutrino emission model not set. "
                           "Call set_neutrino_emission_model first.")
        
        # This is a placeholder for the full calculation
        # User should implement based on their specific neutrino model
        
        # Basic structure:
        # 1. Integrate over redshift
        # 2. For each z, integrate over M_bh
        # 3. For each M_bh, integrate over disk position a
        # 4. Weight by AGN-GRB population density
        # 5. Account for cosmological effects
        
        flux = 0.0
        # ... (implementation depends on specific neutrino model)
        
        return flux
    

def example_usage():
    """
    Example usage of the AGN-GRB distribution framework.
    """
    print("AGN-GRB Distribution Analysis Example")
    print("=" * 50)
    
    # Initialize population model
    pop = AGNGRBPopulation()
    
    # Example 1: AGN mass function at different redshifts
    print("\n1. AGN Mass Function")
    M_bh_array = np.logspace(6, 10, 50)  # 10^6 to 10^10 M_sun
    
    for z in [0.0, 1.0, 2.0]:
        phi = pop.agn_mf.dn_dlogM_dVc(M_bh_array, z)
        total_density = integrate.trapezoid(phi, np.log10(M_bh_array))
        print(f"z = {z}: Total AGN density = {total_density:.2e} Mpc^-3")
    
    # Example 2: GRB rate as function of black hole mass
    print("\n2. GRB Rate vs Black Hole Mass")
    for M_bh in [1e7, 1e8, 1e9]:
        rate = pop.grb_dist.grb_rate_per_agn(M_bh)
        print(f"M_BH = {M_bh:.1e} M_sun: R_GRB = {rate:.2e} yr^-1")
    
    # Example 3: Total GRB rate density at different redshifts
    print("\n3. GRB Rate Density vs Redshift")
    for z in [0.0, 0.5, 1.0, 1.5, 2.0]:
        rate_density = pop.total_grb_rate_at_z(z)
        print(f"z = {z}: R_GRB = {rate_density:.2e} Mpc^-3 yr^-1")
    
    # Example 4: Cumulative GRB rate
    print("\n4. Cumulative GRB Rate")
    z_max = 3.0
    total_rate = pop.cumulative_grb_rate(z_max, z_bins=30)
    print(f"Total GRB rate (z < {z_max}): {total_rate:.2e} yr^-1")
    
    print("\n" + "=" * 50)
    print("Analysis complete!")


if __name__ == "__main__":
    example_usage()
