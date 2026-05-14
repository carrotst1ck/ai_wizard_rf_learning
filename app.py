import streamlit as st
from PIL import Image
import subprocess
import os
import sys

BASE_DIR = os.path.join(os.path.dirname(__file__), 'mage_battle')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TRAIN_SCRIPT = os.path.join(BASE_DIR, 'train.py')
DEMO_SCRIPT = os.path.join(BASE_DIR, 'visual_demo.py')


# ----------------------------
# НАСТРОЙКИ СТРАНИЦЫ
# ----------------------------
st.set_page_config(
    page_title="RL Битва Магов",
    page_icon="⚔️",
    layout="wide"
)


# ----------------------------
# ЗАГОЛОВОК
# ----------------------------
st.title("⚔️ RL Битва Магов ⚔️")
st.write("Демонстрация Reinforcement Learning проекта")


# ----------------------------
# КНОПКИ УПРАВЛЕНИЯ
# ----------------------------
col1, col2, col3 = st.columns(3)


# ----------------------------
# ПЕРЕОБУЧЕНИЕ АГЕНТА
# ----------------------------
with col1:

    if st.button("🔁 Переобучить агента"):

        if os.path.exists(TRAIN_SCRIPT):

            with st.spinner("Идет обучение агента..."):

                result = subprocess.run(
                    [sys.executable, TRAIN_SCRIPT],
                    capture_output=True,
                    text=True,
                    cwd=BASE_DIR
                )

            if result.returncode == 0:
                st.success("✅ Обучение завершено")
            else:
                st.error("❌ Ошибка при обучении")
                st.code(result.stderr)

        else:
            st.error("Файл train.py не найден")


# ----------------------------
# ЗАПУСК БОЯ
# ----------------------------
with col2:

    if st.button("🎬 Запустить бой"):

        if os.path.exists(DEMO_SCRIPT):

            with st.spinner("Запуск демонстрации боя..."):

                result = subprocess.run(
                    [sys.executable, DEMO_SCRIPT],
                    capture_output=True,
                    text=True,
                    cwd=BASE_DIR
                )

            if result.returncode == 0:
                st.success("✅ Бой завершен")
            else:
                st.error("❌ Ошибка при запуске боя")
                st.code(result.stderr)

        else:
            st.error("Файл visual_demo.py не найден")


# ----------------------------
# ОБНОВЛЕНИЕ СТРАНИЦЫ
# ----------------------------
with col3:

    if st.button("🔄 Обновить страницу"):
        st.rerun()


st.divider()


# ----------------------------
# ГРАФИК ОБУЧЕНИЯ
# ----------------------------
st.header("📊 График обучения")

graph_path = os.path.join(STATIC_DIR, "training_progress.png")

if os.path.exists(graph_path):

    try:
        image = Image.open(graph_path)

        st.image(
            image,
            caption="Прогресс обучения RL-агента",
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Ошибка загрузки графика: {e}")

else:
    st.warning("⚠️ График обучения не найден")
    st.info("Сначала запустите обучение агента")


st.divider()


# ----------------------------
# ВИДЕО БОЯ
# ----------------------------
st.header("🎥 Демонстрация боя")

video_path = None
video_candidates = []
if os.path.isdir(STATIC_DIR):
    video_candidates = [f for f in os.listdir(STATIC_DIR) if f.lower().endswith(('.mp4', '.webm', '.mov'))]

if video_candidates:
    video_path = os.path.join(STATIC_DIR, video_candidates[0])

gif_path = os.path.join(STATIC_DIR, "battle.gif")

if video_path and os.path.exists(video_path):
    try:
        st.video(video_path)
        st.caption(f"Видео боя: {os.path.basename(video_path)}")
    except Exception as e:
        st.error(f"Ошибка загрузки видео: {e}")
elif os.path.exists(gif_path):
    try:
        st.image(
            gif_path,
            caption="GIF боя",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Ошибка загрузки GIF: {e}")
else:
    st.warning("⚠️ Видео боя не найдено")
    st.info("Поместите MP4/WEBM файл в mage_battle/static или создайте battle.gif")


st.divider()


# ----------------------------
# СТАТИСТИКА ПРОЕКТА
# ----------------------------
st.header("📈 Информация о проекте")

st.markdown("""
## Что делает RL-агент

Агент обучается с помощью Reinforcement Learning.

### Возможности агента:

- ⚔️ Атаковать
- 🛡️ Ставить щит
- ❤️ Лечиться
- 🔋 Восстанавливать ману

### Используемые технологии

- Q-learning
- Q-table
- Epsilon-greedy стратегия
- Собственная игровая среда
- Пошаговая система боя
- Streamlit интерфейс
- Визуализация обучения
""")


# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("⚙️ Меню")

st.sidebar.info("""
RL Mage Battle Demo

Авторская демонстрация
Reinforcement Learning проекта
""")

st.sidebar.success("Система работает")


# ----------------------------
# СТАТУС ФАЙЛОВ
# ----------------------------
st.sidebar.subheader("📂 Проверка файлов")

files_to_check = [
    TRAIN_SCRIPT,
    DEMO_SCRIPT,
    graph_path,
]

if video_path:
    files_to_check.append(video_path)
elif os.path.exists(gif_path):
    files_to_check.append(gif_path)

for file in files_to_check:

    if os.path.exists(file):
        st.sidebar.success(f"✅ {file}")
    else:
        st.sidebar.error(f"❌ {file}")


# ----------------------------
# FOOTER
# ----------------------------
st.divider()

st.success("🚀 RL Battle System успешно запущена")
