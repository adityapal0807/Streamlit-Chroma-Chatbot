import pandas as pd
from typing import Optional, Union, List, Tuple
import chromadb 
from chromadb.config import Settings
import os
import re
import logging
from dotenv import load_dotenv

load_dotenv()




# Set up logging
logging.basicConfig(level=logging.INFO)
from langchain.text_splitter import RecursiveCharacterTextSplitter

class ChromaRAG:
    """Class to create and manage a collection in a chromadb database."""
    
    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Initialize the CreateCollection class.

        Args:
            collection_name (str): The name of the collection to be created or managed.
            db_path (Optional[str]): The path to the database. Defaults to './db' if None.
        """
        self.db_path = db_path if db_path else './db'
        self.EXISTING_DB = False
        self.client = chromadb.PersistentClient(path=self.db_path, settings=Settings(allow_reset=True))
        self.splitter = RecursiveCharacterTextSplitter(
                chunk_size = 256,
                chunk_overlap  = 0,
                length_function = len,
            )

    ##WHAT Functions i want 
    # Function to upload a file,create a collection , chunk the data in file , then upload in chroma as a collection.

    def chunk_text(self,text):
        chunks = self.splitter.split_text(text)
        return chunks

    def all_collections(self):
        return self.client.list_collections()
    
    def get_collection(self,collection_name: str):
        logging.info(self.client.list_collections())
        collection = self.client.get_collection(name=collection_name)
        return collection
    
    
    def create_collection(self, collection_name: str,chunks):
        """Create a new collection in the database."""
        # client.reset()
        try:
            collection = self.client.get_collection(name=collection_name)
            logging.info("Database exists.")
            self.EXISTING_DB = True
        except:
            # self.client.reset()
            logging.info('Creating database...')
            collection = self.client.create_collection(collection_name)
            collection.add(documents=chunks,ids=[f"id{index}" for index,value in enumerate(chunks)])
            self.EXISTING_DB = False
        return collection
    
                
    def run_query(self,collection, query: str) -> List[Tuple]:
        """Run a query against the collection."""
        results = collection.query(query_texts=[query], n_results=10)

        return results.get('documents')


rag = ChromaRAG()