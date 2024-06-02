from dotenv import load_dotenv
import os
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain


# Sequential Chain

load_dotenv() # Load the env file

secret_key = os.getenv('openapi_key')
os.environ['OPENAI_API_KEY'] = secret_key

llm = OpenAI(temperature=0.7)



def generate_restaurant_name_and_items(cuisine):
    # Chain 1 to get the name
    prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template="I want to open a restaurant for {cuisine} food. Suggest a fancy name for this"
    )
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_name")

    # Chain 2 to get the items
    prompt_template_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="Suggest some menu items for {restaurant_name}. Return it as a comma-separated list."
    )
    food_items_chain = LLMChain(llm=llm, prompt=prompt_template_items, output_key="menu_items")

    chain = SequentialChain(
        chains=[name_chain, food_items_chain],
        input_variables=['cuisine'],
        output_variables=['restaurant_name', 'menu_items']

    )
    response = chain({'cuisine': cuisine})

    return response



if __name__ == "__main__":
    print(generate_restaurant_name_and_items("Italian"))