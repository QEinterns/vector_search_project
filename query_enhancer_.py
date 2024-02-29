from llama_cpp import Llama
import logging
 
def query_enhancer(context,query):
      print("\n\n")
      print(query)
      print(context)
      
      print("\n\n")
      if(len(context)>9600):
            context = context[:9500]
      llm = Llama(
            model_path='/Users/spatra/Desktop/Movie/query_enhancer/mistral-7b-openorca.Q4_0.gguf',
            # n_gpu_layers=-1, # Uncomment to use GPU acceleration
            # seed=1337, # Uncomment to set a specific seed
            n_ctx=10000, # Uncomment to increase the context window
      )
      output = llm(
            f"Q: Context:{context} .Query:{query} . You are a couchbase documentation chatbot, answer the given query based on the context provided to you by docs provided as context. A:", # Prompt
            max_tokens=None, # Generate up to 32 tokens, set to None to generate up to the end of the context window
      # Echo the prompt back in the output
      ) # Generate a completion, can also call create_completion
      # print(output)
      # print(str(output['choices'][0]['text']))
      
      return str(output['choices'][0]['text'])
      # {
      #   'id': 'cmpl-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
      #   'object': 'text_completion',
      #   'created': 1679561337,
      #   'model': './models/7B/llama-model.gguf',
      #   'choices': [
      #     {
      #       'text': 'Q: Name the planets in the solar system? A: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune and Pluto.',
      #       'index': 0,
      #       'logprobs': None,
      #       'finish_reason': 'stop'
      #     }
      #   ],
      #   'usage': {
      #     'prompt_tokens': 14,
      #     'completion_tokens': 28,
      #     'total_tokens': 42
      #   }
      # }
      # from gpt4all import GPT4All
      # model = GPT4All('mistral-7b-openorca.Q4_0.gguf')
      # output = model.generate('The capital of France is ')
      # print(output)
      # from gpt4all import GPT4All
      # model = GPT4All('/Users/nishanth/movie_proj/mistral-7b-openorca.Q4_0.gguf',allow_download=True)
      # output = model.generate(prompt='The capital of France is ? Give the answer in detail. Explain more information on the answer.',temp=0)
      # print(output)
      # import gpt4all
      # # print(dir(gpt4all))
      # from gpt4all import GPT4All
      # gpt = GPT4All(model_name='gpt4all-falcon-newbpe-q4_0.gguf')
      # st = "plot : plot:More than 30 years after graduating from Top Gun,[a] United States Navy Captain Pete 'Maverick' Mitchell is a decorated test pilot whose repeated insubordination has kept him from flag rank.[b] When Rear Admiral Chester 'Hammer' Cain plans to cancel the hypersonic 'Darkstar' scramjet program Maverick is testing on the grounds that it has not reached the contract specification of Mach 10, Maverick unilaterally changes the target speed for that day's test from Mach 9 to Mach 10 and commences the test early in order to prove Cain wrong. During the test flight, Maverick successfully reaches Mach 10 in the Darkstar prototype; however, the prototype aircraft is destroyed when Maverick cannot resist pushing his airspeed beyond Mach 10. After the flight, Cain tells Maverick that he would be grounded if not for Admiral Tom 'Iceman' Kazansky, Maverick's friend and former Top Gun rival. Iceman, now commander of the U.S. Pacific Fleet, has assigned Maverick to the Top Gun school at NAS North Island. The Navy has been ordered to destroy an unsanctioned uranium enrichment plant before it becomes operational. The plant, located in an underground bunker at the end of a canyon, is defended by surface-to-air missiles (SAMs), GPS jammers, and fifth-generation Su-57 fighters as well as older F-14 Tomcats. Maverick devises a plan employing two pairs of F/A-18E/F Super Hornets armed with laser-guided bombs, but instead of participating in the strike, he is to train an elite group of Top Gun graduates assembled by Air Boss Vice Admiral Beau 'Cyclone' Simpson. Maverick dogfights his skeptical students and prevails in every contest, winning their respect. Two of the students clash: Lieutenants Jake 'Hangman' Seresin and Bradley 'Rooster' Bradshaw—son of Maverick's deceased best friend and RIO Nick 'Goose' Bradshaw. Rooster dislikes Hangman's cavalier attitude, while Hangman criticizes Rooster's cautious flying. Maverick reunites with former girlfriend Penny Benjamin, to whom he reveals that he promised Rooster's dying mother that Rooster would not become a pilot. Rooster, unaware of the promise, angrily resents Maverick for blocking his Naval Academy application—impeding his military career—and blames him for his father's death. Maverick is reluctant to further interfere with Rooster's career, but the alternative is to send him on the extremely dangerous mission. He tells his doubts to Iceman, who has terminal throat cancer. Iceman tells him, 'It's time to let go' and reassures him that both the Navy and Rooster need Maverick. Iceman dies soon after, and after an F/A-18F crashes during training, Cyclone removes Maverick as instructor. He relaxes the mission parameters so they are easier to execute but make escape much more difficult. During Cyclone's announcement, Maverick makes an unauthorized flight through the course with even stricter parameters than the original and hitting the target without a wingman, proving that it can be done. Despite the act of insubordination, Cyclone reluctantly appoints Maverick as team leader. Maverick flies the lead F/A-18E, accompanied by a buddy-lasing F/A-18F[c] flown by Lieutenant Natasha 'Phoenix' Trace and WSO Lieutenant Robert 'Bob' Floyd. Rooster leads the second strike pair, which includes Lieutenant Reuben 'Payback' Fitch and WSO Lieutenant Mickey 'Fanboy' Garcia. The four jets launch from an aircraft carrier, and Tomahawk cruise missiles destroy the nearby air base as they approach. The teams destroy the plant, but the SAMs open fire during their escape. Rooster runs out of countermeasures, and Maverick sacrifices his plane to protect him from an incoming strike. Believing Maverick to be dead, all jets are ordered back to the carrier, but Rooster disobeys and returns to find that Maverick ejected and is being pursued by an Mi-24 attack helicopter. After destroying the gunship, Rooster is shot down by a SAM and ejects. The two rendezvous and steal an F-14 from the damaged air base. Maverick and Rooster destroy two intercepting Su-57s, but a third attacks as they run out of ammunition and countermeasures. Hangman unexpectedly arrives in time to shoot it down, and the planes return safely. Later, Rooster helps Maverick work on his P-51 Mustang. Rooster looks at a photo of their mission's success, pinned alongside a photo of his late father and a young Maverick, as Penny and Maverick fly off in the P-51. Query: Tom cruise is fighting . Now enhance this query and give a detailed specific query using the above plot as context. The purpose of this is, I can feed the query to a text to image LLM. Since those models require very specific details, Give a query which is not so long or has more adjectives. Instead focus on the details and the scenario."
      # print(gpt.generate(st))