import sys, configparser                    # 시스템 관련 기능과 설정 파일을 읽기 위한 모듈 임포트
from openai import OpenAI                   # OpenAI API를 사용하기 위한 라이브러리 임포트

from PyQt6 import uic, QtWidgets            # PyQt6의 UI 컴포넌트와 유틸리티 임포트
from PyQt6.QtWidgets import QMessageBox     # ✅ 사용자 경고 메시지를 위한 팝업 창 클래스 임포트

# 설정 파일(config.ini) 읽기
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8') # UTF-8 인코딩으로 config.ini 파일 읽기
OPENAI_API_KEY = config['OpenAI']['api_key']          # API 키 불러오기
MODEL_NAME = config['OpenAI'].get('model', 'gpt-3.5-turbo')  # 모델명 설정, 없으면 기본값 사용
PROMPTS = dict(config['Prompts'])                     # 프롬프트(카테고리별 시스템 메시지) 딕셔너리로 변환

# OpenAI 클라이언트 객체 생성
client = OpenAI(api_key=OPENAI_API_KEY)

# PyQt6 애플리케이션 초기화
app = QtWidgets.QApplication(sys.argv)     # QApplication 객체 생성
MainWindow = QtWidgets.QMainWindow()       # 메인 윈도우 생성
uic.loadUi('chatbot_with_button.ui', MainWindow)  # Qt Designer에서 만든 .ui 파일 불러오기

# [핵심 함수] 질문 전송 및 응답 처리 함수 정의
def handle_send():
  category = MainWindow.categoryCombo.currentText()         # 현재 선택된 카테고리 텍스트 가져오기
  question = MainWindow.questionInput.text().strip()        # 입력된 질문 텍스트 가져오기 및 공백 제거
  if not question:                                          # 질문이 비어 있으면
    QMessageBox.warning(MainWindow, "입력 오류", "질문을 입력하세요.")  # ✅ 경고 팝업 창 띄우기
    MainWindow.questionInput.setFocus()                   # 질문 입력창에 포커스 다시 맞추기
    return                                               # 함수 종료

  system_prompt = PROMPTS.get(category, "당신은 친절한 어시스턴트입니다.")  # 선택된 카테고리의 시스템 메시지 가져오기
  messages = [                                               # ChatGPT 메시지 형식 구성
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": question}
  ]  


# 윈도우 기본 설정 및 이벤트 연결
MainWindow.setWindowTitle("ChatGPT LLM App")                     # 창 제목 설정
MainWindow.sendButton.clicked.connect(handle_send)               # 전송 버튼 클릭 시 handle_send 함수 실행
MainWindow.questionInput.returnPressed.connect(handle_send)      # ✅ 엔터키로 질문 전송 가능하게 연결
MainWindow.clearButton.clicked.connect(lambda: MainWindow.questionInput.clear())  # ✅ 초기화 버튼 클릭 시 입력창 비우기


MainWindow.categoryCombo.addItems(PROMPTS.keys())                # 카테고리 콤보박스에 프롬프트 키 추가
MainWindow.questionInput.returnPressed.connect(handle_send)      # 질문 입력창에서 엔터키 입력 시 handle_send 함수 실행 -(중복이지만 문제 없음) 엔터 입력 이벤트 연결

MainWindow.show()          # 메인 윈도우 표시
sys.exit(app.exec())       # 애플리케이션 실행 및 종료 처리