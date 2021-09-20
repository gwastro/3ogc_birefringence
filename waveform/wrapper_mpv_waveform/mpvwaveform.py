import numpy

def integrand_parityamu_mpvinverse(redshift):
    """
    The integrand:
    (1.0 + z)^parity_beta / sqrt(Omega_m (1+z)^3 + Omega_Lambda)
    """
    omega_m = 0.3075 #pycbc.cosmology.get_cosmology().Om0 # matter density
    omega_l = 0.6910098821161554 #pycbc.cosmology.get_cosmology().Ode0 # dark energy density

    return (1.0+redshift)/ numpy.sqrt(omega_m*(1.0+redshift)**3.0 + omega_l)


def gen(**kwds):
    from pycbc.waveform import get_fd_waveform
    from pycbc import cosmology
    import lal
    from scipy import integrate
    #print(kwds)

    if 'approximant' in kwds:
        kwds.pop("approximant")
    if kwds['baseapprox'] is None:
        raise ValueError("A base waveform approximant is required.")

    hp, hc = get_fd_waveform(approximant=kwds['baseapprox'], **kwds)
    zz = cosmology.redshift(kwds['distance'])
    intz = integrate.quad(integrand_parityamu_mpvinverse, 0, zz)[0]
    temp =  kwds['parity_mpvinverse'] * intz / 1e9 / lal.QE_SI * lal.H_SI * lal.PI * lal.PI / lal.H0_SI

    hp_parity = hp + hc * temp * hp.sample_frequencies **2
    hc_parity = hc - hp * temp * hp.sample_frequencies **2

    return hp_parity, hc_parity
