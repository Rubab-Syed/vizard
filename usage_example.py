# This file contains how to use vizard end to end
import pandas as pd
import numpy as np
import tiktoken
import json
import os
from glob import glob
from time import time as time_stamp_now
from openai import OpenAI
from tqdm import tqdm
from getpass import getpass
from prompts import plot_ideas_prompt, plot_create_prompt, plot_levels, plot_questions_prompt
from utils import ask_gpt, get_plot_code, get_plot_questions, clean_json

tqdm.pandas(desc="Progress Bar")


#openai_api_key = getpass()

#os.environ['OPENAI_API_KEY']=openai_api_key
#client = OpenAI()

os.environ['OPENAI_API_KEY']='<your-openai-key>'
client = OpenAI()
GPT_VISION = 'gpt-4-vision-preview'
GPT_4 = 'gpt-4-0125-preview'
MAX_TOKENS = 1024

## Pipeline 1: Idea -> Plot -> Question -> Level
    
def evaluation_quiz_pipeline(topic):
    
    for p_level in [1, 2, 3]:
        for q_level in [1, 2, 3]:

            print(f'TOPIC:\t\t{topic}\nPLOT LEVEL:\t{p_level}\nQUESTION LEVEL:\t{q_level}\n')

            now_time_stamp = time_stamp_now()
            r = ask_gpt(client, plot_ideas_prompt.format(plot_topic=topic, p_level=plot_levels[p_level]), GPT_4)
            print(r)
            df_schemas = pd.DataFrame(clean_json(r))
            df_schemas['topic'] = topic
            df_schemas['plot_level'] = p_level
            df_schemas['question_level'] = q_level

            print(f'-> Plot ideas done: {len(df_schemas)} received. Now getting code...')
 
            df_schemas['plot_code'] = df_schemas.progress_apply(lambda x: get_plot_code(client, x.to_json(), plot_create_prompt), axis=1)
            print(f'-> Plot code done. Now getting questions...')

            df_schemas['questions'] = df_schemas.progress_apply(lambda x: get_plot_questions(client, x.to_json(), q_level, plot_questions_prompt), axis=1)

            fname = f'{"_".join(topic.split())}_p_level{p_level}_q_level{q_level}.csv'
            df_schemas = df_schemas[['topic', 'plot_level', 'question_level', 'chart_type', 'variables', 'x-axis', 'y-axis', 'color', 'style', 'label', 'sizes', 'error_bars', 'instructions', 'plot_code', 'questions']]
            df_schemas.to_csv(fname)
            print(f'-> Plot questions done. File saved: {fname}')
            print(f'-> Time taken: {time_stamp_now()-now_time_stamp} seconds\n\n')


def main():
    topic = 'women empowerment in economic development and making them inclusive using microfinance especially in pakistan'

    evaluation_quiz_pipeline(topic)

    return 1


if __name__ == '__main__':
    main()
