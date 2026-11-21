from functools import lru_cache
from transformers import AutoTokenizer,AutoModelForSeq2SeqLM
from app.services.rag_service import retrieve_retention_guidance
import torch

@lru_cache(maxsize=1)
def load_llm():
    checkpoint = 'google/flan-t5-base'
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
    model.eval()
    return tokenizer,model

def explain_churn(customer_details):
    query = f"""
    Find retention guidance relevant to this customer:
    {customer_details}
    """
    chunks=retrieve_retention_guidance(query)
    context = " ".join(chunks)
    prompt = f"""
        Answer the question using the following context.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    tokenizer,model = load_llm()
    input = tokenizer(prompt, return_tensors="pt",truncation=True)
    with torch.inference_mode():
        outputs = model.generate(input_ids=input['input_ids'])
    ans = tokenizer.decode(outputs[0],skip_special_tokens=True)

    return {
        "answer":ans,
        "retrieved_context":context,
    }