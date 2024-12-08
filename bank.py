
import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import PromptTemplate
from llama_index.core import Settings
import gradio as gr

# Local embedding model setup
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# Load documents from the specified directory
document = SimpleDirectoryReader("C:/Users/sachit.kaundal/Desktop/Graq/content/tsb").load_data()

# Set up the LLM model
llm = HuggingFaceLLM(
    tokenizer_name="tiiuae/falcon-7b-instruct",
    model_name="tiiuae/falcon-7b-instruct",
    device_map="auto"
)

# Create the index with the embedding model and LLM explicitly passed
index = VectorStoreIndex.from_documents(
    document,
    embed_model=Settings.embed_model,
    llm=llm  # Explicitly pass the LLM
)

# Persist the index storage context
index.storage_context.persist(persist_dir="./embeddings")

# System prompt setup
SYSTEM_PROMPT = """You are an AI assistant that answers questions in a friendly manner, based on the given source documents. Here are some rules you always follow:
- Generate human readable output, avoid creating output with gibberish text.
- Generate only the requested output, don't include any other language before or after the requested output.
- Never say thank you, that you are happy to help, that you are an AI agent, etc. Just answer directly.
- Generate professional language typically used in business documents in North America.
- Never generate offensive or foul language.
"""
query_wrapper_prompt = PromptTemplate(
    "[INST]<<SYS>>\n" + SYSTEM_PROMPT + "<</SYS>>\n\n{query_str}[/INST]"
)

# Load the chat engine with the persisted storage context and explicitly pass the LLM
storage_context = StorageContext.from_defaults(persist_dir="./embeddings")
index = load_index_from_storage(storage_context)
chat_engine = index.as_chat_engine(
    chat_mode="condense_question",
    llm=llm,  # Explicitly pass the LLM
    context_window = 2048,
    verbose=True
)

# Set up the Gradio UI
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        response = chat_engine.chat(message)
        bot_message = response.response
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch()
