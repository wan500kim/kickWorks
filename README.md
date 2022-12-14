## **kickWorks 비속어 순화 필터**

해당 프로젝트는 딥러닝을 통한 비속어 필터링 서비스를 제공합니다.

웹에서 구동되며 비속어로 판단된 어절을 같은 글자 수의 **순화된 단어로 치환**합니다.

#### 시연 영상 (클릭하여 재생)

<img src="https://user-images.githubusercontent.com/74997157/206859407-3415445a-2927-48ef-b488-6eb8ca26bba9.gif"/>

---
### 설치 방법
웹 기반 동작이므로 별도의 설치 방법이 없습니다.

---
### 의존성
- python : v3.9.X
- Web browser : Chrome(recommend)

```
fasttext==0.9.2
gensim==4.2.0
hgtk==0.1.3
joblib==1.2.0
keras==2.10.0
Keras-Preprocessing==1.1.2
numpy==1.23.4
pandas==1.5.1
flask==2.2.2
```

---
### 실행 방법
1. app.py 실행
2. 실행 시 출력되는 https://0.0.0.0:2278/ 로 접속
3. 입력 창에 필터링하고자 하는 문장을 입력
4. 종료하려면 '/종료'를 입력
---

### License
```
MIT License

Copyright (c) 2022 kickWorks

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

---
### Contributors
- YoungChan-Park, adap8709@gmail.com
- WanSoo-Kim, dhkstn0219@gmail.com
