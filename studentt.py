import cv2
import numpy as np
import streamlit as st
import pandas as pd
from answer import my_answer_list
import my_function
import student_info

# Function to get toppers
def get_toppers(df):
    toppers = df[df['Result'] == 'Pass'].nlargest(3, 'Grading')
    return toppers

# Function to get top 3 difficult questions
def get_difficult_questions(ans_dict):
    sorted_ans_dict = sorted(ans_dict.items(), key=lambda x: x[1], reverse=True)
    difficult_questions = [int(sorted_ans_dict[i][0]) + 1 for i in range(3)]
    return difficult_questions

# Main Streamlit app
def main():
    st.title('Student Grading Dashboard')

    path_array = []
    for sheet in range(len(student_info.sheet_list)):
        path_array.append(f'student/{student_info.sheet_list[sheet]}.png')

    student_id = []
    grading = []
    status = []
    ans_dict = {}
    answer_array = my_answer_list
    new_ans_dict = {}
    for ques in range(0, 72):
        ans_dict[f'{ques}'] = 0
    for ques in range(60):
        new_ans_dict[f'{ques}'] = 0

    for sheet in range(len(path_array)):
        img = cv2.imread(path_array[sheet])
        pixel_array2 = my_function.handle_image(img)

        id = student_info.df.loc[sheet, ['Student_ID']].tolist()
        id = ' '.join(id)
        student_id.append(id)

        answer_dict = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E'}
        student_answer = []
        answer_letter = []
        my_function.find_correct_choices(pixel_array2, student_answer)

        for x in student_answer:
            answer_letter.append(answer_dict[f'{x}'])

        count = 0
        check = []
        for x in range(0, 72):
            if answer_array[x] == student_answer[x]:
                check.append(1)
                count += 1
            else:
                check.append(0)
                ans_dict[f'{x}'] += 1
        count -= 12
        grading.append(count)

        if count >= 30:
            status.append('Pass')
        else:
            status.append('Fail')

    count_ques = 0
    for ques in list(ans_dict):
        count_ques += 1
        if count_ques == 6:
            ans_dict.pop(f'{ques}', None)
            count_ques -= 6

    num = 0
    for ques in list(ans_dict):
        new_ans_dict[f'{num}'] = ans_dict[f'{ques}']
        num += 1

    grading_data = {'Student_ID': student_id, 'Grading': grading, 'Result': status}
    grading_df = pd.DataFrame(grading_data, columns=['Student_ID', 'Grading', 'Result'])
    grading_df = grading_df.sort_values(by=['Student_ID'])
    grading_df = grading_df.reset_index(drop=True)

    toppers_df = get_toppers(grading_df)
    difficult_questions = get_difficult_questions(ans_dict)

    # Display the table of student information
    st.subheader('Student Information')
    st.table(grading_df)

    # Display the toppers of the class
    st.subheader('Top Scorers')
    st.write("🏆🎉 Congratulations to the top scorers!")
    st.table(toppers_df)

    # Display the top 3 difficult questions
    st.subheader('Top 3 Difficult Questions')
    st.write(difficult_questions)

if __name__ == '__main__':
    main()
