import json
from json import JSONDecoder
from typing import Generator
from urllib.parse import urljoin

import requests
from ktem.reasoning.base import BaseReasoning
from ktem.utils.render import Render

from kotaemon.base import Document, RetrievedDocument


def decode_multiple_json_from_bytes(byte_data: bytes) -> list:
    """
    Decode multiple JSON objects from bytes received from SSE server.

    Args:
            byte_data: Bytes containing one or more JSON objects

    Returns:
            List of decoded JSON objects
    """
    # Decode bytes to string
    try:
        text_data = byte_data.decode("utf-8").strip()
    except UnicodeDecodeError:
        raise ValueError("Invalid byte data: Unable to decode as UTF-8")

    # Initialize decoder and result list
    decoder = JSONDecoder()
    result = []

    # Keep track of position in string
    pos = 0
    text_data = text_data.strip()

    while pos < len(text_data):
        try:
            # Try to decode next JSON object
            json_obj, json_end = decoder.raw_decode(text_data[pos:])
            result.append(json_obj)

            # Move position to end of current JSON object
            pos += json_end

            # Skip any whitespace
            while pos < len(text_data) and text_data[pos].isspace():
                pos += 1

        except json.JSONDecodeError:
            # If we can't decode at current position, move forward one character
            pos += 1

    return result


class AutoRAGPipeline(BaseReasoning):
    class Config:
        allow_extra = True

    url: str = "http://localhost:8000"

    @classmethod
    def get_pipeline(
        cls,
        user_settings: dict,
        *args,
        **kwargs,
    ) -> "BaseReasoning":
        url = user_settings.get(
            "reasoning.options.autorag.autorag_url", "http://localhost:8000"
        )

        pipeline = cls(url=url)
        return pipeline

    @classmethod
    def get_user_settings(cls) -> dict:
        llm = ""
        choices = [("(default)", "")]
        return {
            "autorag_url": {
                "name": "AutoRAG API Endpoint URL",
                "value": "http://localhost:8000",
                "component": "text",
                "info": (
                    "AutoRAG API endpoint URL. "
                    "AutoRAG will find you the most optimal "
                    "RAG pipeline for your documents."
                ),
            },
            "llm": {
                "name": "Language model for make conversation title",
                "value": llm,
                "component": "dropdown",
                "choices": choices,
                "special_type": "llm",
                "info": (
                    "The language model to use for renaming conversation. "
                    "If you don't set this,"
                    "the application default language model will be used."
                ),
            },
        }

    @classmethod
    def get_info(cls) -> dict:
        return {
            "id": "autorag",
            "name": "AutoRAG",
            "description": (
                "Use AutoRAG backend. AutoRAG will find you the most "
                "optimal RAG pipeline for your documents."
            ),
        }

    @staticmethod
    def make_retrieve_docs(
        passages: list[dict],
    ) -> tuple[list[RetrievedDocument], list[Document]]:
        docs = list(
            map(
                lambda x: RetrievedDocument(
                    content=x["content"],
                    source=x["filepath"],
                    metadata={
                        "file_path": x["filepath"],
                        "file_page": x["file_page"],
                        "start_idx": x["start_idx"],
                        "end_idx": x["end_idx"],
                    },
                ),
                passages,
            )
        )

        info = [
            Document(
                channel="info",
                content=Render.collapsible_with_header(doc, open_collapsible=True),
            )
            for doc in docs
        ]

        return docs, info

    def stream(
        self, message: str, conv_id: str, history: list, **kwargs
    ) -> Generator[Document, None, Document]:
        body = {
            "query": message,
        }
        headers = {"Content-Type": "application/json"}

        with requests.Session() as session:
            try:
                # Make a POST request with streaming enabled
                response = session.post(
                    urljoin(self.url, "/v1/stream"),
                    json=body,
                    headers=headers,
                    stream=True,
                )

                # Check if the request was successful
                if response.status_code == 200:
                    # Process the streaming response
                    for i, chunk in enumerate(response.iter_content(chunk_size=None)):
                        if chunk:
                            data_list = decode_multiple_json_from_bytes(chunk)
                            # Decode the chunk and print it
                            passage_list = []
                            for data in data_list:
                                if data["type"] == "retrieved_passage":
                                    passage_list.append(data["retrieved_passage"])
                                    docs, info = self.make_retrieve_docs(passage_list)
                                    yield from info
                                else:
                                    yield Document(
                                        content=data["generated_text"], channel="chat"
                                    )

                    # yield from [
                    # 				Document(channel="info",
                    # 				content=Render.collapsible_with_header_score(
                    # 				doc)) for doc in docs
                    # 			]
                else:
                    print(f"Request failed with status code: {response.status_code}")
                    print(f"Response content: {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
