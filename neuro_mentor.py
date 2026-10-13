import os
import streamlit as st
import requests
import xmltodict

hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_footer, unsafe_allow_html=True)


private_key = os.environ.get('yagptkey', '')
url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
data = {}
data["completionOptions"] = {"stream": False, "temperature": 0.3, "maxTokens": "1000"}


def get_ya_gpt(input_text: str) -> str:
    folder = os.environ.get("YANDEX_FOLDER_ID") or os.environ.get("folderid", "")
    key = os.environ.get("YANDEX_API_KEY", "")
    token = os.environ.get("YANDEX_IAM_TOKEN") or os.environ.get("yagptkey", "")
    if not folder or not (key or token):
        raise RuntimeError("Configure YANDEX_FOLDER_ID and YANDEX_API_KEY or YANDEX_IAM_TOKEN.")
    payload = {**data, "modelUri": f"gpt://{folder}/yandexgpt-lite/latest"}
    payload["messages"] = [
        {
            "role": "system",
            "text": """Ты — специалист, помогающий сотрудникам онлайн интернет магазина техники помочь с работой,
            твоя задача координировать их и проводить обзор по сервисам для сотрудников ...""",
        },
        {
            "role": "user",
            "text": input_text
        }
    ]
    try:
        response = requests.post(
            url, headers={"Authorization": f"Api-Key {key}" if key else f"Bearer {token}"},
            json=payload, timeout=(10, 60)
        )
        response.raise_for_status()
        answer = response.json()["result"]["alternatives"][0]["message"]["text"]
    except Exception as e:
        raise RuntimeError("YandexGPT request failed; check account configuration and quota.") from None
    return answer


def ya_gpt_interface() -> None:
    st.markdown('Ассистент поможет вам в ваших вопросах')
    st.write('\n')  # add spacing

    st.subheader('\nЗапрос AI помощь\n')
    with st.expander("", expanded=True):

        input_ = st.text_input('Ваш запрос', 'Помоги разобраться с тем как искать товары?')
        answer = []
        space, right_col = st.columns([5, 2])
        with right_col:
            if st.button('Отправить запрос'):
                try:
                    with st.spinner():
                        answer = get_ya_gpt(input_)
                except RuntimeError as error:
                    st.error(str(error))

    if answer:
        st.write('\n')  # add spacing
        st.subheader(f'\nРезультаты по вашему запросу:\n')
        with st.expander("Ответ", expanded=True):
            st.write(answer)


if __name__ == '__main__':
    # call main function
    ya_gpt_interface()
