from pathlib import Path
def get_file_extension(filename):
    """Get the file extension"""
    return Path(filename).suffix.lower()


def is_valid_document(filename):
    """Check if the file is valid, vaild files(PDF,TXT,MD,CSV)"""
    vaild_extensions = [".pdf",".txt",".md",".csv"]
    return get_file_extension(filename=filename) in vaild_extensions


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent security issues."""
    # Remove path traversal attempts
    filename = Path(filename).name
    # Remove special characters except dots and underscores
    return "".join(c for c in filename if c.isalnum() or c in '._- ')