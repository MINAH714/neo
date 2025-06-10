from pathlib import Path

def create_file(name:str, content:str):
    """ Create a file with the given name and content."""
    dest_path = Path(name)
    if dest_path.exists():
        return "Error : file already exists"
    try:
        dest_path.write_text(content, encoding='utf-8')
    except Exception as e:
        return f"Error : {exc!r}"
    return f"File created ."