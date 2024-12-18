import moviepy as mp
import speech_recognition as sr

# Função para extrair áudio do vídeo
def extract_audio_from_video(video_file):
    video = mp.VideoFileClip(video_file)
    audio = video.audio
    audio_file = "extracted_audio.wav"
    audio.write_audiofile(audio_file)
    return audio_file

# Função para transcrever áudio
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    audio_file_path = audio_file

    with sr.AudioFile(audio_file_path) as source:
        print("Ajustando para o ruído ambiente... por favor, espere.")
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Ajuste mais longo para melhorar a calibração do ruído
        print("Capturando áudio...")

        # Captura o áudio
        audio = recognizer.record(source)

    try:
        print("Reconhecendo o que foi dito...")
        # Converte o áudio para texto usando o Google Web Speech API
        text = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Texto transcrito: {text}")
        return text
    except sr.UnknownValueError:
        print("Não consegui entender o áudio. Por favor, fale mais claramente.")
        return None
    # except sr.RequestError as e:
    #     print(f"Ocorreu um erro na requisição ao serviço de reconhecimento de fala: {e}")
    #     return None
    except Exception as e:
        print(f"Erro inesperado durante o reconhecimento de fala: {e}")
        return None

# Função principal para transcrição de vídeo
def transcribe_video(video_file):
    print("Extraindo áudio do vídeo...")
    audio_file = extract_audio_from_video(video_file)
    print(f"Áudio extraído e salvo como {audio_file}. Iniciando transcrição...")
    transcribe_audio(audio_file)

# Exemplo de uso
video_file = "ete_piracaia.mp4"  # Substitua pelo caminho do seu arquivo de vídeo
transcribe_video(video_file)
