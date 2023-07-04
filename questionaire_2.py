import pandas as pd
import numpy as np
import streamlit as st
import psycopg2

@st.cache_resource
def init_connection():
    return psycopg2.connect(host="postgresql-76953-0.cloudclusters.net", 
                            database="mp_candidate",
                            user="mindshare", 
                            password="mindshare",port=19477,connect_timeout=60,keepalives=1,keepalives_idle=30,keepalives_interval=10,keepalives_count=5)

conn = init_connection()

k = ['']
m = ['']
l = ['']
z = ['']
dd = ['']
# read mapping file 
@st.cache_data
def load_data(file_name):
    df = pd.read_csv(file_name)
    return df

dic_name = load_data('dic_name.csv')
mapping = load_data('mp_map.csv')
party_list = load_data('party_name.csv')
district = mapping['district'].unique().tolist()
l.extend(district)
party_list = party_list['party'].unique().tolist()
k.extend(party_list)
candi = load_data('aspirant_list.csv')
rest = load_data('rest.csv')
caste_data = load_data('caste_mp.csv')

# form title 
st.title("Survey Madhya Pradesh by DIC ")
#dic name 
dics = dic_name['dic_name'].unique().tolist()
dd.extend(dics)
selected_DIC = st.selectbox('DIC Name',dd)
#Select district name
selected_dis = st.selectbox('What is the name of your District (Select District) ?',l)
#select AC name
temp = mapping[mapping['district'] == selected_dis]
ac_lists = temp['ac_no_name'].unique().tolist()
m.extend(ac_lists)
selected_ac = st.selectbox('What is the name of your Assembly Constituency (Select AC) ?',m)
# Select Booth
temp1 = mapping[mapping['district'] == selected_dis]
booth_lists = temp1['booth'].unique().tolist()
z.extend(booth_lists)
selected_booth = st.selectbox('Please type the booth no. and name',z)
selected_influencer = st.selectbox('Select the type of  Influencer',["",'General Public', 'Professional', 'Media Person'])
if selected_influencer == 'Professional':
    selected_professional = st.selectbox('Profession',["",'Doctor', 'Teacher', 'Sarpanch', 'Gram Panchayat Sadasya', 'Wards Members', 'Goverment Offical','others' ])
    if selected_professional == 'others':
        selected_professional = st.text_input('Type Profession')
if selected_influencer == 'General Public':
    selected_professional = 'General Public'
if selected_influencer == 'Media Person':
    selected_professional = st.text_input('Type Media House name')
# age
selected_age = st.number_input('We are interested in interviewing people of a certain age, please tell me your age (in years) ?', min_value=18, max_value=100, step=1, format='%d')
# Gender 
gender_brackets = ['male', 'female']
gender = st.radio('Please note the gender of respondent.',gender_brackets)
# Voting preference
mla_2022 = st.selectbox('If Assembly (MLA) elections are to be held tomorrow, then which party will you vote for?',k)
mp_2024 = st.selectbox('If Lok Sabha (MP) elections are to be held tomorrow, then which party will you vote for?',k)
mla_2018 = st.selectbox('Which party did you vote for in the last assembly (MLA) elections held in 2018?',k)
mp_2019 = st.selectbox('Which party did you vote for in the last Lok Sabha (MP) elections held in 2019?',k)
#candidate preference
candi_list = candi[candi['ac_no_name']== selected_ac]
sub_candidate_list = candi_list['candidate_name'].unique().tolist()
sub_candidate_list.append('others')
candi_inc_list = candi_list[candi_list['party_name']=='INC']
candi_bjp_list = candi_list[candi_list['party_name']=='BJP']
sub_inc_candidate_list = candi_inc_list['candidate_list'].unique().tolist()
sub_bjp_candidate_list = candi_bjp_list['candidate_list'].unique().tolist()
sub_inc_candidate_list.append('others')
sub_bjp_candidate_list.append('others')
selected_candidate = st.selectbox('Who is your preffered MLA Candidate in the assembly?',sub_candidate_list)
if selected_candidate == 'others':
    selected_candidate = st.text_input('write the Candidate name:')
selected_inc_candidate = st.selectbox('Who is your preffered MLA Candidate from INC?',sub_inc_candidate_list)
if selected_inc_candidate == 'others':
    selected_inc_candidate = st.text_input('write the INC Candidate name:')
selected_bjp_candidate = st.selectbox('Who is your preffered MLA Candidate from BJP?',sub_bjp_candidate_list)
if selected_bjp_candidate == 'others':
    selected_bjp_candidate = st.text_input('write the BJP Candidate name:')
