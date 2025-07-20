from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '../files/the_old_man_and_the_sea.txt')


#加载长文本
raw_documents = TextLoader(file_path,encoding="utf-8").load()

#实例化文本分割器
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)

#分割文本
documents = text_splitter.split_documents(raw_documents)

#未设置openAI的api_key，会报错
embeddings_model = OpenAIEmbeddings()


# 将分割后的文本，使用 OpenAI 嵌入模型获取嵌入向量，并存储在 Chroma 中
db = Chroma.from_documents(documents, embeddings_model)


query = "男孩子有没有请老人喝啤酒？"
docs = db.similarity_search(query)
print(docs[0].page_content)



### 使用嵌入向量进行语义相似度搜索
embedding_vector = embeddings_model.embed_query(query)
docs = db.similarity_search_by_vector(embedding_vector)
print(docs[0].page_content)