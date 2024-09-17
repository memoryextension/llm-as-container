from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from transformers import set_seed

# Load the model using FastAPI lifespan event so that the model is loaded at the beginning for efficiency
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model from HuggingFace transformers library
    from transformers import pipeline
    global generator
    generator = pipeline('text-generation', model='distilgpt2',clean_up_tokenization_spaces=False)
    yield
    # Clean up the model and release the resources
    del generator

# Initialize the FastAPI app
app = FastAPI(lifespan=lifespan)

@app.get('/')
async def welcome():
    return "Text Gen v 1.0.1"

class TextGen(BaseModel):
    text: str
    seed: int = 42
    nb_tokens: int = 50
    nb_sequences: int = 1


@app.post('/textgen')
@app.post('/tg')
async def generate_text(tg: TextGen):
    print(tg)    
    set_seed(tg.seed)
    a=generator(tg.text, 
                max_length=tg.nb_tokens,
                num_return_sequences=tg.nb_sequences,
                truncation=True,pad_token_id=generator.tokenizer.eos_token_id)
    print(a)
    return a
