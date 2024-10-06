import json
from typing import Generator, Optional
from urllib.parse import urljoin

import requests
from ktem.reasoning.base import BaseReasoning
from ktem.utils.render import Render

from kotaemon.base import BaseComponent, Document, RetrievedDocument


class AutoRAGPipeline(BaseReasoning):
    class Config:
        allow_extra = True

    url: str = "http://localhost:8000"

    @classmethod
    def get_pipeline(
        cls,
        user_settings: dict,
        state: dict,
        retrievers: Optional[list[BaseComponent]] = None,
    ) -> "BaseReasoning":
        url = user_settings.get("autorag_url", "http://localhost:8000")

        pipeline = cls(url=url)
        return pipeline

    @classmethod
    def get_user_settings(cls) -> dict:
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
            }
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
        json_data: dict,
    ) -> tuple[list[RetrievedDocument], list[Document]]:
        retrieved_passages = json_data["retrieved_passage"]

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
                retrieved_passages,
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
                            # Decode the chunk and print it
                            data = json.loads(chunk.decode("utf-8"))
                            if i == 0:
                                docs, info = self.make_retrieve_docs(data)
                                yield from info
                            else:
                                yield Document(content=data["result"], channel="chat")

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
