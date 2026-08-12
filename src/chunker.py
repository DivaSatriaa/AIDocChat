import re


def chunk_text(
    text,
    chunk_size=1500,
    overlap=300
):
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        if (
            len(current_chunk)
            + len(sentence)
            + 1
            <= chunk_size
        ):

            if current_chunk:
                current_chunk += " "

            current_chunk += sentence

        else:

            if current_chunk.strip():
                chunks.append(
                    current_chunk.strip()
                )

            overlap_text = (
                current_chunk[-overlap:]
            )

            if " " in overlap_text:
                overlap_text = (
                    overlap_text[
                        overlap_text.find(" ") + 1:
                    ]
                )

            current_chunk = (
                overlap_text
                + " "
                + sentence
            )

    if current_chunk.strip():
        chunks.append(
            current_chunk.strip()
        )

    return chunks