from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from src.llm.output_models import MockOutput
from src.llm.prompts import SYSTEM_PROMPT

LLM = ChatOllama(model="mistral", temperature=0)


def process_decision(paper: str):
    # TODO: Complete user prompt
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_PROMPT,
            ),
            ("user", "Here is the decision paper: {decision_paper}. I want you to ..."),
        ]
    )

    chain = prompt_template | LLM
    # TODO: Use output parser here if needed, real testing needed
    structured_llm = chain.with_structured_output(MockOutput)
    structured_llm.invoke({"decision_paper": paper})
