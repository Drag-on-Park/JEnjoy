# JEnjoy v 0.1.0

일본어 학습을 위한 웹 애플리케이션입니다. 사용자는 말하기, 읽기, 쓰기, 단어 학습 등 다양한 방법으로 일본어를 공부할 수 있습니다.

**Home**
<img width="1708" alt="JENJOY_Home_1202" src="https://github.com/user-attachments/assets/1396dd6c-81cf-439b-977c-68deb7afd552">

**Nav**
<img width="1706" alt="nav_1129" src="https://github.com/user-attachments/assets/e7cca380-7241-44b7-bf59-2dffe2f94047">

## 주요 기능

- **Speak:** 사용자가 일본어 단어를 듣고 따라 말하면 음성 인식을 통해 정확도를 측정하고 피드백을 제공합니다.
- **Read:** 일본어 지문을 읽고 이해하는 능력을 기릅니다. (구현 예정)
- **Write:** 사용자가 일본어 글자를 손글씨로 쓰면, 딥러닝 모델을 통해 글자의 정확도를 측정하고 피드백을 제공합니다. (구현 예정)
- **Dictionary:**
    - **오늘의 단어:** 매일 새로운 일본어 단어를 학습하고, 빈칸 채우기 퀴즈를 통해 복습할 수 있습니다.
    - **단어 검색:** 한국어 또는 일본어로 단어를 검색하여 뜻, 발음, 품사, JLPT 급수 등의 정보를 확인할 수 있습니다.
    - **십자말풀이:** 매일 새로운 십자말풀이를 통해 단어 학습을 재미있게 할 수 있습니다. (구현 중)
- **Jenmon:** 학습 진행에 따라 펫이 성장하고, 다양한 아이템으로 펫을 꾸밀 수 있습니다. (구현 예정)
- **Board:** 자유롭게 소통할 수 있는 게시판입니다.
- **User:** 사용자 정보 확인 및 수정을 할 수 있습니다.

## 기술 스택

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite3
- **Deep Learning:** (Write 기능 구현 시 사용 예정)
- **Speech Recognition:** (Speak 기능 구현 시 사용 예정)

## Planning

- **Speak:** 음성인식 API를 활용하여 사용자의 발음 정확도를 측정하고 점수와 피드백을 제공하는 기능을 구현할 예정입니다.
- **Listen:** 일본어 음성을 듣고 받아쓰기나 퀴즈를 통해 학습하는 기능을 추가할 예정입니다.
- **Write:** 딥러닝 모델을 활용하여 사용자의 손글씨를 인식하고 정확도를 측정하는 기능을 구현할 예정입니다.
- **Jenmon:** 학습량에 따라 펫이 레벨업하고 외형이 변하며, 다양한 의상과 액세서리를 추가하는 기능을 구현할 예정입니다.
- **실시간 순위:** 사용자들의 학습 성과를 바탕으로 실시간 순위를 보여주는 기능을 추가할 예정입니다.
- **Daily Challenges:** 매일 새로운 학습 목표를 제공하여 꾸준한 학습을 유도하는 기능을 추가할 예정입니다.

## Source

### **Images**
- [220 lively doodling illustrations](https://www.figma.com/community/file/1093160816660454395/220-lively-doodling-illustrations-manila-vector-illustrations-set-svg-png)
- [Free 75 illustrations by Surface pack](https://www.figma.com/community/file/883778082594341562/free-75-illustrations-surface-pack)
- [Eggradients - Gradient Collection](https://www.figma.com/community/file/1012332624512867414/eggradients-gradient-collection)

### **Dictionary**
- 네이버 사전
- GPT
- https://gaigokugo.tistory.com/

### **Kana**
- [가타카나 - 나무위키](https://namu.wiki/w/%EA%B0%80%ED%83%80%EC%B9%B4%EB%82%98)
- [히라가나 - 나무위키](https://namu.wiki/w/%ED%9E%88%EB%9D%BC%EA%B0%80%EB%82%98)
- https://blog.naver.com/jewel12200/222172887463