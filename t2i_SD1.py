from diffusers import DiffusionPipeline

def t2i_SD1(enhanced_query,file_name):
    pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    pipe = pipe.to("mps")

    # Recommended if your computer has < 64 GB of RAM
    pipe.enable_attention_slicing()

    # prompt = "Tom Cruise's character, Maverick, engages in a high-speed aerial dogfight in the movie 'Top Gun: Maverick'"
    # prompt = "Tom Cruise's character, Maverick, engages in a thrilling aerial combat scene in an F-18 fighter jet amidst a canyon, showcasing intense maneuvers and evading enemy fire, in the movie 'Top Gun: Maverick'."
    # prompt = "Tom cruise engages in a daring aerial combat mission to destroy an unsanctioned uranium enrichment plant defended by surface-to-air missiles, GPS jammers, and enemy fighters, ultimately sacrificing his own plane to protect his student, Rooster, and ensuring the success of the mission in 'Top Gun: Maverick'."
    # prompt = "Tom Cruise, portraying Navy Captain Pete 'Maverick' Mitchell, engages in intense aerial combat missions, navigating through a series of challenges and personal conflicts to protect his team and complete a critical mission, ultimately displaying unwavering courage and sacrifice in the face of adversity."
    prompt = enhanced_query

    image = pipe(prompt).images[0]
    image.save(f"static/output/{file_name}.png")

    # print("ended")
    return 1