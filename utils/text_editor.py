# region - Text Snippet
def snippet(text, count):
    words = text.split()
    snippet_words = words[:count]
    snippet_text = ' '.join(snippet_words)
    return snippet_text

# endregion
