import streamlit as st
import pandas as pd
from joblib import load

pipeline = load("CatBoost_heart.pkl")

st.title('Прогнозирование риска сердечно-сосудистых заболеваний')
st.write("Пожалуйста, заполните параметры для ")

age = st.number_input("Возраст", min_value=1, max_value=120, value=30)
sex = st.selectbox("Пол", ["Мужчина", "Женщина"])
chol = st.number_input("Холестерин", min_value=50, max_value=500, value=200)
maxHR = st.number_input("Максимальная частота сердечных сокращений (числовое значение от 60 до 202)", min_value=60, max_value=202, value=175)
chestPainType = st.selectbox("""Тип боли в груди:\n
**TA** - Типичная стенокардия,\n
**ATA** - Атипичная стенокардия,\n
**NAP** - Не стенокардиальная боль,\n
**ASY** - Бессимптомная""", ["ATA", "NAP", "ASY", "TA"])
restingBP = st.number_input("Артериальное давление в покое [мм рт. ст.]", min_value=1, max_value=250, value=120)
fastingBS = st.selectbox("""Уровень глюкозы натощак:\n
**1** - уровень глюкозы натощак более 120 мг/дл,\n
**0** - инуровень глюкозы натощак менее 120 мг/длаче""", [1, 0]) 
restingECG = st.selectbox("""Электрокардиограмма в покое:\n
**Normal** - норма,\n
**ST** - наличие ST-T аномалий (инверсия T-зубца и/или подъем или депрессия ST > 0.05 мВ),\n
**LVH** - вероятная или достоверная гипертрофия левого желудочка по критериям Эстеса""", ['Normal', 'ST', 'LVH'])
exerciseAngina = st.selectbox('Случается ли стенокардия, вызванная физической нагрузкой', ['Нет', "Да"])                  
oldpeak =  st.number_input("депрессия сегмента ST после нагрузки (числовое значение от 0 до 7)", min_value=1, max_value=250, value=120) 
st_slope = st.selectbox('Наклон сегмента ST при пиковом упражнении (Up: восходящий, Flat: горизонтальный, Down: нисходящий)', ['Up', 'Flat', 'Down'])

if st.button("Сделать предсказание"):
    simple_data = pd.DataFrame({
        "Age": [float(age)],
        "Sex": [1.0 if sex == "Мужчина" else 0.0],
        "Cholesterol": [float(chol)],
        "MaxHR": [float(maxHR)],
        "ChestPainType": [0.0 if chestPainType == "ATA" else 1.0 if chestPainType == "NAP" else 2.0 if chestPainType == "ASY" else 3.0],
        "RestingBP": [float(restingBP)],
        "FastingBS": [float(fastingBS)],
        "RestingECG": [0.0 if restingECG == "Normal" else 1.0 if restingECG == "ST" else 2.0],
        "ExerciseAngina": [1.0 if exerciseAngina == "Да" else 0.0],
        "Oldpeak": [float(oldpeak)],
        "ST_Slope_Flat": [1.0 if st_slope == "Flat" else 0.0],
        "ST_Slope_Up": [1.0 if st_slope == "Up" else 0.0],
        "ST_Slope_Down": [1.0 if st_slope == "Down" else 0.0]
    })
    
    try:
        pred = pipeline.predict(simple_data)
        pred_proba = pipeline.predict_proba(simple_data)
        
        if pred[0] == 1:
            st.error(f"Высокий риск сердечно-сосудистых заболеваний")
            #st.write(f"Вероятность: {pred_proba[0][1]*100:.1f}%")
        else:
            st.success(f"Низкий риск сердечно-сосудистых заболеваний")
            #st.write(f"Вероятность: {pred_proba[0][0]*100:.1f}%")
            
    except Exception as e:
        st.error(f"Ошибка при предсказании: {e}")