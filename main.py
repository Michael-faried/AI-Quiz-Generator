import streamlit as st
from model import global_filtered_qa_pairs

# Split the array into questions and answers
questions = global_filtered_qa_pairs[::5]
answers = [global_filtered_qa_pairs[i:i+4] for i in range(1, len(global_filtered_qa_pairs), 5)]

st.set_page_config(page_title="Doc Searcher", page_icon=":robot:")
# Display the questions and answers
for i, question in enumerate(questions):
    st.markdown(f"## **{question}**")  # make the question text bold and larger
    for j, option in enumerate(answers[i]):
        if st.button(option, key=f'option_{i}_{j}'):  # unique key for each button
            if j == 0:  # assuming the first answer is always correct
                st.write("Correct!")
            else:
                st.write("Incorrect. The correct answer is: ", answers[i][0])


