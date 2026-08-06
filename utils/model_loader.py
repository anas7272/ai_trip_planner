import os
from dotenv import load_dotenv
from typing import Literal , Optional , Any
from pydantic import BaseModel , Field
from utils.config_loader import load_config
from langcchain_groq import ChatGroq
from langcchain_openai import ChatOpenAI

class ConfigLoader:
    def __init__(self):
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider : Literal["openai" , "groq"] = "groq"
    config : Optional[ConfigLoader] = Field(default = None , exclude=True)

    def model_post_init(self, context):
        self.config = ConfigLoader()

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        "load and return llm model"
        print(f"Loading LLM model with provider: {self.model_provider}")
        if self.model_provider == "groq":
            print("loading llm from groq...")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config["llm"]["groq"]["model_name"]
            llm = ChatGroq(api_key=groq_api_key, model_name=model_name)
        elif self.model_provider == "openai":
            print("loading llm from openai...")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(api_key=openai_api_key, model_name=model_name)

        return llm