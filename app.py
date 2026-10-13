import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title='Нейроконсультант', page_icon='🔎')

from clever_search import ya_search_interface
from neuro_mentor import ya_gpt_interface

st.title('Нейроконсультант')
if st.radio('Инструмент', ['Поиск товаров', 'Помощник сотрудника'], horizontal=True) == 'Поиск товаров':
    ya_search_interface()
else:
    ya_gpt_interface()
