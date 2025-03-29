import requests
from time import sleep
import random
import pandas as pd
import time
import numpy as np
from sympy.physics.units import amount_of_substance

host = "http://172.18.4.158:8000"
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5
global my_words_df
my_words_df = pd.read_csv('data.csv')
# print(my_words_df.head())
my_words_df.drop("id",axis=1,inplace=True)

# print(my_words_df)

def solve_word(word, model="gemma3:12b"):
    prompt = '''You are playing a strategy game. Each round, you must choose **one word** from a fixed list that can **defeat** an opponent word. 

    

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






def random_words(word,df):

    idx = random.randint(0,df.shape[0])
    size = 60
    mean = 60 / 2
    std = size / 6

    x = np.linspace(0, size - 1, size)
    gauss = np.exp(-0.5 * ((x - mean) / std) ** 2)
    gauss = gauss / gauss.sum()
    # print(gauss)

    ceva=  df.sample(5, weights=gauss, axis=0)
    rez = ceva.sample(1)
    print(rez)
    # print(rez.index[0])
    # rez =
    # print(ceva.index.get_loc(rez))
    # print(idx+1)
    return int(rez.index[0] + 1)


def what_beats(word,df):
    start = time.perf_counter()

    # answer =  random_words(word,df)
    answer = solve_word(word)

    if df[df['text'] == answer].empty:
        answer = random_words(word,df)
    else:
        answer = df[df['text'] == answer].index[0] + 1

    end = time.perf_counter()
    elapsed = end - start
    print(f'Time taken: {elapsed:.6f} seconds')
    return answer


def play_game(player_id):
    global my_words_df
    for round_id in range(1, NUM_ROUNDS+1):
        print("...................STARTING ROUND", round_id , "...................")
        round_num = -1
        while round_num != round_id:
            response = requests.get(get_url)
            sys_word = response.json()['word']
            round_num = response.json()['round']

        print(f"round  {round_num} started! - Received GET , word = {sys_word}")
            # sleep(1)

        if round_id > 1:
            status = requests.get(status_url)
            print(status.json())

        choosen_word = what_beats(sys_word,my_words_df)
        data = {"player_id": "ARDUINO Copilul Minune", "word_id": choosen_word, "round_id": round_id}
        response = requests.post(post_url, json=data)
        print(response.json())


play_game(1)

