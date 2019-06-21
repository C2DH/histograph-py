from unicodedata import normalize

def to_slug(text):
    clean_text = text.strip().replace(' ', '-')
    while '--' in clean_text:
        clean_text = clean_text.replace('--', '-')
    ascii_text = normalize('NFKD', clean_text).encode('utf-8', 'ignore')
    return ascii_text.lower().decode("utf-8")
