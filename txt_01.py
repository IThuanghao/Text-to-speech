from aip import AipSpeech
import os

# 配置百度智能云TTS参数（替换为你自己的API Key、Secret Key、App ID）
APP_ID = "txt"
API_KEY = "vybs1yYpmLG8EAXmLgNpEp4f"
SECRET_KEY = "EcmJmUXF0S55mIrtTNcpft9sfcN3VsEW"

# 初始化百度TTS客户端
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def read_txt_with_baidu_tts(txt_file_path, save_audio=False, audio_path="novel_audio.mp3"):
    """
    读取TXT文件，通过百度AI TTS实现自然朗读，可选保存音频文件
    :param txt_file_path: TXT文件路径
    :param save_audio: 是否保存朗读音频为MP3文件（默认不保存）
    :param audio_path: 保存音频的文件路径（默认novel_audio.mp3）
    """
    # 1. 读取TXT文件内容
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            # 百度TTS单次请求文本长度有限制（默认最多1024个字符），需分段读取
            novel_content = f.read()
        
        # 2. 分段处理文本（避免超过接口限制）
        chunk_size = 1000  # 每段1000个字符，留有余量
        novel_chunks = [novel_content[i:i+chunk_size] for i in range(0, len(novel_content), chunk_size)]
        
        # 3. 配置TTS参数（语音效果配置）
        tts_config = {
            'spd': 5,  # 语速（0-9，5为默认，数值越小语速越慢）
            'pit': 5,  # 音调（0-9，5为默认）
            'vol': 7,  # 音量（0-15，7为默认）
            'per': 0,  # 音色（0=男性，1=女性，3=情感男声，4=情感女声，更自然）
            'lan': 'zh',  # 语言（中文）
            'ctp': 1,  # 固定值，无需修改
        }
        
        # 4. 逐段生成语音并朗读/保存
        audio_data_list = []
        print("开始通过AI生成语音并朗读，按 Ctrl+C 可终止...")
        
        for chunk in novel_chunks:
            if not chunk.strip():
                continue
            
            # 调用百度TTS接口生成语音数据
            result = client.synthesis(chunk, 'zh', 1, tts_config)
            
            # 处理返回结果（成功返回二进制音频数据，失败返回字典）
            if not isinstance(result, dict):
                audio_data_list.append(result)
                
                # 直接播放音频（可选，需额外安装播放库：pip install playsound）
                # 这里优先支持保存音频，如需实时播放可补充playsound代码
            else:
                print(f"生成语音失败：{result.get('err_msg', '未知错误')}")
        
        # 5. 保存音频文件（如果开启保存）
        if save_audio and audio_data_list:
            with open(audio_path, 'wb') as audio_file:
                for audio_data in audio_data_list:
                    audio_file.write(audio_data)
            print(f"音频文件已保存至：{os.path.abspath(audio_path)}")
        
    except FileNotFoundError:
        print(f"错误：未找到指定的TXT文件 - {txt_file_path}")
    except UnicodeDecodeError:
        print(f"错误：TXT文件编码格式不正确，建议使用UTF-8编码")
    except Exception as e:
        print(f"未知错误：{str(e)}")

# 主程序调用
if __name__ == "__main__":
    TXT_FILE_PATH = "前端单词.txt"
    # 调用函数，开启保存音频功能（生成MP3文件，可后续播放）
    read_txt_with_baidu_tts(TXT_FILE_PATH, save_audio=True)