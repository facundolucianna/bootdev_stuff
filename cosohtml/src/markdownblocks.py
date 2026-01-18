def markdown_to_blocks(markdown: str) -> list[str]:
    markdown = markdown.strip()
    if markdown == "":
        raise ValueError("Markdown is empty")
    blocks = markdown.split("\n\n")
    blocks_clean = []
    for block in blocks:
        block_clean = block.strip()
        if block_clean == "":
            continue
        blocks_clean.append(block_clean)
    return blocks_clean
    