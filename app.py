import json

import streamlit as st
from openai import OpenAI

# client = OpenAI(
#     # This is the default and can be omitted
#     api_key=os.environ["OPENAI_API_KEY"],
# )


def create_blog(topic, keywords, length, client: OpenAI = None, money_sites: dict = None):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": '''
                    You are a professional Wordpress Blog Writter who writes blogs in html format with links to money(main) sites and make sure to add new line manually and do not alter the anchor text.
                        Input: 
                        {
                            'topic': {topic},
                            'keywords': [
                                {keyword1},
                                {keyword2}
                                ....
                            ],
                            'length': {no_of_words_for_the_article}
                            'm-sites': {
                                {link}: {anchor_text}
                                ...
                            }
                        }
                        Output:
                        {
                            'title': {title},
                            'content': {content}
                        }
                ''',
            },
            {
                "role": "user",
                "content": json.dumps({
                    'topic': topic,
                    'keywords': keywords,
                    'length': length,
                    'm-sites': money_sites
                })

                ,
            },
        ],
        model="gpt-3.5-turbo",
        temperature=0.9,
    )

    return chat_completion.choices[0].message.content

st.title('Blog Writter')
st.write('''
    This is a blog writter that can write a blog for you.
    You just need to provide the topic and keywords.
''')

topic = st.text_input('Topic')
# make a text area for keywords
keywords = st.text_area('Keywords')
length = st.number_input('Length', min_value=100, max_value=1000000, value=100)
api_key = st.text_input('OpenAI API Key')
money_sites = st.text_area('Money Sites',
                            placeholder='''https://www.example.com: example
                                            https://www.example.com: example
                            '''
)


if st.button('Create Blog'):
    client = OpenAI(api_key=api_key)
    # '''
    #     Money sites are in the format
    #     link: anchor text
    # '''
    money_sites = money_sites.split('\n')
    money_sites = [site.split(':') for site in money_sites]
    money_sites = {site[0].strip(): site[1].strip() for site in money_sites}

    blog = json.loads(create_blog(topic, keywords.split('\n'), length, client, money_sites))
    title = blog['title']
    content = blog['content']
    st.write(f'# {title}')
    st.write(content)
    
