from diffusers import DiffusionPipeline
import torch

def sdx(movie_name, enhanced_query):
    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0")
    pipe = pipe.to("mps")

    # Recommended if your computer has < 64 GB of RAM
    pipe.enable_attention_slicing()

    #prompt = "In 'Top Gun Maverick,' Tom Cruise's Maverick engages in a thrilling aerial duel, his determined face visible inside the cockpit amidst rugged canyons and vast skies."

    image = pipe(enhanced_query).images[0]
    return image.save("static/output/q4.png")