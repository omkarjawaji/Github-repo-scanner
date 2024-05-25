import streamlit as st
import matplotlib.pyplot as plt


class StreamlitStatistics:

    def __init__(self, data):
        self.data = data

    def plot_pie_chart(self):
        fig, ax = plt.subplots()
        count_list = [len(self.data[self.data['file_exists'] == True]), len(self.data[self.data['file_exists'] == False])]
        ax.pie(count_list, labels=['Exists', 'Missing'], autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'tomato'])
        ax.axis('equal')
        fig.set_facecolor('black')
        return fig

    def display_stats(self):
        st.title('Github scan result stats')

        st.header("Pie chart of certain file missing")
        pie_chart = self.plot_pie_chart()
        st.pyplot(pie_chart)

        st.header("Statistics")

        selected_category = st.selectbox("File exists?", [True, False])
        st.header(f"Items in Category {selected_category}")
        selected_data = self.data[self.data['file_exists'] == selected_category][['name', 'link']]
        st.write(selected_data)

        if st.checkbox('Show raw data'):
            st.subheader('Raw data')
            st.write(self.data)
