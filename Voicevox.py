import requests
import json

class Voicevox:
    def __init__(self, host='localhost', port=50021):
        self.url  = f'http://{host}:{port}'
        try:
            response = requests.get(f"{self.url}/version")
            response.raise_for_status()
            print("Voicevox APIに正常に接続されました。")
        except requests.exceptions.ConnectionError:
            print("Voicevox APIに接続できませんでした。Voicevoxアプリケーションが起動していることを確認してください。")
        except requests.exceptions.HTTPError:
            print("Voicevox APIへの接続中にエラーが発生しました。ホストとポート番号を正しく指定しているか確認してください。")

    def post_data(self, url, header_param, params_param, data_param):
        ret = requests.post(
            url,
            headers = header_param,
            params = params_param,
            data = data_param,
        )
        if ret.status_code != 200:
            print("Error occurred during API request. Status code:", response.status_code)
            try:
                error_response = ret.json()
                print("Error response:", error_response)
            except json.JSONDecodeError:
                print("Unable to parse error response as JSON.")
            
        return ret

    def generate(self, text, speaker_id=1,wav_file_name='voicevox_audio.wav'):
        
        params = (
            ('text', text),
            ('speaker', speaker_id),
        )
        
        response1 = self.post_data(f'{self.url}/audio_query',None,params,None)

        headers = {'Content-Type': 'application/json',}
        response2 = self.post_data(f'{self.url}/synthesis',headers,params,json.dumps(response1.json()))
        
        with open(wav_file_name, 'wb') as f:
            f.write(response2.content)

        # TODO: Play the audio using a suitable audio player library

        print("Audio playback complete.")

if __name__ == "__main__":
    # Voicevoxアプリケーションのホストとポート番号を設定
    host = 'localhost'
    port = 50021

    # テキストを指定して音声を再生
    voicevox = Voicevox()
    voicevox.generate("きょうもつかれてしんどい", speaker_id=1)
