from transformers import pipeline
from app.pipeline.generator.base_generator import BaseGenerator
from app.pipeline.generator.prompt_builder import PromptBuilder

from scripts.utils.config import CONFIG
class HuggingFaceGenerator(BaseGenerator):
    def __init__(self, model_name= CONFIG.get("generator_settings.model_name"), prompt_mode="default"):
        self.generator = pipeline("text-generation", model=model_name)
        self.prompt_builder = PromptBuilder()
        self.mode = prompt_mode

    def generate(self, question, context_docs):
        prompt = self.prompt_builder.build(question, context_docs, mode=self.mode)
        output = self.generator(prompt, max_new_tokens=200, do_sample=True)[0]["generated_text"]
        return output.split("Answer:")[-1].strip()
