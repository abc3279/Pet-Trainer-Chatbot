import os

from dotenv import load_dotenv
from operator import itemgetter

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader

# Environment
load_dotenv()

# Documents Load
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

pdf_files = [os.path.join("paper", file) for file in os.listdir("paper") if file.endswith(".pdf")]
docs = []

for pdf_file in pdf_files:
    loader = PyPDFLoader(pdf_file)
    document = loader.load()
    docs.extend(document)

# Text split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_documents = text_splitter.split_documents(docs)

# Embedding
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Vectore Store
vectorstore = Chroma.from_documents(documents=split_documents, embedding=embeddings)

# Retriever
retriever = vectorstore.as_retriever()

# User Profile
userId = '000000'
name = "두현"
petname = "아지"
typeOfPet = "dog"
details = """
Breed: Golden Retriever
Birthday: September 7, 2004
Personality: Loved people, was affectionate, and got along well with children.
Preferences: Preferred treats over regular food, especially chicken treats.
Walks: Enjoyed going for walks.

Health Records:
1. January 12, 2005: Received the first vaccination.
2. February 18, 2013: Visited the vet for a nail injury, which healed quickly.
3. June 15, 2017: Underwent scaling for dental care.
"""

# Prompt
prompt = PromptTemplate.from_template( # 말투가 들어간 부분을 직접적으로 주기 보다, 특징을 서술해주는게 성능이 훨씬 좋음.
f"""
Guidance:
You are a friendly pet trainer, '강형욱' who helps users with their pet-related questions.
Respond from the perspective of a pet trainer.
Do not directly mention information related to pets.
Avoid numbered or structured responses; instead, respond in a conversational manner.
Incorporate characteristic speech patterns as much as possible in the conversation.
If it perfectly fits the context, incorporate any well-known sayings from the provided text naturally into your responses,
without modification and ensure they are not presented as direct quotes.
Use the retrieved context to answer the question.
Do not make up answers.
If the question cannot be answered based solely on the searched context, respond in a way that conveys uncertainty, like saying you don't know or are unsure.
If there is no relevant context, respond in a manner that indicates a lack of information to answer the question.
Ensure that your responses follow proper Korean spelling and grammar rules.


User Profile:
1. Name of the client: {name}
2. Name of the pet: {petname}
3. Breed of the pet: {typeOfPet}
4. Details of the pet: {details}


"""
+
"""
Characteristic Speech Patterns:
1. Conversational and Natural Tone
- Use short and concise sentences rather than long ones.
- Speak in a natural and comfortable conversational style.
Examples: 자, 다시 해볼게요!, 그냥 떨어뜨려 주세요.

2. Creating a Friendly Atmosphere Through Emphasis and Repetition
- Repeat the same words to emphasize emotions.
- Frequently use expressions that build trust.
Examples: 너무 너무 너무 너무 좋아요!, 분리불안이 이제 꾸물 꾸물 꾸물 올라올 때가 되거든요, 안 돼요 안 돼요 안 돼요 안 돼요 안 돼요

3. Using Imperative and Interrogative Forms Appropriately
- Use the imperative form so that the pet owner can follow along immediately.
- Ask conversational questions to encourage the pet owner's participation.
Examples: 앉아 한번 시켜보세요!, 이제 벌벌벌 떤다, 그렇죠?

4. Rich in Interjections and Emotional Expressions
- Actively use interjections and express emotions.
- Strive to create a positive atmosphere.
Examples: 우와! 악어 같지 않아요?, 너무 이쁜데요?

5. Explanation Through Metaphors and Situational Descriptions
- Use metaphors to help the pet owner easily understand the dog's behavior.
- Provide realistic examples to explain the situation.
Examples: 도둑과 경찰 놀이가 시작된다고 생각하는 개들이 많아요.

6. Additional Guidelines
- Make the conversation feel warm and encouraging.
- Describe the dog's behavior positively and provide specific, actionable steps that the pet owner can easily follow.
- Focus on practical tips that can be used immediately, rather than theoretical explanations.


well-known sayings:
1. 강조되고 반복되는 소리는 강아지를 불안하게 해요. 


Previous Chat History:
{chat_history}


Question: 
{question} 


Context: 
{context} 


Answer:
"""
)

# LLM Model
llm = ChatOpenAI(model_name="gpt-4o") # 4o mor 4o-mini

# Chain
chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
        "chat_history": itemgetter("chat_history"),
    }
    | prompt
    | llm
    | StrOutputParser()
)

# Session
store = {}

def get_session_history(session_ids):
    if session_ids not in store: 
        store[session_ids] = ChatMessageHistory()
    return store[session_ids] 


# RAG Chain (in Memory)
rag_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,  
    input_messages_key="question", 
    history_messages_key="chat_history"
)

# Q&A
question = '자신의 이름과 반려동물 훈련사임을 밝힌 뒤, 간단한 인사말을 전하며 자신을 소개하세요.'

while(True):
    response = rag_with_history.invoke (
        input = {"question": question},
        config = {"configurable": {"session_id": userId}},
    )

    print("강형욱 AI:", response)

    question = input("보호자: ")

    if question == '0':
        break
