import asyncio
import inspect
import ollama
from pywizlight import wizlight, PilotBuilder
from typing import Dict, Any, Callable
from langchain_core.prompts import ChatPromptTemplate
#from langchain import ChatOllama
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import whisper
import sys
#
#from aud2 import get_audio, speak, listen_for_wake_word
#from aud import record_audio, speak
from aud3 import listen_for_wake_word, record_audio, speak, transcribe_audio
from scene import get_scene_id, SCENES, get_available_scenes, get_top_five_scenes
from web import web_search
from youtube import play_youtube
from weather import get_weather
from news import get_top_news, get_more_articles
#
import warnings
# Suppress specific categories
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
#
ip_address = "192.168.1.24"  # replace with your bulb's IP

#
OUTPUT_FILENAME = "Recorded.wav"
WAKE_WORD_FILENAME = "output.wav"
COMMAND_FILENAME = "LightCommand.wav"
#
MODEL_NAME = "small"
model = whisper.load_model(MODEL_NAME)

# Suppress buggy cleanup
if hasattr(wizlight, "__del__"):
    del wizlight.__del__
# --- Light control functions ---
async def turnon_light(location: str):
    try:
        bulb = wizlight(ip_address)
        print("Turning on the light at the entrance...")
        await bulb.turn_on(PilotBuilder(scene=1))
        await asyncio.sleep(1)
        await bulb.async_close()   # ✅ closes socket cleanly
        return "Light turned on."
    except Exception as e:
        return "Error " + str(e)
#

async def turnoff_light(location: str):
    try:
        """Turn off the light at the entrance."""
        bulb = wizlight(ip_address)
        print("Turning off the light at the entrance...")
        await bulb.turn_off()
        await asyncio.sleep(1)
        await bulb.async_close()   # ✅ closes socket cleanly
        return "Light turned off."
    except Exception as e:
        return "Error " + str(e)
#

#
async def change_color(color: str):
    try:
        scene_id = get_scene_id(color)  # reuse the helper to map name → ID
        if not scene_id:
            return f"Scene '{color}' not recognized."

        bulb = wizlight(ip_address)
        print(f"Changing light to {color} (ID={scene_id})...")
        await bulb.turn_on(PilotBuilder(scene=scene_id))
        await asyncio.sleep(1)
        await bulb.async_close()
        return f"Light set to {color}."
    except Exception as e:
        return "Error " + str(e)
#
light_tools = [
    {
        "type": "function",
        "function": {
            "name": "turnon_light",
            "description": "Turn on the entrance light.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                    "type": "string",
                    "description": "The location of the light i.e. livingroom bedroom."
                }
                }
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "turnoff_light",
            "description": "Turn off the entrance light.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                    "type": "string",
                    "description": "The location of the light i.e. livingroom bedroom."
                }
                }
            },
        },
    },
{
    "type": "function",
    "function": {
        "name": "change_color",
        "description": "Change the light color to a given scene.",
        "parameters": {
            "type": "object",
            "properties": {
                "color": {
                    "type": "string",
                    "description": "The name of the scene or color, e.g. 'Ocean', 'Romance', 'Sunset'."
                }
            },
            "required": ["color"]
        },
    },
},
{
        "type": "function",
        "function": {
            "name": "get_available_scenes",
            "description": "List all available scenes.",
            "parameters": {
                "type": "object",
                "properties": {}
            },
        },
},
{
        "type": "function",
        "function": {
            "name": "get_top_five_scenes",
            "description": "List all available scenes.",
            "parameters": {
                "type": "object",
                "properties": {}
            },
        },
},
{
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for the user query and return results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"],
            },
        },
    },
{
    "type": "function",
    "function": {
        "name": "play_youtube",
        "description": "Play a song or video on YouTube.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Song or video name"}
            },
            "required": ["query"],
        },
    },
},
{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for the New York.",
            "parameters": {
                "type": "object",
                "properties": {}
            },
        },
},
{
        "type": "function",
        "function": {
            "name": "get_top_news",
            "description": "Get top news for the day.",
            "parameters": {
                "type": "object",
                "properties": {}
            },
        },
},
{
    "type": "function",
    "function": {
        "name": "get_more_articles",
        "description": "Get news articles on a topic",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "news article"}
            },
            "required": ["topic"],
        },
    },
},
   
]
#
def clean_quotes(text: str) -> str:
    # Remove single and double quotes
    return text.replace("'", "").replace('"', "")
#
def get_response(user_query: str, function_call: list):

    template = """You are a home assistant with access to light, web search, news, and weather functions.  
                Always form a short, natural, and user-friendly response based on the outcome of the function call.  
                Your response will be spoken aloud by text to speech, so avoid symbols, asterisks, lists, or code formatting.  
                Write the response in plain conversational language.  
                Spell out numbers and dates so they are read correctly by text to speech.  
                Keep it concise and clear.
    User question: {question}
    function_call: {function_call}"""
    #
    prompt = ChatPromptTemplate.from_template(template)
    # llm
    llm = ChatOllama(model="llama3",  base_url="http://192.168.1.70:11434", temperature=0)
    #
    chain = (prompt
    | llm
    | StrOutputParser()
    )

    return chain.invoke({
    "question": user_query,
    "function_call": function_call,
    })

# --- Chat with Ollama + tool calling ---
async def main():
    available_functions: Dict[str, Callable] = {
        'turnon_light': turnon_light,
        'turnoff_light': turnoff_light,
        'change_color': change_color,
        'get_top_five_scenes': get_top_five_scenes,
        'get_available_scenes': get_available_scenes,
        'web_search': web_search,
        'play_youtube': play_youtube,
        'get_weather': get_weather,
        'get_top_news': get_top_news,
        'get_more_articles': get_more_articles
    }

    while True:
        if listen_for_wake_word():   # Wait for "okay amy"
            record_audio()           # Record 5 seconds
            #print("You can now transcribe or process the audio...")
            result = transcribe_audio(OUTPUT_FILENAME)
            transcript = result.lower().strip()
            print("Transcription:", transcript)
            #speak(transcript)

            if any(word in transcript for word in ["quit", "exit", "stop", "goodbye"]):
                    speak("Goodbye")
                    print("User ended the program.")
                    sys.exit(0)  # exit program
            elif "sorry, i did not" in transcript:
                speak("Sorry, I did not get that. Please try again.")
                continue
            #
            else:
                # Play audio chunk
                client = ollama.Client(host="http://192.168.1.70:11434") 
                response = client.chat(
                model="llama3.2",  # instruct model handles tool calls better
                messages=[{"role": "user", "content": transcript}],
                tools=light_tools,
                )

                message = response["message"]
                if "tool_calls" in message:
                    for tool in message["tool_calls"]:
                        fn_name = tool["function"]["name"]
                        fn_args = tool["function"].get("arguments", {})

                        if fn_name in available_functions:
                            print(f"Calling function: {fn_name}")
                            fn = available_functions[fn_name]
                            sig = inspect.signature(fn)
                            valid_args = {k: v for k, v in fn_args.items() if k in sig.parameters}
                            result = await fn(**valid_args)
                            print("Function output:", result)
                            cleaned_output = clean_quotes(result or "")
                            # Optional: send result back to model for natural response
                            response = get_response(transcript, cleaned_output)
                            print("Assistant:", response or "(no response)")
                            speak(response or "(no response)")
                        else:
                            print(f"Function {fn_name} not found")
                else:
                    print("Assistant:", message["content"])


if __name__ == "__main__":
    asyncio.run(main())