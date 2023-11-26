import os

from dotenv import load_dotenv

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

MONTH_NAMES = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь',
}


def ai_question(question) -> str:
    load_dotenv()
    chat = GigaChat(credentials=os.environ.get('GIGA_CHAT_TOKEN'), verify_ssl_certs=False)
    messages = [
        SystemMessage(
            content="Ты финансовый аналитик, который понятно и доступно может дать совет любому человеку."
        ),
        HumanMessage(
            content=question
        ),
    ]

    res = chat(messages)
    return res.content
