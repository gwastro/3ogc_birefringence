def gen(**kwds):
    from pycbc.waveform import get_fd_waveform
    import lal
    #print(kwds)

    if 'approximant' in kwds:
        kwds.pop("approximant")
    hp, hc = get_fd_waveform(approximant="IMRPhenomXPHM", **kwds)

    temp =  kwds['parity_amu'] / 1e9 / lal.QE_SI * lal.H_SI * lal.PI * lal.PI / lal.H0_SI

    hp_parity = hp + hc * temp * hp.sample_frequencies **2
    hc_parity = hc - hp * temp * hp.sample_frequencies **2

    return hp_parity, hc_parity


#pycbc.waveform.add_custom_waveform('IMRPhenomParity', IMRPhenomParity, 'frequency', force=True)

def add_me(**kwds):
    kwds['cpu_fd']['IMRPhenomXPHMParity'] = gen
    kwds['filter_time_lengths']['IMRPhenomXPHMParity'] = kwds['filter_time_lengths']['IMRPhenomXPHM']

