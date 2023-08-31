import openai
import streamlit as st

openai_api_key = st.secrets['openai']['api_key']
openai.api_key = openai_api_key

def generate_images(*args, **kwargs):
    size = kwargs.get("size", "256x256")
    num = kwargs.get("num", 1)
    response = openai.Image.create(
        prompt=kwargs.get("prompt", "a white siamese cat"),
        n=num,
        size=size,
    )
    for img in response["data"]:
        st.image(img["url"])


with st.sidebar:
    size = st.selectbox("size of image", ("256x256", "512x512", "1024x1024"))
    num = st.text_input(label="num_of_images", value=1)
    prompt = st.text_area(label="prompt", height=600, value="a white siamese cat")
    st.button(
        "generate",
        on_click=generate_images,
        kwargs={
            "prompt": prompt,
            "size": size,
            "num": int(num),
        },
    )
