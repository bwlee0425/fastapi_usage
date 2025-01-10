import requests

url = 'http://127.0.0.1:8000/upload/'  # FastAPI 서버 URL 및 엔드포인트
# files = {'file': open('a.jpg', 'rb')}  # 파일 열기
files = {'file': ('lion.jpg', open('lion.jpg', 'rb'), 'image/jpeg')}  # Content-Type 명시

response = requests.post(url, files=files)  # POST 요청 보내기

if response.status_code == 200:
    with open('response_image.png', 'wb') as f:
        f.write(response.content)  # 받은 이미지 저장
    print("이미지가 성공적으로 처리되어 'response_image.png'로 저장되었습니다.")
else:
    print("에러:", response.status_code, response.text)