import streamlit as st
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

st.title("🌍 Neural Machine Translation (Fine-Tuned T5 Model)")
st.write("Translate English → French using your fine-tuned T5-small model.")
# -----------------------
# Load Model & Tokenizer
# -----------------------
path= "Dhineshsakthivel/translator-t5-finetuned" 

@st.cache_resource
def load_model():
    model = T5ForConditionalGeneration.from_pretrained(path,local_files_only=False)
    tokenizer = T5Tokenizer.from_pretrained(path,local_files_only=False)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    return model, tokenizer, device

model, tokenizer, device = load_model()

# -----------------------
# Translation Function
# -----------------------
def translate(sentence):
    # ALWAYS add T5 prefix
    prefixed = "translate English to French: " + sentence

    encoded = tokenizer(prefixed, return_tensors="pt").to(device)

    with torch.no_grad():
        output = model.generate(
            encoded.input_ids,
            max_length=128,
            num_beams=4,
            do_sample=False,
            early_stopping=True
        )

    return tokenizer.decode(output[0], skip_special_tokens=True)

# -----------------------
# Streamlit UI
# -----------------------
text = st.text_area("Enter English text:")

if st.button("Translate"):
    if text.strip() == "":
        st.warning("Please enter some text!")
    else:
        translation = translate(text)
        st.success("Translation:")
        st.write(translation)
