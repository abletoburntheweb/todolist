def wrap_text(text, line_length):
    if len(text) <= line_length:
        return text
    wrapped_text = ''
    while text:
        if len(text) <= line_length:
            wrapped_text += text
            break
        else:
            space_index = text.rfind(' ', 0, line_length)
            newline_index = line_length if space_index == -1 else space_index
            wrapped_text += text[:newline_index].strip() + '\n'
            text = text[newline_index:].lstrip()
    return wrapped_text
