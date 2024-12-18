import moviepy.editor as mp  # Corrigido para importar o módulo correto do moviepy
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
import sys

# Defina o caminho do vídeo
path = "./onyx_ete.mp4"

# Carregue o vídeo e extraia o áudio
clip = mp.VideoFileClip(path)  # Carregue o vídeo completo
clip.audio.write_audiofile("./audio.mp3")  # Gere o arquivo de áudio MP3

# Carregar o áudio
audio = AudioSegment.from_file("./audio.mp3", "mp3")  # Caminho correto para o arquivo de áudio

# Tamanho do corte em milissegundos (exemplo: 3 minutos)
size = 180000  # 180000 ms = 3 minutos

# Divida o áudio em pedaços
chunks = make_chunks(audio, size)

# Itere pelos pedaços do áudio
for i, chunk in enumerate(chunks):
    # Nome do arquivo de saída
    chunk_name = f"audio{i}.wav"  # Nome do arquivo para o pedaço de áudio
    
    # Exporte o pedaço para WAV
    chunk.export(chunk_name, format="wav")
    
    # Abrir o arquivo de áudio para reconhecimento
    file_audio = sr.AudioFile(chunk_name)
    
    # Crie o reconhecedor de fala
    r = sr.Recognizer()
    
    try:
        with file_audio as source:
            audio_text = r.record(source)  # Capture o áudio do arquivo
            text = r.recognize_google(audio_text, language='pt-BR')  # Converta para texto (Português)
        
        # Salve o texto reconhecido em um arquivo .txt
        with open(chunk_name.replace('.wav', '.txt'), 'w', encoding='utf-8') as arq:  # Abertura com encoding
            arq.write(text)
        
        print(f"Texto do {chunk_name}: {text}")  # Exiba o texto no terminal

    except sr.UnknownValueError:
        print(f"Não foi possível reconhecer o áudio no arquivo {chunk_name}")
    except sr.RequestError as e:
        print(f"Erro de requisição ao serviço de reconhecimento de fala: {e}")
