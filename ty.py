# import threading
# import time
# import webbrowser
# import sys
# import os
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# # Groq 임포트 체크
# try:
#     from groq import Groq
# except ImportError:
#     print("❌ groq 패키지가 설치되지 않았습니다!")
#     print("📦 설치 중...")
#     os.system("pip install groq")
#     from groq import Groq

# # 🔑 API 키 설정
# API_KEY = ""

# # API 키 확인
# if not API_KEY or len(API_KEY) < 20:
#     print("❌ 오류: API_KEY가 올바르지 않습니다!")
#     print("👉 코드 상단의 API_KEY 변수를 확인하세요.")
#     input("엔터를 눌러 종료...")
#     sys.exit(1)

# # Groq 클라이언트 초기화
# try:
#     client = Groq(api_key=API_KEY)
#     print("✅ Groq API 연결 성공!")
# except Exception as e:
#     print(f"❌ Groq 클라이언트 초기화 실패: {e}")
#     input("엔터를 눌러 종료...")
#     sys.exit(1)

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})  # CORS 설정 강화

# SELECTED_MODEL = "llama-3.3-70b-versatile"

# # 서버 상태 확인용
# server_running = False

# @app.route('/')
# def home():
#     """123.html 파일 연결"""
#     try:
#         html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '123.html')
#         with open(html_path, 'r', encoding='utf-8') as file:
#             return file.read()
#     except FileNotFoundError:
#         return """
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <meta charset="UTF-8">
#             <title>M&MC 챗봇</title>
#             <style>
#                 body { font-family: Arial; padding: 50px; text-align: center; background: #f5f5f5; }
#                 .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
#                 h1 { color: #0066ff; }
#                 .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
#             </style>
#         </head>
#         <body>
#             <div class="container">
#                 <h1>🚀 M&MC 챗봇</h1>
#                 <div class="status">✅ 서버가 정상적으로 실행 중입니다!</div>
#                 <p>⚠️ 123.html 파일을 찾을 수 없습니다.</p>
#                 <p>Python 파일과 같은 폴더에 123.html 파일을 넣어주세요.</p>
#                 <hr>
#                 <h2>💡 터미널 챗봇은 사용 가능합니다!</h2>
#                 <p>콘솔 창으로 돌아가서 질문을 입력하세요.</p>
#             </div>
#         </body>
#         </html>
#         """, 200

# @app.route('/health')
# def health():
#     """서버 상태 확인"""
#     return jsonify({'status': 'ok', 'server': 'running'}), 200

# @app.route('/ask', methods=['POST', 'OPTIONS'])
# def ask():
#     """웹 챗봇 API"""
#     # OPTIONS 요청 처리 (CORS preflight)
#     if request.method == 'OPTIONS':
#         response = jsonify({'status': 'ok'})
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#         response.headers.add('Access-Control-Allow-Methods', 'POST')
#         return response
    
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({'success': False, 'message': '잘못된 요청입니다.'}), 400
            
#         question = data.get('query', '').strip()
        
#         if not question:
#             return jsonify({'success': False, 'message': '질문을 입력해주세요.'}), 400
        
#         print(f"\n📩 받은 질문: {question}")
        
#         # Groq API 호출
#         response = client.chat.completions.create(
#             model=SELECTED_MODEL,
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "당신은 친절하고 유용한 AI 어시스턴트입니다. 한국어로 자연스럽게 답변해주세요."
#                 },
#                 {
#                     "role": "user",
#                     "content": question
#                 }
#             ],
#             temperature=0.7,
#             max_tokens=2048,
#             stream=False
#         )
        
#         answer = response.choices[0].message.content
#         print(f"✅ 답변 생성 완료!")
        
#         return jsonify({
#             'success': True,
#             'result': {'answer': answer}
#         }), 200
        
#     except Exception as e:
#         error_msg = str(e)
#         print(f"❌ API 오류: {error_msg}")
#         return jsonify({
#             'success': False, 
#             'message': f'오류가 발생했습니다: {error_msg}'
#         }), 500

# def terminal_chatbot():
#     """터미널 챗봇"""
#     print("\n" + "="*60)
#     print("🚀 Groq 터미널 챗봇 시작! (초고속 응답)")
#     print(f"🤖 사용 모델: {SELECTED_MODEL}")
#     print("💡 'quit' 또는 'q' 입력하면 종료")
#     print("🌐 웹버전: http://localhost:5000")
#     print("="*60)
    
#     conversation_history = []
    
#     while True:
#         try:
#             question = input("\n💬 질문: ").strip()
            
#             if question.lower() in ['quit', 'exit', '종료', 'q']:
#                 print("\n👋 챗봇을 종료합니다!")
#                 os._exit(0)
                
#             if question:
#                 print("🤖 답변 생성 중...", end='', flush=True)
                
#                 conversation_history.append({"role": "user", "content": question})
                
