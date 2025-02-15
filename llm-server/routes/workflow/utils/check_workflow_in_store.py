from typing import Any, Dict, Optional

from langchain.vectorstores.base import VectorStore
from langchain.docstore.document import Document
from opencopilot_utils import StoreOptions
from opencopilot_utils.get_vector_store import get_vector_store
import os
from utils import struct_log


def check_workflow_in_store(text: str, bot_id: str) -> Optional[Document]:
    try:
        vector_store = get_vector_store(StoreOptions("swagger"))
        score_threshold = float(os.getenv("SCORE_THRESHOLD", "0.91"))
        retriever = vector_store.as_retriever(
            search_kwargs={
                "k": 5,
                "score_threshold": score_threshold,
                "filter": {"bot_id": bot_id},
            },
        )

        result = retriever.get_relevant_documents(text)
        struct_log.info(
            event="check_workflow_in_store",
            result=result,
        )

        if len(result) > 0:
            result[0]

        return None

    except Exception as e:
        struct_log.exception(
            payload={"text": text, "bot_id": bot_id},
            error=str(e),
            event="/check_workflow_in_store",
        )
        return None
