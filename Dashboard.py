import time
import pandas as pd
import streamlit as st

from Gif import Gif
from Map import Map
from EvolutionaryOperator import EvolutionaryOperator

st.markdown("# **Пути**")

map_path = st.text_input("Путь к карте:", value = "./data/map.txt")

is_gif = st.checkbox("Сохранить GIF файл")
if is_gif:
    gif_path = st.text_input("Путь для вывода GIF:", value = "./gif/route.gif")

is_save = st.checkbox("Сохранить лучший путь")
if is_save:
    route_path = st.text_input("Путь для вывода пути:", value = "./data/save.txt")

st.markdown("# **Параметры алгоритма**")

n_state = st.slider("Количество состояний в автомате:", 1, 25, step = 1, value = 5)
n_ants = st.slider("Популяция муравьёв:", 5, 1000, step = 5, value = 100)
n_iter = st.slider("Количество селекций:", 5, 1000, step = 5, value = 100)
n_moves = st.slider("Максимальное количество действий муравья:", 100, 900, step = 5, value = 100)
percent_of_survivors = st.slider("Процент отбираемой популяции:", 1, 100, step = 1, value = 25)
percent_of_crossover = st.slider("Вероятность мутации:", 1, 100, step = 1, value = 50)

map = Map(map_path)

if st.button("Начать отбор!"):
    ev = EvolutionaryOperator(map,
                              max_iter=n_iter,
                              max_moves=n_moves,
                              n_ants=n_ants,
                              percent_of_survivors=percent_of_survivors / 100,
                              percent_of_crossover=percent_of_crossover / 100,
                              n_state=n_state)
    with st.spinner("[1/4] Отбираем муравьёв..."):
        start_time = time.time()
        ev.fit()
        end_time = time.time()
    st.success("Селекция завершена!")

    with st.spinner("[2/4] Загружаем лучший путь..."):
        moves, n_food, route, food = ev.look_food(ev.best_ant)
    st.success("Загружен лучший путь!")

    with st.spinner("[3/4] Анимируем..."):
        if is_gif:
            gif = Gif(map, route, food)
            gif.create_gif(gif_path)
        
        if is_save:
            file = open(route_path, 'w+')
            for pos in route:
                file.write(f"{str(pos[0])},{str(pos[1])}\n")
            file.close()
    st.success("Анимация завершена!")

    with st.spinner("[4/4] Выводим отчёт..."):
        st.success("Отчёт готов!")

        st.markdown("# **Отчёт**")

        st.markdown(f"**Очки приспособленности**: {n_food}")
        st.markdown(f"**Время работы**: {(end_time - start_time) // 1} с.")

        handle_actions = {
            0 : "Идти вперёд",
            1 : "Повернуть направо",
            2 : "Повернуть налево"
        }

        states, actions, next_states = [], [], []
        for i in range(1, n_state + 1):
            next_state = ev.best_ant.automaton[0][i]["next_state"]
            action = ev.best_ant.automaton[0][i]["action"]

            states.append(i)
            actions.append(handle_actions[action])
            next_states.append(next_state)
        
        table = []
        table.append(states)
        table.append(actions)
        table.append(next_states)

        st.markdown("### **Лучший конечный автомат**")

        df = pd.DataFrame(table).transpose()
        df.columns = ['Состояние', 'Действие', 'Следующее состояние']
        df.set_index('Состояние', inplace = True)

        st.table(df)
            