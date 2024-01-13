from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_categories(sample):
    prompt = f"""
        The following are random samples from a JIRA project. Please create
        classifications for the category these issues could fall into, and
        sub categories underneath. These should be general enough that you 
        can classify any issue from this project into one of these, but 
        should make sense. Return a JSON object with a key "categories" and a list
        of objects with the key "category", and "subcategories" which would be a string
        list of the subcategories. Make sure to include other as a category and subcategory for each.
        {sample}
    """
    completion = client.chat.completions.create(
        model="gpt-4-32k",
        messages=[{"role": "system", "content": prompt}]
    )
    return completion.choices[0].message.content

def classify(issue, categories):
    prompt = f"""
        Use the following categories to classify the following JIRA issue:
        
        {categories}
        
        return a JSON object with the keys "category" and "subcategory", 
        importantly, do not explain why just return one JSON object and make sure it's one of the
        categories/subcategories and ONLY one.
        
        {issue}
    """
    completion = client.chat.completions.create(
        model="gpt-4-32k",
        messages=[{"role": "system", "content": prompt}]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content