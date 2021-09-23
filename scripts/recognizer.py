#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import pyaudio
import wave
from playsound import playsound
import rospy

import os
import sys
from std_msgs.msg import String
pub = rospy.Publisher("voice_txt", String, queue_size=10)

rospy.sleep(1)

# 初始化ROS节点
rospy.init_node('voice_recognize', anonymous=True)

#from .tuning import Tuning

import usb.core

import usb.util

from aip import AipSpeech

APP_ID='24105668'
API_KEY='xIBkcVKdcRPkdGpOsclwCtci'
SECRET_KEY='GFnTBaNQHIlNxPwab2oDTnWWQuyTQDVm'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def recording(time,languge):        #time为录取时间,language为语言接口英语1737，中文1537
    RESPEAKER_RATE = 16000
    RESPEAKER_CHANNELS = 1 
    RESPEAKER_WIDTH = 2
    RESPEAKER_INDEX = 2 
    CHUNK = 1024
    RECORD_SECONDS = time
    WAVE_OUTPUT_FILENAME ="output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(
            rate=RESPEAKER_RATE,
            format=p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            input_device_index=RESPEAKER_INDEX,)

    print("* recording")

    frames = []

    for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)



    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(RESPEAKER_CHANNELS)
    wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
    wf.setframerate(RESPEAKER_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


    result = client.asr(get_file_content('output.wav'), 'wav', 16000, {
    'dev_pid': 1737,})
    
    try:
        if result['err_no'] == 0:
            return result['result'][0]
    except KeyError as ke:
        print(result)
        print(ke)
        return ''
    return ''

#文本转语音输出测试代码
def get_file_content(a):
	with open(a, 'rb') as fp:
		return fp.read()

while not rospy.is_shutdown():
    pub.publish(recording(3,1737))
    rospy.loginfo("I heard::"+recording(3,1737))
