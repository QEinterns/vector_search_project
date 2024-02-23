from diffusers import DiffusionPipeline

def sd1(movie_name, enhanced_query):
    pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    pipe = pipe.to("mps")

    # Recommended if your computer has < 64 GB of RAM
    pipe.enable_attention_slicing()

    #prompt = "In 'Top Gun Maverick,' Tom Cruise's Maverick engages in a thrilling aerial duel, his determined face visible inside the cockpit amidst rugged canyons and vast skies."

    image = pipe(enhanced_query).images[0]
    image.save(f"output/{movie_name}.png")