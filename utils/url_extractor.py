from urlextract import URLExtract

def is_url(string: str) -> bool:
    url_extract = URLExtract()

    if url_extract.find_urls(string):
        return True

    return False
