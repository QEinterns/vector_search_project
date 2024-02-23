from gpt4all import GPT4All

def query_enhancer_mistral(context,query):
    model = GPT4All("/Users/nishanth/Documents/movie_qe_proj/models/query_enhancer/mistral-7b-openorca.Q4_0.gguf")
    system_template = 'You are a query enhancer that expands the query with more of scene setting words in a way that can be depicted in an image by a text-to-image model using the plot as context fed to you by the user.'
    with model.chat_session(system_template):
        output = model.generate("Plot:{context} .Query:{query}")
        print(output)
        return output