#                 response = client.chat.completions.create(
#                     model=SELECTED_MODEL,
#                     messages=[
#                         {
#                             "role": "system",
#                             "content": "당신은 친절하고 유용한 AI 어시스턴트입니다. 한국어로 자연스럽게 답변해주세요."
#                         }
#                     ] + conversation_history,
#                     temperature=0.7,
#                     max_tokens=2048,
#                     stream=False
#                 )
                
#                 answer = response.choices[0].message.content
#                 conversation_history.append({"role": "assistant", "content": answer})
                
#                 print("\r" + " "*50 + "\r", end='')  # 진행 메시지 지우기
#                 print(f"💡 답변:\n{answer}")
#             else:
#                 print("❓ 질문을 입력해주세요!")
                
#         except KeyboardInterrupt:
#             print("\n\n👋 챗봇을 종료합니다!")
#             os._exit(0)
#         except Exception as e:
#             print(f"\n❌ 오류: {e}")
#             print("💡 다시 시도해주세요.")

# def run_web_server():
#     """웹 서버 실행"""
#     global server_running
#     try:
#         print("🌐 Flask 서버 시작 중...")
#         server_running = True
#         app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False, threaded=True)
#     except OSError as e:
#         server_running = False
#         if "Address already in use" in str(e) or "10048" in str(e):
#             print("\n⚠️  포트 5000이 이미 사용 중입니다!")
#             print("💡 해결 방법:")
#             print("   1. 다른 Flask 서버를 종료하세요")
#             print("   2. 또는 작업 관리자에서 python.exe를 모두 종료하세요")
#         else:
#             print(f"\n❌ 서버 오류: {e}")
#     except Exception as e:
#         server_running = False
#         print(f"\n❌ 예상치 못한 서버 오류: {e}")

# def open_browser():
#     """브라우저 자동 실행"""
#     # 서버가 완전히 시작될 때까지 대기
#     for i in range(10):
#         time.sleep(0.5)
#         try:
#             import urllib.request
#             urllib.request.urlopen('http://localhost:5000/health', timeout=1)
#             break
#         except:
#             continue
    
#     try:
#         webbrowser.open('http://localhost:5000')
#         print("✅ 브라우저가 자동으로 열렸습니다!")
#     except Exception as e:
#         print(f"⚠️  브라우저 자동 실행 실패: {e}")
#         print("💡 수동으로 http://localhost:5000 에 접속하세요.")

# if __name__ == "__main__":
#     print("\n" + "="*60)
#     print("🚀 M&MC Groq 챗봇! (초고속 응답)")
#     print("="*60 + "\n")
    
#     # 웹 서버를 백그라운드에서 실행
#     web_thread = threading.Thread(target=run_web_server, daemon=True)
#     web_thread.start()
    
#     # 서버 시작 대기
#     time.sleep(2)
    
#     if server_running:
#         print("✅ 웹 서버 실행됨: http://localhost:5000")
        
#         # 브라우저 자동 실행
#         browser_thread = threading.Thread(target=open_browser, daemon=True)
#         browser_thread.start()
#     else:
#         print("⚠️  웹 서버 시작 실패 - 터미널 챗봇만 사용 가능합니다.")
    
#     print("\n" + "="*60)
    
#     # 터미널 챗봇 시작
#     try:
#         terminal_chatbot()
#     except Exception as e:
#         print(f"\n❌ 심각한 오류 발생: {e}")
#         input("엔터를 눌러 종료...")
#         os._exit(1)

import threading
import time
import webbrowser
import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Groq 임포트 체크
try:
    from groq import Groq
except ImportError:
    print("❌ groq 패키지가 설치되지 않았습니다!")
    print("📦 설치 중...")
    os.system("pip install groq")
    from groq import Groq

# 🔑 환경변수에서 API 키 가져오기
API_KEY = os.getenv("GROQ_API_KEY")

# API 키 확인
if not API_KEY or len(API_KEY) < 20:
    print("❌ 오류: GROQ_API_KEY가 설정되지 않았습니다!")
    print("👉 .env 파일을 생성하고 다음과 같이 작성하세요:")
    print("   GROQ_API_KEY=your_api_key_here")
    print("\n💡 .env 파일은 app.py와 같은 폴더에 있어야 합니다.")
    input("엔터를 눌러 종료...")
    sys.exit(1)

# Groq 클라이언트 초기화
try:
    client = Groq(api_key=API_KEY)
    print("✅ Groq API 연결 성공!")
except Exception as e:
    print(f"❌ Groq 클라이언트 초기화 실패: {e}")
    input("엔터를 눌러 종료...")
    sys.exit(1)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

SELECTED_MODEL = "llama-3.3-70b-versatile"

# 서버 상태 확인용
server_running = False

