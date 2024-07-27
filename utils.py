# This file contains all the helper functions being used

import json
from prompts import question_levels

GPT_VISION = 'gpt-4-vision-preview'
GPT_4 = 'gpt-4-0125-preview'
MAX_TOKENS = 1024

def ask_gpt(client, user_prompt, model, sys_prompt=''):

  prompt_messages = [
          {
          "role": "user",
          "content": user_prompt
          }
          ]

  if sys_prompt:
    prompt_messages = [{"role": "system", "content": sys_prompt}] + prompt_messages

  completion = client.chat.completions.create(model=model,
                                              messages=prompt_messages,
                                              max_tokens=MAX_TOKENS
                                              )

  return completion.choices[0].message.content


def ask_gptV(user_prompt, img_link, client):
  response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [

        {
          "type": "image_url",
          "image_url": {
            "url": img_link,
          },
        },
      ],
    }
  ],
  max_tokens=4096,
  )

  return response.choices[0].message.content


def clean_json(gpt_response):
  s = gpt_response.strip().strip('`').strip('json').strip()
  return json.loads(s)


def clean_python(gpt_response):
  s = gpt_response.strip().strip('`').strip('python').strip()
  return s


def get_plot_code(client, json_schema, plot_create_prompt):
  json_schema = json.loads(json_schema)
  instr = json_schema['instructions']
  schema = {k:v for k, v in json_schema.items() if k!='instructions' and json_schema[k]}
  s = plot_create_prompt.format(instructions=instr, schema=schema)

  response = ask_gpt(client, s, GPT_4)

  return clean_python(response)


def get_plot_questions(client, json_schema, question_level, plot_questions_prompt):
  json_schema = json.loads(json_schema)
  instr = json_schema['instructions']
  plot_code = json_schema['plot_code']
  question_level = question_levels[question_level]
  s = plot_questions_prompt.format(instructions=instr, code=plot_code, q_level=question_level)

  response = ask_gpt(client, s, GPT_4)

  response = response.strip().split('\n')

  return response


def plot_rows(dataframe):
  for idx, i in dataframe.iterrows():
    try:
      print(idx)
      exec(i['plot_code'])
      print('\n'.join(i['questions']))
    except Exception as e:
      # print(f'\n{"#"*100}\n\nCOULD NOT GENERATE PLOT {idx} WITH CODE:\n\n{i["plot_code"]}\n\n{"#"*100}\n')
      print(f'\n{"#"*100}\n\nCOULD NOT GENERATE PLOT {idx}\n\n')
