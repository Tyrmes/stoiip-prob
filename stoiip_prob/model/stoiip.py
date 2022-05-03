def stoiip(area, h, poro, swc, boi):
    """
    Volume of Oil in Place, stb

    Parameters
    ----------
    area
        Area, acre
    h
        reservoir thickness, ft
    poro
        rock porosity, fraction
    swc
        connate water saturation, fraction
    boi
        oil formation volume factor, rb/stb

    Returns
    -------
    float with stoiip value

    """

    return 7758 * area * h * poro * (1-swc) / boi
