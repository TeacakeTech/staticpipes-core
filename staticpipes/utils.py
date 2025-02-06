def does_filename_have_extension(filename: str, extensions: list) -> bool:
    fn = filename.lower()
    for extension in extensions:
        if fn.endswith("." + extension.lower()):
            return True
    return False
