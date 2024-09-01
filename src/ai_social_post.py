from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.ollama import OllamaEmbeddings

# Initialize the Ollama embeddings and model
embeddings = OllamaEmbeddings(model="qwen:0.5b")
llm = Ollama(model="qwen:0.5b")

# Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a social media manager who writes social media posts on the topic provided as input."),
    ("user", "{input}"),
    ("agent_scratchpad", 'assistant'),
    ("tool_names", "{retriever_tool}"),
    ("tools", "{retriever_tool}")
])

# Load documents from a file
loader = TextLoader("./readme.md", encoding='utf-8')
raw_docs = loader.load()

# Split documents into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(raw_docs)

# Create a vector store and retriever
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

# Create a retriever tool
retriever_tool = create_retriever_tool(retriever, name="web_search", description="Search the web for relevant information.")

# Create an agent executor
agent = create_react_agent(llm=llm, tools=[retriever_tool], prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=[retriever_tool], verbose=True)

# Run the agent with an input
input_data = {"input": "What is LangChain?"}
output = agent_executor.invoke(input_data)
print(output)
