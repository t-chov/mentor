import openai
import streamlit as st
from more_itertools import chunked

openai_api_key = st.secrets['openai']['api_key']
openai.api_key = openai_api_key


def define_cols(size: str) -> int:
    if size == "256x256":
        return 4
    elif size == "512x512":
        return 2
    else:
        return 1

def generate_images(*args, **kwargs):
    size = kwargs.get("size", "256x256")
    cols = define_cols(size)
    num = kwargs.get("num", 1)
    response = openai.Image.create(
        prompt=kwargs.get("prompt", "a white siamese cat"),
        n=num,
        size=size,
    )
    for row in chunked(response["data"], cols):
        for img, col in zip(row, st.columns(cols)):
            col.image(img["url"])


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
