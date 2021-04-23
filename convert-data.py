@outputSchema('vals: {(val:chararray)}')
def convert(the_input):
    # This converts the indeterminate number of vals into a bag.
    out = []
    for map in the_input:
        out.append(map)
    return out
