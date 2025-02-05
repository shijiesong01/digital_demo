import streamlit as st
import subprocess
import webbrowser
import time

###
# 因streamlit特殊的启动方式较为复杂，因此暂时废弃streamlit作为ui前端
###
def ui_start_streamlit(config):
    subprocess.Popen(["streamlit", "run", "forward_module\\ui\\ui_init.py"])
    # 等待一段时间，确保Streamlit应用已经启动
    time.sleep(2)
    # 打开浏览器访问Streamlit应用
    #webbrowser.open("http://localhost:8501")