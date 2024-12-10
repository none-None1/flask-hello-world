from flask import *
from uuid import uuid4
from look import mid2notes,notes2brainfuck
from os import remove
def rand_fn(): #随机文件名
    return str(uuid4())+'.mid'
def err(msg,red): #发送错误消息
    flash(msg)
    return redirect(red)
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16777216 #最大大小：16MiB
app.secret_key='a'
@app.route('/')
def home(): #主页
    return render_template('index.html')


@app.route('/l2b')
def l2b(): #Look!转brainfuck功能
    return render_template('l2b.html')
@app.route('/upload_l2b', methods=['POST'])
def upload_l2b(): #上传文件
    if 'file' not in request.files: #必须有文件信息
        return err('No file part','/l2b')
    f=request.files['file']
    if f.filename=='': #必须有文件
        return err('No file uploaded','/l2b')
    if not f.filename.endswith('.mid'): #必须是MIDI文件
        return err('Only MIDI files may be uploaded','/l2b')
    fn='uploads/'+rand_fn()
    f.save(fn)
    bf=notes2brainfuck(mid2notes(fn))
    print(bf)
    remove(fn)
    return render_template('l2b_result.html',code=bf)
