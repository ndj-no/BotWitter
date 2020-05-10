allow_debug = True


def debug(message='', value=''):
    if allow_debug:
        print(message + ':', value)


def debug_print_content(content=''):
    if allow_debug:
        print(content)
