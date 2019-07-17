from sciQt.tools import Q_

def parse_units(text, base_unit='s'):
    ''' Parses text of the form "<magnitude> <unit>" and returns the magnitude
        in units of the specified base unit, as well as the text in compact form.
        For example, if the base unit is "s", then an input of "0.5 ms" will
        return a magnitude 5e-4 and a string "500 us".
    '''
    duration = Q_(text)
    if str(duration.units) == 'dimensionless':
        duration = Q_('{} {}'.format(duration.magnitude, base_unit))    # assume base unit if none is passed
    cleaned_value = duration.to_compact()                   # auto-convert units for compact view
    cleaned_value = '{:~}'.format(cleaned_value)
    duration.ito_base_units()

    return duration.magnitude, cleaned_value
