from transformers import AutoTokenizer, AutoModel, Trainer, TrainingArguments
from peft import get_peft_model, LoraConfig, TaskType
import torch
from torch import nn

from app.jobs.fine_tune_prep import get_query_text_pairs
from app.jobs.train_dataset import DualEncoderDataset
from scripts.utils.config import CONFIG

class ContrastiveTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):

        # Encode queries and documents
        q_inputs = inputs["query_input"]
        d_inputs = inputs["doc_input"]

        q_embeds = model(**q_inputs).last_hidden_state[:, 0] # CLS token
        d_embeds = model(**d_inputs).last_hidden_state[:, 0]

        # Normalize for cosine similarity
        q_embeds = nn.functional.normalize(q_embeds, p=2, dim=-1)
        d_embeds = nn.functional.normalize(d_embeds, p=2, dim=-1)

        # Compute cosine similarity matrix
        logits = q_embeds @ d_embeds.T
        labels = torch.arange(logits.size(0), device=logits.device)

        # Compute contrastive loss
        loss = nn.CrossEntropyLoss()(logits, labels)
        print("q_embeds:", q_embeds.shape)
        print("d_embeds:", d_embeds.shape)
        print("logits:", logits)
        print("labels:", labels)


        return (loss, logits) if return_outputs else loss

def collate_fn(batch):
    # stack the query and doc inputs separately
    query_input = {
        k: torch.stack([sample["query_input"][k] for sample in batch])
        for k in batch[0]["query_input"]
    }

    doc_input = {
        k: torch.stack([sample["doc_input"][k] for sample in batch])
        for k in batch[0]["doc_input"]
    }

    return {
        "query_input": query_input,
        "doc_input": doc_input,
    }


def main():
    #Load the tokenizer 
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    #Load query-doc pairs
    query_doc_pairs = get_query_text_pairs(n=500)

    #Create the dataset
    dataset = DualEncoderDataset(query_doc_pairs=query_doc_pairs, 
                                 tokenizer=tokenizer,
                                 max_length=128)
    
    model = AutoModel.from_pretrained(model_name)

    # Define LoRA configuration
    peft_config = LoraConfig(
        task_type=TaskType.FEATURE_EXTRACTION,
        inference_mode=False,
        r=8,
        lora_alpha=16,
        lora_dropout=0.1
    )

    # Wrap the model with LoRA
    model = get_peft_model(model, peft_config)

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./models/encoder_lora_v1",
        per_device_train_batch_size=32,
        num_train_epochs=3,
        learning_rate=5e-5,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=10,
        save_steps=100,
        save_total_limit=1,
        eval_strategy="no",  
        remove_unused_columns=False,  
        fp16=torch.cuda.is_available()
    )

    trainer = ContrastiveTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer,
        data_collator=collate_fn,
    )

    trainer.train()

if __name__ == "__main__":
    main()



