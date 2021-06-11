from flask import Flask, render_template, request
import json
import pickle

app = Flask(__name__)

with open('hr_columns.json') as f:
    hr_columns = json.load(f)

# print(hr_columns['gender'])

with open("hr_analytics.pickle", "rb") as f:
    model = pickle.load(f)

with open('encode_values.json') as f:
    encode_values = json.load(f)

keys = list(encode_values.keys())
values = list(encode_values.values())
print(keys[1])
print(values[1][0])
# print(hr_columns['gender'])
# print(len(hr_columns['gender']))


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('index.html', hr_columns=hr_columns)

@app.route('/predict', methods=['GET','POST'])
def predict():
    gen = 0
    rel_experience = 0
    en_uni = 0
    edu_lev = 0
    m_dis = 0
    com_type = 0

    city_development_index = int(request.form.get('city_development_index'))
    gender = request.form.get('gender')
    relevent_experience = request.form.get('relevent_experience')
    enrolled_university = request.form.get('enrolled_university')
    education_level = request.form.get('education_level')
    major_discipline = request.form.get('major_discipline')
    experience = int(request.form.get('experience'))
    company_size = int(request.form.get('company_size'))
    company_type = request.form.get('company_type')
    last_new_job = int(request.form.get('last_new_job'))

    gender_val = keys[0].split(",")
    for i in range(0,len(gender_val)):
        if gender in gender_val[i]:
            gender = str(values[0][i])
            gen = int(gender)
    # print(gender)

    rel_exp_val = []
    rel_exp_val = keys[1].split(',')
    for i in range(0,len(rel_exp_val)):
        if relevent_experience in rel_exp_val[i]:
            relevent_experience = str(values[1][i])
            rel_experience = int(relevent_experience)
    # print(relevent_experience)

    en_uni_val = []
    en_uni_val = keys[2].split(',')
    for i in range(0,len(en_uni_val)):
        if enrolled_university in en_uni_val[i]:
            enrolled_university = str(values[2][i])
            en_uni = int(enrolled_university)
    # print(enrolled_university)

    edu_level_val = keys[3].split(',')
    for i in range(0,len(edu_level_val)):
        if education_level in edu_level_val[i]:
            education_level = str(values[3][i])
            edu_lev = int(education_level)
    # print(education_level)

    major_discipline_val = keys[3].split(',')
    for i in range(0,len(major_discipline_val)):
        if major_discipline in major_discipline_val[i]:
            major_discipline = str(values[4][i])
            m_dis = int(major_discipline)
    # print(major_discipline)

    com_type_val = []
    com_type_val = keys[2].split(',')
    for i in range(0,len(com_type_val)):
        if company_type in com_type_val[i]:
            company_type = str(values[5][i])
            com_type = int(company_type)

    with open("hr_analytics.pickle","rb") as f:
        hr_model = pickle.load(f)
    
    data = [[city_development_index,gen,rel_experience,en_uni,edu_lev,m_dis,experience,company_size,com_type,last_new_job]]
    prediction = hr_model.predict(data)
    # print(prediction)


    if prediction[0] == 1:
        return "You are elligible for this job !!!"
    elif prediction[0] == 0:
        return "You are not elligible for this job !!!"
    else:
        return render_template('index.html', hr_columns=hr_columns)

if __name__ == '__main__':
    app.run(debug=True)