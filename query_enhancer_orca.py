
from gpt4all import GPT4All

def query_enhancer_orca(context,query):
    model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
    system_template = 'You are a query enhancer that expands the query with more of scene setting words in a way that can be depicted in an image by a text-to-image model using the plot as context fed to you by the user.'
    with model.chat_session(system_template):
        output = model.generate(f"Plot:{context}  Query: {query}.")
        print(output)
        return output