# who will win
vs_ac = st.selectbox('If Assembly (MLA) elections are to be held tomorrow, then which party will win in your Assembly Constituency?',k)
vs_state = st.selectbox('If Assembly (MLA) elections are to be held tomorrow, then which party will form the government in Madhya Pradesh?',k)
# cm preference
cm_list = ["",'Kamal Nath','Shivraj Singh Chouhan','Jyotiraditya Scindiya','Narottam Mishra','Narendra Tomar','Kailash Vijayvargiya','Digvijay Singh','Jitu Patwari','others','Do not know']
cm_prefer = st.selectbox('According to you, who is best suitable to be the next Chief Minister of Madhya Pradesh?',cm_list)
# anti incumbency 
sg_incumbency = st.selectbox('Do you think that the current BJP government should be given an another chance?',["",'yes','no','Dont Know / Cant Say'])
mla_incumbency = st.selectbox('Do you think that your MLA should be given another chance to represent your assembly constituency?',["",'yes','no','Dont Know / Cant Say'])
# class classification 
#Modi Factor
modi_impact = st.selectbox('Is narendra modi a relevant voting factor in the upcoming elections?',["",'yes','no','Dont Know / Cant Say'])
modi_visit = st.selectbox('Are you likely to change your vote if Narendra Modi visits your AC?',["",'yes','no','Dont Know / Cant Say'])
#education list 
h = ['']
education_list = rest['What is your highest level of education?'].unique().tolist()
h.extend(education_list)
edu = st.selectbox('What is your highest level of education?',h)
#occupation
i = ['']
occ_list = rest['What is your occupation?'].unique().tolist()
i.extend(occ_list)
occ = st.selectbox('What is your occupation?',i)
#income
j = ['']
inc_list = rest['What is your familys monthly income?'].unique().tolist()
j.extend(inc_list)
inc = st.selectbox('What is your familys monthly income?',j)
#religion
r = ['']
rel_list = rest['What is your religion?'].unique().tolist()
r.extend(rel_list)
religion = st.selectbox('What is your religion?',r)
#category
c = ['']
cat_list = rest['Which Caste Category do you belong to?'].unique().tolist()
c.extend(cat_list)
cat = st.selectbox('Which Caste Category do you belong to?',c)
# caste preference 
caste_list = caste_data[caste_data['ac_no_name']== selected_ac]
caste_list = caste_list[caste_list['Category']==cat]
caste_list = caste_list['Cleaned Caste'].unique().tolist()
caste_list.append('others')
selected_caste = st.selectbox('Which caste do you belong to?',caste_list)
if selected_caste =='others':
    selected_caste = st.text_input('write the caste name:')

# Ask for person's mobile phone number
phone = st.number_input('Could you please share your contact no?', min_value=0, max_value=10**14-1, step=1, format='%d')
#submit button
submit_button = st.button("Submit")
#varia = [selected_ac,selected_booth,selected_influencer,selected_professional,selected_age,gender,mla_2022,mp_2024,mla_2018,mp_2019,selected_candidate,selected_inc_candidate,selected_bjp_candidate,vs_ac,vs_state,cm_prefer,sg_incumbency,mla_incumbency,edu,inc,religion,cat,selected_caste,phone]
# Handle Form Submission
if submit_button and selected_DIC and selected_dis and selected_ac and selected_booth and selected_influencer and selected_professional and selected_age and gender and mla_2022 and mp_2024 and mla_2018 and mp_2019 and selected_candidate and selected_inc_candidate and selected_bjp_candidate and vs_ac and vs_state and cm_prefer and sg_incumbency and mla_incumbency and modi_impact and modi_visit and edu and inc and occ and religion and cat and selected_caste and phone:
    cursor = conn.cursor()
    sql = "INSERT INTO mp_tabl1 VALUES ( %s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s,%s)"
    values = (selected_DIC,selected_dis,selected_ac,selected_booth,selected_influencer,selected_professional,selected_age,gender,mla_2022,mp_2024,mla_2018,mp_2019,selected_candidate,selected_inc_candidate,selected_bjp_candidate,vs_ac,vs_state,cm_prefer,sg_incumbency,mla_incumbency,modi_impact,modi_visit,edu,inc,occ,religion,cat,selected_caste,phone)
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    st.success("Response submitted successfully!")
    st.write('Click below to fill another response.')
    if st.button('Fill Another Response'):
        #st.cache_data.clear()
        st.experimental_rerun()
        pg.press('f5')
elif submit_button:
    st.warning("Please fill in all the fields before submitting.")