@app.route('/')
def home():
    """123.html 파일 연결"""
    try:
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '123.html')
        with open(html_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>M&MC 챗봇</title>
            <style>
                body { font-family: Arial; padding: 50px; text-align: center; background: #f5f5f5; }
                .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
                h1 { color: #0066ff; }
                .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 M&MC 챗봇</h1>
                <div class="status">✅ 서버가 정상적으로 실행 중입니다!</div>
                <p>⚠️ 123.html 파일을 찾을 수 없습니다.</p>
                <p>Python 파일과 같은 폴더에 123.html 파일을 넣어주세요.</p>
                <hr>
                <h2>💡 터미널 챗봇은 사용 가능합니다!</h2>
                <p>콘솔 창으로 돌아가서 질문을 입력하세요.</p>
            </div>
        </body>
        </html>
        """, 200

@app.route('/health')
def health():
    """서버 상태 확인"""
    return jsonify({'status': 'ok', 'server': 'running'}), 200

@app.route('/ask', methods=['POST', 'OPTIONS'])
def ask():
    """웹 챗봇 API"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': '잘못된 요청입니다.'}), 400
            
        question = data.get('query', '').strip()
        
        if not question:
            return jsonify({'success': False, 'message': '질문을 입력해주세요.'}), 400
        
        print(f"\n📩 받은 질문: {question}")
        
        # Groq API 호출
        response = client.chat.completions.create(
            model=SELECTED_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "당신은 친절하고 유용한 AI 어시스턴트입니다. 한국어로 자연스럽게 답변해주세요."
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.7,
            max_tokens=2048,
            stream=False
        )
        
        answer = response.choices[0].message.content
        print(f"✅ 답변 생성 완료!")
        
        return jsonify({
            'success': True,
            'result': {'answer': answer}
        }), 200
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ API 오류: {error_msg}")
        return jsonify({
            'success': False, 
            'message': f'오류가 발생했습니다: {error_msg}'
        }), 500

def terminal_chatbot():
    """터미널 챗봇"""
    print("\n" + "="*60)
    print("🚀 Groq 터미널 챗봇 시작! (초고속 응답)")
    print(f"🤖 사용 모델: {SELECTED_MODEL}")
    print("💡 'quit' 또는 'q' 입력하면 종료")
    print("🌐 웹버전: http://localhost:5000")
    print("="*60)
    
    conversation_history = []
    
    while True:
        try:
            question = input("\n💬 질문: ").strip()
            
            if question.lower() in ['quit', 'exit', '종료', 'q']:
                print("\n👋 챗봇을 종료합니다!")
                os._exit(0)
                
            if question:
                print("🤖 답변 생성 중...", end='', flush=True)
                
                conversation_history.append({"role": "user", "content": question})
                
                response = client.chat.completions.create(
                    model=SELECTED_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": "당신은 친절하고 유용한 AI 어시스턴트입니다. 한국어로 자연스럽게 답변해주세요."
                        }
                    ] + conversation_history,
                    temperature=0.7,
                    max_tokens=2048,
                    stream=False
                )
                
                answer = response.choices[0].message.content
                conversation_history.append({"role": "assistant", "content": answer})
                
                print("\r" + " "*50 + "\r", end='')
                print(f"💡 답변:\n{answer}")
            else:
                print("❓ 질문을 입력해주세요!")
                
        except KeyboardInterrupt:
            print("\n\n👋 챗봇을 종료합니다!")
            os._exit(0)
        except Exception as e:
            print(f"\n❌ 오류: {e}")
            print("💡 다시 시도해주세요.")

def run_web_server():
    """웹 서버 실행"""
    global server_running
    try:
        print("🌐 Flask 서버 시작 중...")
        server_running = True
        app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False, threaded=True)
    except OSError as e:
        server_running = False
        if "Address already in use" in str(e) or "10048" in str(e):
            print("\n⚠️  포트 5000이 이미 사용 중입니다!")
            print("💡 해결 방법:")
            print("   1. 다른 Flask 서버를 종료하세요")
            print("   2. 또는 작업 관리자에서 python.exe를 모두 종료하세요")
        else:
            print(f"\n❌ 서버 오류: {e}")
    except Exception as e:
        server_running = False
        print(f"\n❌ 예상치 못한 서버 오류: {e}")

def open_browser():
    """브라우저 자동 실행"""
    for i in range(10):
        time.sleep(0.5)
        try:
            import urllib.request
            urllib.request.urlopen('http://localhost:5000/health', timeout=1)
            break
        except:
            continue
    
    try:
        webbrowser.open('http://localhost:5000')
        print("✅ 브라우저가 자동으로 열렸습니다!")
    except Exception as e:
        print(f"⚠️  브라우저 자동 실행 실패: {e}")
        print("💡 수동으로 http://localhost:5000 에 접속하세요.")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 M&MC Groq 챗봇! (초고속 응답)")
    print("="*60 + "\n")
    
    # 웹 서버를 백그라운드에서 실행
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # 서버 시작 대기
    time.sleep(2)
    
    if server_running:
        print("✅ 웹 서버 실행됨: http://localhost:5000")
        
        # 브라우저 자동 실행
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
    else:
        print("⚠️  웹 서버 시작 실패 - 터미널 챗봇만 사용 가능합니다.")
    
    print("\n" + "="*60)
    
    # 터미널 챗봇 시작
    try:
        terminal_chatbot()
    except Exception as e:
        print(f"\n❌ 심각한 오류 발생: {e}")
        input("엔터를 눌러 종료...")
        os._exit(1)