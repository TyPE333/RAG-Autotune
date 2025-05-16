from typing import List, Tuple, Dict
from torch.utils.data import Dataset
from transformers import PreTrainedTokenizer


class DualEncoderDataset(Dataset):
    def __init__(
        self,
        query_doc_pairs: List[Tuple[str, str]],
        tokenizer: PreTrainedTokenizer,
        max_length: int = 128,
    ):
        self.pairs = query_doc_pairs
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx: int) -> Dict[str, Dict[str, List[int]]]:
        query, doc = self.pairs[idx]

        query_enc = self.tokenizer(
            query,
            padding="max_length",
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt",
        )

        doc_enc = self.tokenizer(
            doc,
            padding="max_length",
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt",
        )

        return {
            "query_input": {k: v.squeeze(0) for k, v in query_enc.items()},
            "doc_input": {k: v.squeeze(0) for k, v in doc_enc.items()},
        }
