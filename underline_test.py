
#function to help underline what i need later on
def underline(string):
    emptystring = ''

    for i in range(0, len(string)):

        if string[i] == ' ':
            emptystring = emptystring + string[i]
        else:
            emptystring= emptystring+string[i]+str('\u0332')

    return emptystring


