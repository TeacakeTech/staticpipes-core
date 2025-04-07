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


def is_directory_in_list(check_dir: str, directories: list) -> bool:
    """Returns bool True if directory is in list
    or is a child of any directory in the list."""
    # Easy check - is just everything included?
    if "/" in directories:
        return True
    # Ok, we need to check more
    for in_dir in directories:
        in_dir_bits = (in_dir if in_dir.startswith("/") else "/" + in_dir).split("/")
        check_dir_bits = (
            check_dir if check_dir.startswith("/") else "/" + check_dir
        ).split("/")
        check_dir_bits = check_dir_bits[: len(in_dir_bits)]
        if check_dir_bits == in_dir_bits:
            return True
    # No
    return False
