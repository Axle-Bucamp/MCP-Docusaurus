import os
from pathlib import Path
from typing import Dict, List, Union

DOCS_DIR = Path("/app/docs")


def generate() -> Dict[str, Union[str, List[dict]]]:
    """
    Generate a hierarchical site map of the Docusaurus documentation.

    Returns:
        dict: A tree-like representation of folders and markdown files.
    """
    def build_tree(directory: Path) -> List[dict]:
        tree = []
        for item in sorted(directory.iterdir()):
            if item.is_dir():
                tree.append({
                    "type": "folder",
                    "name": item.name,
                    "children": build_tree(item)
                })
            elif item.suffix == ".md":
                tree.append({
                    "type": "file",
                    "name": item.name,
                    "path": str(item.relative_to(DOCS_DIR))
                })
        return tree

    return {
        "root": str(DOCS_DIR),
        "structure": build_tree(DOCS_DIR)
    }