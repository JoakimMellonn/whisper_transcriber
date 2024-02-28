# whisper_transcriber
You can download this quick and dirty python script to quickly transcribe an audio file with the use of the OpenAI Whisper Large v3 model. All processing is done LOCALLY, so no data will leave your machine.

## Prerequisites
- Python should of course be installed.

Run the following commands, you should be able to copy/paste the entire block:
```shell
pip install --upgrade pip
pip install --upgrade git+https://github.com/huggingface/transformers.git accelerate datasets\[audio\]
pip install ffmpeg-python
```

## Usage
Clone the repository:
```shell
git clone https://github.com/JoakimMellonn/whisper_transcriber.git
```

I the directory it's been cloned into, place the file to transcribe.
Now just run the script from a terminal in the directory:
```shell
python whisper.py
```

It will ask for the relative path to the input file, if you've placed the file in the same directory as the script just write the full name of the file.
```shell
example_audio.mp3
```

Now just wait for the magic to happen. The first time running the script, it will download the model, which can take some time. After that the process can take quite some time depending on the hardware (M1 Pro MacBook Pro took x minutes).
