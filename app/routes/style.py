from fastapi import HTTPException

# Define some basic styles as examples
STYLE_MAP = {
    "bold_headers": lambda content: content.replace("# ", "# **").replace("\n", "**\n"),
    "add_spacing": lambda content: content.replace("\n", "\n\n"),
    "remove_comments": lambda content: "\n".join(
        [line for line in content.splitlines() if not line.strip().startswith("<!--")]
    ),
}


def transform(style_id: str, content: str) -> dict:
    """
    Apply a specific style transformation to the document content.

    Args:
        style_id (str): The ID of the style to apply.
        content (str): The markdown content to transform.

    Returns:
        dict: The transformed content.
    """
    if style_id not in STYLE_MAP:
        raise HTTPException(status_code=400, detail=f"Style '{style_id}' not supported")

    transformed = STYLE_MAP[style_id](content)
    return {
        "style": style_id,
        "transformed": transformed
    }