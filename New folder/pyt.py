import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from translations import translations 
from pathlib import Path
import feedparser

dataset = pd.read_csv("t20_wc.csv")

def load_css():
    css_file = Path("styles.css")
    if css_file.exists():
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS
load_css()




# Create a navbar using streamlit-option-menu
selected = option_menu(
    menu_title=None,
    options=["Home", "Quiz","Search","CricInfo","About", "Contact"],
    icons=["house", "clipboard", "check-circle", "envelope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)
# Load the dataset once and store it in session state
if 'df' not in st.session_state:
    st.session_state['df'] = pd.read_csv('mens_t20_world_cup_quiz.csv')

# Show content based on selection
if selected == "Home":
   
    st.title(" ✨ Welcome to Our page ✨")
    st.markdown("---------")
    video_url = "video.mp4"
    st.image(["img3.jpeg"])
    st.markdown("INDIA ARE T20 WORLD CHAMPIONS 🏆 AFTER 17 YEARS! It's been a long, long wait for India and they now join West Indies and England as the only three teams to have won the Men's T20 World Cup two times. You really couldn't ask for more, what a grand finale we have had here in Barbados and both sides gave it their all! The Indian players are up in ecstasy and the playing field is flooded by the dugout. The crowd is at the top of its lungs and it's another heartbreak for South Africa, they simply couldn't get it done. Rohit Sharma is down in tears, as he was after the 2023 World Cup final - but this time, these are tears of joy. You really have to hand it to the Indian side, they were down and out but what redemption this is for the Men in Blue.")
   
    st.image(["img2.jpg"])
    st.markdown(
        "The ICC Men's T20 World Cup (formerly the ICC World Twenty20) is the Twenty20 International cricket tournament, organised by the International Cricket Council (ICC) since 2007. The event has generally been held every two years. In May 2016, the ICC put forward the idea of having a tournament in 2018, with South Africa being the possible host,[2] but the ICC later dropped the idea of a 2018 edition at the conclusion of the 2017 ICC Champions Trophy.[3] The 2020 edition of the tournament was scheduled to take place but due to the COVID-19 pandemic, the tournament was postponed until 2021, with the intended host changed to India. The 2021 ICC Men's T20 World Cup was later relocated to the United Arab Emirates (UAE) and Oman[4] due to problems relating to the COVID-19 pandemic in India, taking place 5 years after the previous (2016) iteration."
    )
    st.image(["img1.jpg"])
    st.markdown(
        "The International Cricket Council's executive committee votes for the hosts of the tournament after examining bids from the nations which have expressed an interest in holding the event. After South Africa in 2007, the tournament was hosted by England, the West Indies and Sri Lanka in 2009, 2010 and 2012 respectively. Bangladesh hosted the tournament in 2014.[38] India hosted the tournament in 2016. After a gap of five years, India won the hosting rights of 2021 edition as well, but due to COVID-19 pandemic the matches were played in Oman and the United Arab Emirates."
    )
    st.video(video_url, start_time=0)
    st.markdown("The ICC Men's T20 World Cup (formerly the ICC World Twenty20) is the Twenty20 International cricket tournament, organised by the International Cricket Council (ICC) since 2007.")
    
    st.markdown("""
<hr style="border: 1px solid #ddd;">
<div style="text-align: center; font-size: 14px; color: #000;">
    <p>&copy; 2024 Your Company Name. All rights reserved.</p>
    <p><a href="https://www.yourcompany.com" target="_blank">Visit our website</a> | <a href="https://www.yourcompany.com/privacy" target="_blank">Privacy Policy</a> | <a href="https://www.yourcompany.com/terms" target="_blank">Terms of Service</a></p>
    <p>Follow us on: <a href="https://twitter.com/yourcompany" target="_blank">Twitter</a> | <a href="https://linkedin.com/company/yourcompany" target="_blank">LinkedIn</a></p>
    <p>Contact us: <a href="mailto:support@yourcompany.com">support@yourcompany.com</a></p>
</div>
""", unsafe_allow_html=True)
    
    
    
    

elif selected == "Quiz":
    

    # Initialize session state
    if 'question_index' not in st.session_state:
        st.session_state['question_index'] = 0
    if 'score' not in st.session_state:
        st.session_state['score'] = 0
    if 'selected_answer' not in st.session_state:
        st.session_state['selected_answer'] = None
    if 'questions' not in st.session_state:
        # Randomly sample up to 15 questions
        st.session_state['questions'] = st.session_state['df'].sample(n=min(len(st.session_state['df']), 15)).reset_index(drop=True)
        st.session_state['question_index'] = 0
        st.session_state['user_answers'] = []  # To track user's answers

    # Function to display the next question
    def next_question():
        correct_answer = st.session_state['questions'].loc[st.session_state['question_index'], 'Answer']
        if st.session_state['selected_answer'] == correct_answer:
            st.session_state['score'] += 1
        # Store the user's answer and the correct answer
        st.session_state['user_answers'].append({
            'question': st.session_state['questions'].loc[st.session_state['question_index'], 'Question'],
            'user_answer': st.session_state['selected_answer'],
            'correct_answer': correct_answer
        })
        st.session_state['question_index'] += 1
        st.session_state['selected_answer'] = None

    # Display quiz content
    if st.session_state['question_index'] < len(st.session_state['questions']):
        st.markdown('<div class="quiz-container">', unsafe_allow_html=True)

        question = st.session_state['questions'].loc[st.session_state['question_index'], 'Question']
        options = [st.session_state['questions'].loc[st.session_state['question_index'], f'Option {i}'] for i in range(1, 5)]

        st.markdown(f"<div class='question'>Question {st.session_state['question_index'] + 1}: {question}</div>", unsafe_allow_html=True)

        # Display checkboxes for options
        selected_option = st.session_state['selected_answer']
        option_keys = []
        for option in options:
            key = f"option_{option}"
            option_keys.append(key)
            if st.checkbox(option, key=key, value=(option == selected_option)):
                st.session_state['selected_answer'] = option

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Next", disabled=st.session_state['selected_answer'] is None):
            next_question()
    else:
        st.markdown('<div class="results">', unsafe_allow_html=True)
        st.write(f"Quiz Completed! Your score: {st.session_state['score']} out of {len(st.session_state['questions'])}.")

        # Show results
        st.write("### Your Answers and Correct Answers:")
        for answer in st.session_state['user_answers']:
            st.write(f"**Question:** {answer['question']}")
            st.write(f"**Your Answer:** {answer['user_answer']}")
            st.write(f"**Correct Answer:** {answer['correct_answer']}")
            st.write("---")

        st.markdown('</div>', unsafe_allow_html=True)

    # Option to restart the quiz
    if st.button("Restart Quiz"):
        st.session_state['questions'] = st.session_state['df'].sample(n=min(len(st.session_state['df']), 15)).reset_index(drop=True)
        st.session_state['question_index'] = 0
        st.session_state['score'] = 0
        st.session_state['selected_answer'] = None
        st.session_state['user_answers'] = []  # Reset user answers
        
if selected == "Search":
     st.title("Search records")

     player_name = st.text_input("Enter the player name ")
     if player_name:
        results = dataset[dataset['Player Of The Match'] == player_name]
        if not results.empty:
            st.write(results)

     team_name = st.text_input("Enter the team name")
     if team_name:
        results = dataset[dataset['Winner Team'] == team_name]
        if not results.empty:
            st.write(results[['Result', 'Venue']])

     match_bw = st.text_input("Enter the team names")
     if match_bw:
        between = dataset[dataset['Match Between'] == match_bw]
        if not between.empty:
            st.write(between[['Winner Team', 'Winning Team Score', 'Losing Team', 'Losing Team Score']])
        else:
            st.write("No results found for the entered team names.")

     date = st.text_input("Enter the date of the match")
     if date:
        time = dataset[dataset['Date'] == date]
        if not time.empty:
            st.write(time[['Match Between', 'Winner Team', 'Losing Team']])
            
            
if selected == "CricInfo":
 def fetch_rss_feed(url):
    try:
        feed = feedparser.parse(url)
        if feed.bozo == 1:  # Check if there was an error parsing the feed
            st.error("Failed to fetch RSS feed. Please try again later.")
            return None
        return feed
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# RSS feed URL
rss_url = "https://sports.ndtv.com/rss/cricket"  # Make sure this is a valid RSS feed URL

# Fetch and display news
st.title("Latest Cricket News")
feed = fetch_rss_feed(rss_url)

if feed:
    for entry in feed.entries[:10]:  # Limit to 5 latest news
        st.subheader(entry.title)
        
        st.write(entry.summary)
        st.write(f"[Read more]({entry.link})")
        st.markdown("---")

if selected == "About":
      st.subheader("This website provides a detailed analysis of the T20 World Cup from 2007 to 2021. It offers comprehensive records for each World Cup, represented through various plots such as bar plots, pie plots, histograms, scatter plots, and line plots. We utilized powerful Python libraries, including NumPy for numerical operations, pandas for data manipulation, matplotlib for plotting, and Streamlit for creating interactive web applications. Additionally, the site includes interactive features that allow users to filter and explore the data in more depth.")
      st.markdown("---")
      st.markdown("Location : Mumbai 🗺️")

elif selected == "Contact":
     
 st.title("Contact Details")
 st.markdown("---")
 
 # Contact Information Section
 st.header("Our Team")
 
 # Contact Details for Anant Maurya
 st.subheader("Anant Maurya")
 st.markdown("""
 - **Phone No:** 9152990014
 - **GitHub Profile:** [mauryaanant005](https://github.com/mauryaanant005)
 - **Role:** Full Stack Developer with expertise in building scalable web applications and a passion for learning new technologies.
 """)
 
 # Contact Details for Anas Malkani
 st.subheader("Anas Malkani")
 st.markdown("""
 - **Phone No:** 7039372198
 - **GitHub Profile:** [ANASMALKANI189](https://github.com/ANASMALKANI189)
 - **Role:** Data Scientist focused on analyzing data and deriving actionable insights using statistical techniques and machine learning.
 """)
 
 # Contact Details for Rayyan Bhati
 st.subheader("Rayyan Bhati")
 st.markdown("""
 - **Phone No:** 8779811107
 - **GitHub Profile:** [RAYYAN2906](https://github.com/RAYYAN2906)
 - **Role:** Front-End Developer with a strong background in creating user-friendly interfaces and improving user experience through design.
 """)
 
 # Contact Details for Manas Londhe
 st.subheader("Manas Londhe")
 st.markdown("""
 - **Phone No:** 8850205475
 - **GitHub Profile:** [GamerMANAS09](https://github.com/GamerMANAS09)
 - **Role:** Backend Developer experienced in server-side logic and database management, passionate about optimizing performance and scalability.
 """)
 
 st.markdown("---")
 st.write("Feel free to reach out to any of us for collaboration or inquiries!")
 
 