from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_into_documents(text):
    """
    Splits the input text into document objects.

    Args:
        text (str): The text to be split into documents.

    Returns:
        List[Document]: A list of document objects.
    """

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=50
    )
    doc_splits = text_splitter.create_documents([text])
    return doc_splits