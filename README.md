<!-- nddev-public-hackathon -->
# hack-2024-citilink

Citilink 2024 hackathon prototype: AI product search, employee onboarding and marketplace description generation. Python + YandexGPT.

[NDDev OpenNetwork](https://github.com/NDDev-Technocracy-OpenNetwork) · [Repository](https://github.com/NDDev-Technocracy-OpenNetwork/hack-2024-citilink)

This repository is a hackathon prototype or supporting tool. Follow the project-specific setup below; cloud integrations require your own configuration and credentials.

---

## Нейроконсультант



## Полуавтоматическая платформа для онлнайн-маркетплейсов
### Структура репозитория
Файлы соответствуют инструментам для сотрудника маркетплейса:
- [clever_search](clever_search.py) - код инструмента для интеллектуального поиска по товарам
- [neuro_mentor](neuro_mentor.py) - код инструмента для онбординга новых сотрудников
- [text_generation](experiments/text_generation/) - код инструментов для генерации описаний товаров и парсинга различных источников.

Скриншот приложения для генерации описания товаров:
![img.png](imgs/img.png)

### Окружение
Используются возможности облачной платформы [Yandex Cloud](https://yandex.cloud/ru/), особенно - возможности сервисов [Yandex DataSpere](https://datasphere.yandex.cloud) и [Yandex Compute Cloud](https://yandex.cloud/ru/services/compute).
В качестве операционной системы используется Ubuntu 22.04.

### Стек
- Python 3.10
- YandexGPT
- Gradio
- Streamlit

### Генерация текста по гетерогенным признакам
Товары на маркетплейсе - коллекция сущностей с неоднородными (гетерогенными признаками), которые пока что плохо поддаются нейронным сетям. Однако существует ряд подходов, помогающий решить возникающие проблемы. Некоторые из них были предложены участниками команды и являются уникальными на рынке. Со статьями на тему генерации текста по гетерогенным данным можно ознакомиться по ссылкам:
- https://habr.com/ru/companies/spbifmo/articles/787660/
- https://kmu.itmo.ru/digests/article/12896

Предлагаемые решения ориентировались на разработки в рамках https://github.com/KirpaDmitriy/boostformers/ и https://github.com/KirpaDmitriy/Podruchniy/.

## Maintained local demo

```sh
uv venv --python 3.12
uv pip install --python .venv/bin/python -r requirements.txt
cp .env.example .env
# Fill your own Yandex folder and API credentials in .env.
.venv/bin/streamlit run app.py
```

The light-theme app provides product search and employee assistance. Missing credentials are reported before sending requests; request timeouts are bounded and authentication URLs are not logged. Provider field names follow the [Yandex completion schema](https://yandex.cloud/ru-kz/docs/foundation-models/text-generation/api-ref/TextGenerationAsync/completion) and [Search API v1 XML documentation](https://yandex.cloud/ru-kz/docs/search-api/concepts/post-request). `python -m unittest discover -s tests` exercises request parsing with mocks, without paid calls. Historical tabular/text-generation research is retained under `experiments/` and is not part of the maintained app.
