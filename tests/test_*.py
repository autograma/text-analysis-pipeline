def test_path(path)
    if not path.exists():
        raise FileNotFoundError(f"File was not found: {path}")
