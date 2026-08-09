import streamlit as st
import os
from openai import OpenAI
from streamlit import text_input
from datetime import datetime
import json


# 1.与LLM交互逻辑:
#     1>设置聊天输入框(chat_input)和聊天输出框(chat_output);
#     2>创建与LLM交互的客户端对象,将输入和对象的参数绑定,获取结果;
# 2.显示聊天记录逻辑:由于每次请求都会刷新(重新执行代码),故想要记录一直显示,需要将聊天记录保存在缓存中;
#     1>在发送和接收消息之后,将消息放到缓存session_state中;
#     2>在页面前面遍历消息记录并展示;(这样前端每次刷新都会显示)
# 3.流式输出逻辑:由于流式每次返回一个包(含几个文字)
#     1>LLM交互对象stream设为True;
#     2>遍历返回的包,创建空容器,每次获取一个包,刷新内容到容器中;同时累积所有消息;
#     3>将全部消息放入缓存中;
# 4.设置侧边栏 ai昵称,性格逻辑:由于昵称性格输入后,此会话需要一致保持,故也要放入缓存;
#     1>创建输入框;
#     2>在缓存中创建容器并为昵称性格设置默认值;
#     3>将输入框值更新到缓存中,并将输入框显示值与缓存中绑定;
#     4>将缓存中昵称性格与ai交互对象中的提示词绑定;
# 5.新建会话逻辑:新建会话时,要保存当前会话并创建新会话;会话记录要保存,因此要存入文件中;
#     1>创建会话按钮
#     2>将聊天记录,昵称,性格,会话标识以json格式放入session目录中;
#     3>刷新页面,重新渲染显示新会话;
#     注意:保存会话前先判断当前会话是否为空(防止点击一直保存空会话);保存当前会话时,也要判断,否则也会保存空会话;
# 6.展示会话历史逻辑:
#     1>获取所有会话历史文件名(sessions目录下去除.json后缀)
#     2>遍历所有会话文件名,创建按钮;
# 7.点击展示会话逻辑:
#     1>根据点击的会话名,读取会话文件,并赋给当前会话变量;
#     2>再重新运行;
# 8.删除会话逻辑:
#     1>获取删除会话的文件名称,删除文件
#     2>若删除的是当前会话,则要更新当前会话为新会话;
#     3>刷新页面;
def save_current_session():
    if st.session_state.current_session:
        # 创建会话内容
        session_data = {
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages,
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature
        }
        # 创建保存会话目录
        if not os.path.exists("sessions"):
            os.mkdir("sessions")
        # 以json格式存入
        with open(f"sessions/{session_data["current_session"]}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)


# 加载会话文件名
def load_sessions():
    session_list = []
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")  # 返回文件名列表
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])  # 切片保留名称
    session_list.sort(reverse=True)#倒序,使得最新的会话显示在最上面
    return session_list


def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception as e:
        print(e)


def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            #若删除的是当前会话,则要更新当前会话为新会话
            if session_name == st.session_state.current_session:
                st.session_state.messages = [{"role": "system", "content": "我是贺晨浩的ai助手,你好!"}]
                st.session_state.current_session=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    except Exception as e:
        print(e)

# 页面配置
st.set_page_config(
    page_title="贺晨浩的ai",  # 网页浏览导航栏名称
    page_icon="😃",  # 导航栏图标
    layout="wide",  # 页面占用布局
    initial_sidebar_state="expanded",  # 侧边栏状态
    menu_items={  # 菜单导航
    }
)

# 标题和logo
st.title("贺晨浩的ai")
st.logo("resources/logo.png")

# 创建与LLM交互的客户端对象(DEEPSEEK_API_KEY为环境变量名字，值为apik)
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),  # 从本机环境变量中获取apik,首次设置环境变量后,要重启ide
    base_url="https://api.deepseek.com")

# 给ai的提示词
system_prompt = ''' 
    你叫%s，现在是用户的真实伴侣，请完全代入伴侣角色。
    规则:
    1.每次只回1条消息
    2.禁止任何场景或状态描述性文字
    3.匹配用户的语言
    4.回复简短，像微信聊天一样
    5.有需要的话可以用等emoji表情
    6.用符合伴侣性格的方式对话
    7.回复的内容，要充分体现伴侣的性格特征伴侣性格:%s
    你必须严格遵守上述规则来回复用户。
    '''

# 保存需要放入缓存的变量:由于每次请求都会刷新,故需要记录以前变量和需要一致维持的变量
if "messages" not in st.session_state:  # 将聊天记录保存在session_state中
    st.session_state.messages = [{"role": "system", "content": "我是贺晨浩的ai助手,你好!"}]
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "小甜甜"
if "nature" not in st.session_state:
    st.session_state.nature = "温柔可爱的南方女孩"
# 保存当前会话唯一标识
if "current_session" not in st.session_state:
    st.session_state.current_session = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

st.text(f"会话名称:{st.session_state.current_session}")
# 展示聊天记录:将记录加入缓存;每次刷新后,加载缓存中的记录
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

with st.sidebar:
    st.subheader("AI控制面板")
    # 创建按钮 调用保存会话函数
    if st.button("新建会话", width="stretch", icon="🔎"):
        if len(st.session_state.messages) > 1:
            save_current_session()  # 保存当前会话
            # 新建会话
            st.session_state.messages = [{"role": "system", "content": "我是贺晨浩的ai助手,你好!"}]
            st.session_state.current_session = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            # 保存当前会话:防止刷新后当前会话丢失
            if len(st.session_state.messages) > 1:
                save_current_session()
            st.rerun()  # 刷新,显示新的会话

    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1, col2 = st.columns([4, 1])
        with col1:
            # 加载会话
            if st.button(session, width="stretch", icon="🎬", key=f"load_{session}",
                         type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            # 删除会话
            if st.button("", width="stretch", icon="❌️️", key=f"delete_{session}"):
                delete_session(session)
                st.rerun()
    #分割线
    st.divider()

    st.subheader("ai信息")
    nick_name = st.text_input("昵称", placeholder="请输入昵称", value=st.session_state.nick_name)  # 昵称输入框
    if nick_name:
        st.session_state.nick_name = nick_name
    nature = st.text_area("性格", placeholder="请输入性格", value=st.session_state.nature)  # 性格输入框
    if nature:
        st.session_state.nature = nature

# 消息输入框
prompt = st.chat_input("请输入您要问的问题")
if prompt:
    st.chat_message("user").write(prompt)  # user表示发的人是谁:user/assistant
    st.session_state.messages.append({"role": "user", "content": prompt})  # 添加用户记录
    # 交互参数设置
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            *st.session_state.messages
        ],
        stream=True,  # 控制流式输出
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    # 流式展示返回值
    reponse_message = st.empty()  # 空容器,展示返回值
    full_response = ""  # 存储整个返回值

    # 遍历流式输出结果
    for chunk in response:
        if chunk.choices[0].delta.content:  # 每次的流式返回包
            content = chunk.choices[0].delta.content
            full_response += content  # 记录之前所有包的值
            reponse_message.chat_message("assistant").write(full_response)  # 刷新容器中展示
    # st.chat_message("assistant").write(response.choices[0].message.content)  #非流式输出结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})  # 整体记录
    save_current_session()
