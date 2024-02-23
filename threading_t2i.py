import threading
from opendalle import opendalle
from openjourney import openjourney
from playground import playground
from proteus import proteus
from t2i_SD1 import t2i_SD1

def threadit(enhanced_query,text_to_image):
    model_name = "" 
    if(text_to_image=="Stable diffusion X"):
        model_name = t2i_SD1
    elif(text_to_image=="Proteus"):
        model_name = proteus
    elif(text_to_image=="Playground"):
        model_name =playground
    else:
        model_name = openjourney
    
    
    p1 = threading.Thread(target=model_name,args=(enhanced_query,"q1"))
    p2 = threading.Thread(target=model_name,args=(enhanced_query,"q2"))
    p3 = threading.Thread(target=model_name,args=(enhanced_query,"q3"))
    p4 = threading.Thread(target=model_name,args=(enhanced_query,"q4"))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()

    return 1    