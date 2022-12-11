import re

RE_NATNUMS = re.compile(r'(?P<int>\d+)')


def natnums(s):
    """
    >>> natnums("foo divisible by 3 and 2")
    [3, 2]
    """
    return [int(x) for x in RE_NATNUMS.findall(s)]


def items_from_template_from_lines(template, lines):
    # + 1 to count the last line of the template
    # + 1 to count a record separator line in the input
    chunksize = template.count('\n') + 2
    re_template = re.compile(template)
    for start in range(0, len(lines), chunksize):
        text = '\n'.join(lines[start:start + chunksize])
        yield re_template.match(text)
