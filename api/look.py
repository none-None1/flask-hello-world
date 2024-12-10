from os import environ
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
    file.save(fn)
def mid2notes(fn):
    file=MidiFile(fn)
    track=file.tracks[0]
    result=[]
    for msg in track:
        if msg.type=='note_on':
            result.append(notes[msg.note%12])
    return result
def interpret(fn):
    bf(notes2brainfuck(mid2notes(fn)))

