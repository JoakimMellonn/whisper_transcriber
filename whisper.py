import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
import ffmpeg
import os
import json

print("Please specify relative path to input file:")
inputPath = str(input())

while not inputPath:
    print("You have to enter something...")
    inputPath = str(input())


inputName = inputPath.split(".")[0]
inputType = inputPath.split(".")[-1]
if inputType not in ["mp3", "flac", "wav"]:
    print("Not a supported format, converting file...")
    if os.path.exists("temp.wav"):
        os.remove("temp.wav")
    stream = ffmpeg.input(inputPath)
    stream = ffmpeg.output(stream, "temp.wav")
    ffmpeg.run(stream)
    inputPath = "temp.wav"

# Do the AI magic
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)

dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")

result = pipe(inputPath, return_timestamps=True)

jf = open("output.json", "a")
jf.write(json.dumps({"result": result["chunks"]}))
jf.close()

f = open("output.txt", "a")
f.write(result["text"])
f.close()

if inputPath == "temp.wav":
    os.remove("temp.wav")

print("DONE! Wrote raw result to output.txt and with timestamps to output.json")
