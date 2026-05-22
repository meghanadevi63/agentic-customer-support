from pathlib import Path
import json

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
import pandas as pd

#backend/rag/loaders.py
class KnowledgeLoader:

    def __init__(self,data_path:str):

        self.data_path=Path(data_path)


    def load_pdfs(self):

        documents=[]

        pdf_files=self.data_path.rglob("*.pdf")

        for pdf in pdf_files:

            try:

                loader=PyPDFLoader(str(pdf))

                docs=loader.load()

                for d in docs:

                    d.metadata["source"]=pdf.name
                    d.metadata["type"]="pdf"

                documents.extend(docs)

                print(f"Loaded PDF: {pdf.name}")

            except Exception as e:

                print(f"Error {pdf}:{e}")

        return documents


    def load_csv(self):

        documents=[]

        csv_files=self.data_path.rglob("*.csv")

        for csv_file in csv_files:

            try:

                df=pd.read_csv(csv_file)

                for _,row in df.iterrows():

                    content=" | ".join(
                        [f"{col}:{row[col]}" for col in df.columns]
                    )

                    documents.append(
                        Document(
                            page_content=content,
                            metadata={
                                "source":csv_file.name,
                                "type":"csv"
                            }
                        )
                    )

                print(f"Loaded CSV:{csv_file.name}")

            except Exception as e:

                print(e)

        return documents


    def load_json(self):

        documents=[]

        json_files=self.data_path.rglob("*.json")

        for file in json_files:

            try:

                with open(file,"r",encoding="utf8") as f:

                    data=json.load(f)

                for item in data:

                    text=json.dumps(item,indent=2)

                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source":file.name,
                                "type":"json"
                            }
                        )
                    )

                print(f"Loaded JSON:{file.name}")

            except Exception as e:

                print(e)

        return documents


    def load_all(self):

        docs=[]

        docs.extend(self.load_pdfs())

        docs.extend(self.load_csv())

        docs.extend(self.load_json())

        return docs