from flask import Flask
from flask import request
from BananaKickRun import *
from gensim.models import FastText
from keras.models import load_model

app = Flask(__name__)

embedding_model = FastText.load("./Fasttext.model")
cnn_model = load_model("./CNN_model")

@app.route("/", methods=['GET', 'POST'])
def test():
    instr = request.form.get("instr")
    #입력받겠다
    if instr is not None:
        global result
        result = str(bananaKick(instr))
        #입력 값이 있으면 result에 저장

    else:
        result = str()
        #입력 값이 없으면 null 출력
	
    return(
		"""<form action="" method="post">
				input : <input type="text" name="instr">
				<input type="submit" value="입력">
			</form>"""
		+ "output:" + result
	)#get 메소드로 입력받는다는 뜻
     #input이라는 칸은 text형식 입력받고 변수명은 instr
     #제출해야 입력되는 형식이고 submit 버튼을 누르면 값이 입력됨
     #input : 옆에 입력값 출력

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=2278)
