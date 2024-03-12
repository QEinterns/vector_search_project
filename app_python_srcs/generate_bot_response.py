from llama_cpp import Llama

def llm_container(context,query,history):
    if(len(context)>9600):
        context = context[:9500]
    llm = Llama(
        # model_path='/Users/nishanth/lora/TheBloke/mistral-7b-openorca.Q4_0.gguf',
        model_path='/Users/nishanth/lora/architect_chat_models/architect_model.gguf',
        n_ctx=10000,
    )
    output = llm(
        f"Q: Context:{context}. Conversation History: {history} .Query:{query} . You are a couchbase documentation chatbot, answer the given query based on the context provided to you by docs provided as context. Also use conversation history to keep track of the conversation. Answer in less than 50 word. A:", # Prompt
        max_tokens=None,
    )
    response_llm = str(output['choices'][0]['text'])
    
    return response_llm
