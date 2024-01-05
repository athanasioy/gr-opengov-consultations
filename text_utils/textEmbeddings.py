from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


class GreekBERTEncoder:
    def __init__(self):
        MODEL_NAME = "nlpaueb/bert-base-greek-uncased-v1"
        self._tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self._model = AutoModel.from_pretrained(MODEL_NAME)

    def get_embedding(self, input_text:str) -> tuple[np.ndarray, int]:
        tokens = self._tokenizer(input_text, return_tensors="pt",truncation=True)

        tokens_original = self._tokenizer(input_text, return_tensors="pt")
        tokens_size = tokens_original['input_ids'].size(1)

        with torch.no_grad():
            output = self._model(**tokens)
        embeddings = output.last_hidden_state.mean(dim=1)
        
        return (embeddings.numpy(), tokens_size)
    
    def get_embeddings_batch(self, input_text:list[str]) -> tuple[list[np.ndarray], list[int]]:

        tokens = self._tokenizer(input_text, return_tensors="pt", truncation=True,padding=True)
        
        tokens_original = self._tokenizer(input_text, return_tensors="pt",padding=True)
        tokens_size = tokens_original['attention_mask'].sum(dim=1).tolist()
        with torch.no_grad():
            output = self._model(**tokens)
        
        embeddings = output.last_hidden_state.mean(1)
        embeddings = mean_pooling(output,tokens['attention_mask'])
        vectors = torch.split(embeddings,1,dim=0)
        embeddings_list = [v.squeeze().numpy() for v in vectors]
        
        return (embeddings_list,tokens_size)
    
class GreekLongFormerEncoder:
    
    def __init__(self) -> None:
        MODEL_NAME = "dimitriz/st-greek-media-longformer-4096"
        self._tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self._model = AutoModel.from_pretrained(MODEL_NAME)

    def get_embeddings_batch(self, input_text:list[str]) -> tuple[list[np.ndarray], list[int]]:
        tokens = self._tokenizer(input_text,padding=True,truncation=True,return_tensors="pt")
        tokens_original = self._tokenizer(input_text,padding=True,return_tensors="pt")
        tokens_size = tokens_original['attention_mask'].sum(dim=1).tolist()
        
        with torch.no_grad():
            output = self._model(**tokens)
            
        embeddings = mean_pooling(output,tokens['attention_mask'])
        vectors = torch.split(embeddings,1,dim=0)
        embeddings_list = [v.squeeze().numpy() for v in vectors]
        
        return (embeddings_list,tokens_size)