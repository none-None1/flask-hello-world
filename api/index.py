from os import environ,chdir
from os.path import dirname
from io import BytesIO
from mido import MidiFile,MidiTrack,Message,MetaMessage,bpm2tempo
from random import *
import sys
def bf(code):
    s=[]
    matches={}
    tape=[0]*1000000
    for i,j in enumerate(code):
        if j=='[':
            s.append(i)
        if j==']':
            m=s.pop()
            matches[m]=i
            matches[i]=m
    cp=0
    p=0
    while cp<len(code):
        if code[cp]=='+':
            tape[p]=(tape[p]+1)%256
        if code[cp]=='-':
            tape[p]=(tape[p]-1)%256
        if code[cp]==',':
            ch=sys.stdin.read(1)
            tape[p]=(ord(ch) if ch else 0)%256
        if code[cp]=='.':
            print(chr(tape[p]),end='')
        if code[cp]=='<':
            p-=1
        if code[cp]=='>':
            p+=1
        if code[cp]=='[':
            if not tape[p]:
                cp=matches[cp]
        if code[cp]==']':
            if tape[p]:
                cp=matches[cp]
        cp+=1
notes=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
note2fuck='+]-+,.[>><,['
fuck2note={}
for j,i in enumerate(note2fuck):
    if i in fuck2note:
        fuck2note[i].append(notes[j])
    else:
        fuck2note[i]=[notes[j]]
def brainfuck2notes(brainfuck):
    return [choice(fuck2note[i]) for i in brainfuck]
def notes2brainfuck(notes_):
    return ''.join([note2fuck[notes.index(i)] for i in notes_])
def notes2mid(notes_,fn,bpm=120,velocity=127):
    file=MidiFile()
    track=MidiTrack()
    file.tracks.append(track)
    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(bpm)))
    for i in notes_:
        track.append(Message('note_on',note=60+notes.index(i),velocity=velocity,time=0))
        track.append(Message('note_off', note=60 + notes.index(i), time=480))
    file.save(file=fn)
def mid2notes(fn):
    file=MidiFile(file=fn)
    track=file.tracks[0]
    result=[]
    for msg in track:
        if msg.type=='note_on':
            result.append(notes[msg.note%12])
    return result
def interpret(fn):
    bf(notes2brainfuck(mid2notes(fn)))
#look module end

from flask import *
from uuid import uuid4
def err(msg,red): #发送错误消息 send error message
    flash(msg)
    return redirect(red)
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16777216 #最大大小：16MiB max size:16MiB
import os
if os.getenv('SEC_KEY'):
    app.secret_key=os.getenv('SEC_KEY')
else:
    app.secret_key='a'
@app.route('/')
def home(): #主页
    return render_template('index.html')


@app.route('/l2b')
def l2b(): #Look!转brainfuck功能 Look! to BF
    return render_template('l2b.html')
@app.route('/li')
def li(): #Look!解释功能 Look! interpreter
    return render_template('li.html')
@app.route('/lc')
def lc(): #brainfuck转Look!功能 BF to Look!
    return render_template('lc.html')
@app.route('/bf.js')
def lijs(): 
    return render_template('bf.js')
@app.route('/upload_l2b', methods=['POST'])
def upload_l2b(): #上传文件
    if 'file' not in request.files: #必须有文件信息 Must have file info
        return err('No file part','/l2b')
    f=request.files['file']
    if f.filename=='': #必须有文件 Must have file
        return err('No file uploaded','/l2b')
    if not f.filename.endswith('.mid'): #必须是MIDI文件 Must be MIDI file
        return err('Only MIDI files may be uploaded','/l2b')
    k=f.read()
    b=BytesIO(k)
    bf=notes2brainfuck(mid2notes(b))
    return render_template('l2b_result.html',code=bf)
@app.route('/upload_li', methods=['POST'])
def upload_li(): #上传文件
    if 'file' not in request.files: #必须有文件信息
        return err('No file part','/li')
    f=request.files['file']
    if f.filename=='': #必须有文件
        return err('No file uploaded','/li')
    if not f.filename.endswith('.mid'): #必须是MIDI文件
        return err('Only MIDI files may be uploaded','/li')
    k=f.read()
    b=BytesIO(k)
    bf=notes2brainfuck(mid2notes(b))
    return render_template('li_result.html',code=bf)
@app.route('/upload_lc', methods=['POST'])
def upload_lc(): #上传文件
    fm=request.form.get('code','')
    fm=''.join(filter(lambda x:x in'+-><,.[]',fm))
    b=BytesIO()
    nts=brainfuck2notes(fm)
    notes2mid(nts,b)
    b.seek(0)
    return send_file(b,mimetype='audio/midi',as_attachment=True,download_name='code.mid')