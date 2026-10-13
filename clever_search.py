import os
import streamlit as st
import requests
import xmltodict

hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_footer, unsafe_allow_html=True)


private_key = os.environ.get('searchapikey')
url = "https://yandex.ru/search/xml"

filters = [
    'dns.ru',
    'citilink.ru',
    'apple.com',
    'samsung.com',
    'sony.com',
    'techradar.com',
    'google.com',
    'microsoft.com',
    'amazon.com',
    'dns.ru',
    'citilink.ru',
    'apple.com',
    'samsung.com',

]
filter_query = " | ".join([f"site:{url}" for url in filters])


def get_search_results(input_text: str) -> list[str]:
    folder = os.environ.get("YANDEX_FOLDER_ID") or os.environ.get("folderid", "")
    key = os.environ.get("YANDEX_SEARCH_API_KEY") or os.environ.get("searchapikey", "")
    if not folder or not key:
        raise RuntimeError("Configure YANDEX_FOLDER_ID and YANDEX_SEARCH_API_KEY.")
    query_params = {
        "folderid": folder,
        "apikey": key,
        "query": input_text + f"({filter_query})",
    }
    try:
        search_response = requests.get(url, params=query_params, timeout=(10, 30))
        search_response.raise_for_status()
        search_response = xmltodict.parse(search_response.text)
        result = search_response['yandexsearch']['response']
        if 'error' in result:
            raise RuntimeError("Yandex Search rejected the request.")
        groups = result.get('results', {}).get('grouping', {}).get('group', [])
        if isinstance(groups, dict):
            groups = [groups]
        urls = []
        for group in groups:
            docs = group.get('doc', [])
            if isinstance(docs, dict):
                docs = [docs]
            urls.extend(doc['url'] for doc in docs if 'url' in doc)
    except Exception as e:
        raise RuntimeError("Yandex Search failed; check account configuration and quota.") from None
    return urls


def ya_search_interface() -> None:
    st.markdown('Ищите проффесионально в Яндекс Поиске')
    st.write('\n')  # add spacing

    st.subheader('\nКакой товар ищите?\n')
    with st.expander("Поисковый запрос", expanded=True):

        input_ = st.text_input('Введите товар', '')
        answer = []
        space, right_col = st.columns([5, 2])
        with right_col:
            if st.button('Отправить запрос'):
                try:
                    with st.spinner():
                        answer = get_search_results(input_)
                except RuntimeError as error:
                    st.error(str(error))

    if answer:
        st.write('\n')  # add spacing
        st.subheader(f'\nРезультаты по запросу: {input_}\n')
        with st.expander("Результаты", expanded=True):
            for uri in answer:
                st.write(uri)


if __name__ == '__main__':
    # call main function
    ya_search_interface()
