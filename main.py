import requests




def solve_word(word, model="gemma3"):
    prompt = '''You are playing a strategy game. Each round, you must choose **one word** from a fixed list that can **defeat** an opponent word. 

    Your goal is to **spend as little money as possible** while still **winning the round**.

    A word defeats the opponent if it makes logical sense in a symbolic or physical way. Always choose the **cheapest possible word** from the list that can beat the opponent.

    You may **only choose words from the list** below. No other words are allowed.

    Respond with only **one word** from the list. Do not explain your answer.

    ---

    ### Example 1:
    Opponent: Candle  
    Best response: Wind  

    ### Example 2:
    Opponent: Tank  
    Best response: Nuclear Bomb  

    ### Example 3:
    Opponent: House  
    Best response: Earthquake  

    ---

    Now choose a word to defeat: {0}

    Only choose from this list (format: Word,Cost):

    Feather,1  
    Coal,1  
    Pebble,1  
    Leaf,2  
    Paper,2  
    Rock,2  
    Water,3  
    Twig,3  
    Sword,4  
    Shield,4  
    Gun,5  
    Flame,5  
    Rope,5  
    Disease,6  
    Cure,6  
    Bacteria,6  
    Shadow,7  
    Light,7  
    Virus,7  
    Sound,8  
    Time,8  
    Fate,8  
    Earthquake,9  
    Storm,9  
    Vaccine,9  
    Logic,10  
    Gravity,10  
    Robots,10  
    Stone,11  
    Echo,11  
    Thunder,12  
    Karma,12  
    Wind,13  
    Ice,13  
    Sandstorm,13  
    Laser,14  
    Magma,14  
    Peace,14  
    Explosion,15  
    War,15  
    Enlightenment,15  
    Nuclear Bomb,16  
    Volcano,16  
    Whale,17  
    Earth,17  
    Moon,17  
    Star,18  
    Tsunami,18  
    Supernova,19  
    Antimatter,19  
    Plague,20  
    Rebirth,20  
    Tectonic Shift,21  
    Gamma-Ray Burst,22  
    Human Spirit,23  
    Apocalyptic Meteor,24  
    Earth’s Core,25  
    Neutron Star,26  
    Supermassive Black Hole,35  
    Entropy,45
    '''.format(word)

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)

    if response.ok:
        return response.json()["response"]
    else:
        return -1







# Example usage
if __name__ == "__main__":


    # Example usage
    answer = solve_word("ghost")
    print("Ollama says:", answer)
