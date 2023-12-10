import json

import streamlit as st
from openai import OpenAI

# client = OpenAI(
#     # This is the default and can be omitted
#     api_key=os.environ["OPENAI_API_KEY"],
# )


def create_blog(topic, keywords, length, client: OpenAI = None):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": '''
                    You are a professional Blog Writter.
                        Input: 
                        {
                        'topic': {{topic}},
                        'keywords': [
                            {{keyword1}},
                            {{keyword2}}
                            ....
                        ],
                        'length': {{no of words for the article}}
                        }
                ''',
            },
            {
                "role": "user",
                "content": json.dumps({
                    'topic': topic,
                    'keywords': keywords,
                    'length': length
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
length = st.number_input('Length', min_value=100, max_value=1000, value=100)
api_key = st.text_input('OpenAI API Key')



if st.button('Create Blog'):
    client = OpenAI(api_key=api_key)
    blog = create_blog(topic, keywords.split('\n'), length, client)
    st.write(blog)
