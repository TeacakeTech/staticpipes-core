def does_filename_have_extension(filename: str, extensions: list) -> bool:
    fn = filename.lower()
    for extension in extensions:
        if fn.endswith("." + extension.lower()):
            return True
    return False


def make_path_from_dir_and_filename(dir: str, filename: str) -> str:
    return (
        ("" if dir == "" or dir == "/" else (dir if dir.startswith("/") else "/" + dir))
        + "/"
        + filename
    )


def make_dir_and_filename_from_path(path: str):
    bits = path.split("/")
    filename = bits.pop()
    dir = "/".join(bits)
    if not dir.startswith("/") and dir:
        dir = "/" + dir
    return dir, filename
