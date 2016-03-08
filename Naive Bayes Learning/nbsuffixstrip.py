import re


def measure_of_word(string):
    count = -1
    prev_vowel = -1
    eli = 0
    for x in string:
        if re.search('[^aeiou]', x):
            eli = eli + 1
        else:
            break
    if eli > 0:
        string = string[eli:]
    eli = 0
    for x in range(len(string)):
        if re.search('[aeiou]|.*[^aeiou]y\b', string[len(string) - x - 1]):
            eli = eli - 1
        else:
            break
    if eli < 0:
        string = string[:eli]

    for x in range(len(string)):
        regex = re.search(r'([aeiou])',string[x])
        if regex:
            if prev_vowel == -1 or prev_vowel != x-1:
                count = count + 1
            prev_vowel = x
    if len(string) == 0:
        count = 0
    return count


def step1a(string):

    new_string = string
    if re.search(r'(.*sses\b|.*ies\b)', string):
        new_string = string[:-2]

    elif re.search(r'(.*ss\b)', string):
        new_string = string

    elif re.search(r'(.*s\b)', string):
        new_string = string[:-1]

    return new_string


def step1b(m, string):
    success = False
    new_string = string
    if re.search(r'(.*eed\b)', new_string):
        if m > 0:
            new_string = new_string[:-1]
    elif re.search(r'(.*[aeiou].*ed\b)', new_string):
        new_string = new_string[:-2]
        success = True
    elif re.search(r'(.*[aeiou].*ing\b)', new_string):
        new_string = new_string[:-3]
        success = True
    if success:
        if re.search(r'(.*at\b|.*bl\b|.*iz\b)', new_string):
            new_string = new_string + 'e'
        elif new_string[len(new_string) - 1] == new_string[len(new_string) - 2] \
                and (re.search(r'[^lsz]', new_string[len(new_string) - 1])):
            new_string = new_string[:-1]
        elif m == 1 and re.search(r'(.*[^aeiou][aeiou][^aeiouwxy]\b)', new_string):
            new_string = new_string + "e"

    return new_string


def step1c(string):
    new_string = string
    if re.search(r'(.*[aeiou].*y\b)', new_string):
        new_string = new_string[:-1] + 'i'

    return new_string


def step2(m, string):
    new_string = string
    if m > 0:
        if re.search(r'.*ational\b', new_string):
            new_string = new_string[:-6] + "te"

        elif re.search(r'.*ization\b', new_string):
            new_string = new_string[:-5] + "e"

        elif re.search(r'.*biliti\b', new_string):
            new_string = new_string[:-5] + "le"

        elif re.search(r'.*iveness\b|.*fulness\b|.*ousness\b', new_string):
            new_string = new_string[:-4]

        elif re.search(r'.*ation\b', new_string):
            new_string = new_string[:-4] + "te"

        elif re.search(r'.*iviti\b', new_string):
            new_string = new_string[:-3] + "e"

        elif re.search(r'.*alism\b|.*aliti\b', new_string):
            new_string = new_string[:-3]

        elif re.search(r'.*ator\b', new_string):
            new_string = new_string[:-2] + "e"

        elif re.search(r'.*tional\b|.*alli\b|.*entli\b|.*eli\b|.*ousli\b', new_string):
            new_string = new_string[:-2]

        elif re.search(r'.*enci\b|.*anci|.*abli\b', new_string):
            new_string = new_string[:-1] + "e"

        elif re.search(r'.*izer\b', new_string):
            new_string = new_string[:-1]

    return new_string


def step3(m, string):
    new_string = string
    if m > 0:
        if re.search(r'.*icate\b', new_string):
            new_string = new_string[:-3]

        elif re.search(r'.*ative\b', new_string):
            new_string = new_string[:-5]

        elif re.search(r'.*alize\b|.*iciti\b', new_string):
            new_string = new_string[:-3]

        elif re.search(r'.*ical\b', new_string):
            new_string = new_string[:-2]

        elif re.search(r'.*ful\b', new_string):
            new_string = new_string[:-3]

        elif re.search(r'.*ness\b', new_string):
            new_string = new_string[:-4]

    return new_string


def step4(m, string):
    new_string = string
    if m > 1:
        if re.search(r'.*al\b', new_string):
            new_string = new_string[:-2]

        elif re.search(r'.*ance\b', new_string):
            new_string = new_string[:-4]

        elif re.search(r'.*ence\b', new_string):
            new_string = new_string[:-4]

        elif re.search(r'.*er\b', new_string):
            new_string = new_string[:-2]

        elif re.search(r'.*ic\b', new_string):
            new_string = new_string[:-2]

        elif re.search(r'.*able\b', new_string):
            new_string = new_string[:-4]

        elif re.search(r'.*ible\b', new_string):
            new_string = new_string[:-4]

        elif re.search(r'.*ant\b', new_string):
            new_string = new_string[:-3]

        elif re.search(r'.*ement\b', new_string):
            new_string = new_string[:-5]

        elif re.search(r'.*ment\b', new_string):
            new_string = new_string[:-4]

        elif re.search(r'.*ent\b', new_string):
            new_string = new_string[:-3]

        elif re.search(r'.*[st]ion\b', new_string):
            new_string = new_string[:-3]

        elif re.search(r'.*ou\b', new_string):
            new_string = new_string[:-2]

        elif re.search(r'.*ism\b', new_string):
            new_string = new_string[:-3]

        elif re.search(r'.*ate\b', new_string):
            new_string = new_string[:-3]

        elif re.search(r'.*iti\b', new_string):
            new_string = new_string[:-3]

        elif re.search(r'.*ous\b', new_string):
            new_string = new_string[:-3]

        elif re.search(r'.*ive\b', new_string):
            new_string = new_string[:-3]

        elif re.search(r'.*ize\b', new_string):
            new_string = new_string[:-3]
    return new_string


def step5a(m, string):
    new_string = string
    if m > 1:
        if re.search(r'(.*e\b)', new_string):
            new_string = new_string[:-1]
    elif m == 1 and re.search(r'(.*[aeiou][^aeiou][aeiouwxy]e\b)', new_string):
            new_string = new_string
    return new_string


def step5b(m, string):
    new_string = string
    if m > 1 and len(new_string) > 0 and new_string[len(new_string) - 1] == "l" \
        and new_string[len(new_string) - 1] == new_string[len(new_string) - 2]:
        new_string = new_string[:-1]
    return new_string


def suffix_strip(string):
    new_string = ''.join(e for e in string if e.isalnum())
    m = measure_of_word(new_string)

    new_string = step1a(new_string)
    new_string = step1b(m, new_string)
    new_string = step1c(new_string)
    new_string = step2(m, new_string)
    new_string = step3(m, new_string)
    # new_string = step4(m, new_string)
    # new_string = step5a(m, new_string)
    # new_string = step5b(m, new_string)
    return new_string

