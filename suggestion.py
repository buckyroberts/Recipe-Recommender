import os

import promptlayer

openai = promptlayer.openai
openai.api_key = os.getenv('OPENAI_API_KEY')


def suggest_final_recipe(food, recipes_list):
    """Given a prompt and a list of recipes, use GPT to suggest one of the recipes"""

    # Fetch our template from PromptLayer
    recipe_template = promptlayer.prompts.get('recipe_template')
    recipe_template_template = recipe_template['template']

    # Set our template variables
    variables = {
        'food': food,
        'recipes_string': '\n\n'.join(recipes_list)
    }

    response, pl_request_id = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'system',
                'content': (
                    'You are a helpful assistant. '
                    'Given some user input and a list of recipes, suggest one of the recipes. '
                    'The final output should be the full recipe.'
                )
            },
            {
                'role': 'user',
                'content': recipe_template_template.format(**variables)
            },
        ],
        temperature=0.5,
        max_tokens=1024,
        return_pl_id=True
    )
    print(response.choices[0].message.content)

    # Associate request with a prompt template
    promptlayer.track.prompt(
        request_id=pl_request_id,
        prompt_name='recipe_template',
        prompt_input_variables=variables
    )
