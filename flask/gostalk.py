import openai
import json
import os

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get('OPENAI_API_KEY')
#%%
if API_KEY:
    openai.api_key = API_KEY    # API_KEY is the key to access the openai API, you can get it from https://platform.openai.com/account/api-keys
else:
    print('Please set the OPENAI_API_KEY environment variable.\n You can get it from https://platform.openai.com/account/api-keys')
#%%

template_data = '''{
                "url": "https://server.gosling-lang.org/api/v1/tileset_info/?d=cistrome-multivec",
                "type": "multivec",
                "row": "sample",
                "column": "position",
                "value": "peak",
                "categories": ["sample 1", "sample 2", "sample 3", "sample 4"]
                '''

Chat_FineTune_Message = [
                { 'role': 'system', 'content': "Hello, I'm Gosling. I'm a visualization toolkit for interactive genomic data." },
                {"role": "system", 'content': 'I can help you write gosling specification json code'},
                
                # template data
                {"role": "user", "content": (
                    "please just draw one sample unless you are asked to draw multiple samples,"
                    'always update the template spec if it is given'
                    )
                },

                # teach the gosling grammar again
                {"role": "user", "content": (
                    'do not miss tracks, ' 
                    'axis should be specified as string, '
                    'and one axis should be genomic, '
                    #'remember to specify the field name, '
                    'width and height should be specified for each track or view as number'
                )},

                {"role": "user", "content": (
                    'the genomic axis of tracks in the same view will be linked'
                )},
                # multi view
                {"role": "user", "content": (
                    'the track number is in the title of the tracks,'
                    'do not change track titles,'
                    'do not leave tracks out unless you are told to do so.'
                    'always update information from the original spec instead of building a new one.'
                    'if no track is specified, apply the change to all tracks'
                )},
                # grammar
                {"role": "user", "content": (
                    'to change the color of a track, change the hex value string in the range field of color,'
                    'the colors of rows correspond to the values in the range. to change colors of tracks, update the values in or change the order of color ranges.'
                    'to change whether to include a bounding box, change the value of outlinewidth of style, 1 indicates to have a bounding box, 0 indicates to remove the bounding box.'
                    'to add rows to a track, add values to categories under data field. we cannot add more tracks to heatmap,'
                )},
                # mark
                {"role": "user", "content":(
                    'triangleLeft and triangleRight are both refered as triangle marks'
                )},
                # multi view
                {"role": "user", "content":(
                    'If some tracks are specified in one change, apply the following changes in the same instruction to all of them unless you are told otherwise.'
                )}

               
            ]


class GosTalk_ChatGPT():
    MODEL = 'gpt-3.5-turbo'
    def __init__(self, template_chart=None,prompt=Chat_FineTune_Message):
        self.prompt = prompt
        if template_chart:
            self.prompt = self.prompt + [{"role": "user", "content": f'help me update the Gosling Specification Code {template_chart}'}]

    def ask(self, new_question):

        self.prompt = self.prompt + [{"role": "user", "content": new_question}]

        response = openai.ChatCompletion.create(
            model=GosTalk_ChatGPT.MODEL,
            messages=self.prompt,
            temperature=0,
            # stream=True  # this time, we set stream=True
        )

        content = response.choices[0]['message']['content']

        if '```' in content:
            code = content.split('```')[1]
            explanation = content.split('```')[2]
        else:
            code = content
            explanation = ''

        print(explanation)
        print(code)

        self.prompt = self.prompt + [{"role": "assistant", "content": code}]
        
        return explanation, code
