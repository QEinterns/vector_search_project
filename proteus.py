from diffusers import DiffusionPipeline
import torch,logging

def proteus(enhanced_query,file_name):

    pipe = DiffusionPipeline.from_pretrained("dataautogpt3/ProteusV0.2")
    pipe = pipe.to("mps")

    # Recommended if your computer has < 64 GB of RAM
    pipe.enable_attention_slicing()

    # prompt = "In 'Top Gun Maverick,' Tom Cruise's Maverick engages in a thrilling aerial duel, his determined face visible inside the cockpit amidst rugged canyons and vast skies."

    image = pipe(enhanced_query).images[0]
    # movie_name = movie_name + 'proteus12'
    return image.save(f"static/output/{file_name}.png")
