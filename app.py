import streamlit as st
import os
from google import genai

# ১. অ্যাপের টাইটেল এবং সেটআপ
st.set_page_config(page_title="আমার AI চ্যাটবট", page_icon="🤖", layout="centered")

# --- সাইডবার ডিজাইন (আপনার নাম, টিমের নাম ও লোগো) ---
st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <h2 style="color: #00FFAA; margin-bottom: 0;">BCE_Anowar Hossan</h2>
        <p style="color: #888; font-size: 14px; margin-top: 5px;">Founder & Developer</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# লোগো দেখানোর ব্যবস্থা
# আপনার লোগো ছবির ফাইলের নাম 'logo.png' হলে সেটি কোড ফাইলের সাথে আপলোড করে দিন
try:
    st.sidebar.image("logo.png", use_container_width=True)
except:
    st.sidebar.markdown(
        """
        <div style="background-color: #262730; padding: 20px; border-radius: 10px; text-align: center; border: 1px dashed #444;">
            <span style="color: #888;">🤖 [আপনার লোগো (logo.png) এখানে আপলোড করুন]</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

st.sidebar.markdown("---")

# টিমের নাম ও বিবরণী ডিজাইন
st.sidebar.markdown(
    """
    <div style="background-color: #1E1E24; padding: 15px; border-radius: 8px; border-left: 5px solid #00FFAA;">
        <h4 style="margin: 0; color: #FFF;">🎯 টিম ইনফো</h4>
        <p style="margin: 5px 0 0 0; color: #00FFAA; font-weight: bold; font-size: 16px;">Bhujpur Cyber Expert</p>
        <p style="margin: 5px 0 0 0; color: #AAA; font-size: 13px;">ডিজিটাল নিরাপত্তা ও প্রযুক্তিগত সহায়তা দল।</p>
    </div>
    """, 
    unsafe_allow_html=True
)

st.sidebar.markdown("<br><br><br><p style='text-align: center; color: #555; font-size: 12px;'>© ২০২৬ BCE Team | সর্বস্বত্ব সংরক্ষিত</p>", unsafe_allow_html=True)
# ---------------------------------------------

# মূল স্ক্রিনের টাইটেল ও ইন্টারফেস
st.title("🤖 আমার নিজস্ব AI চ্যাটবট")
st.write("Gemini API দ্বারা চালিত আপনার ব্যক্তিগত সহকারী।")

# ২. Gemini API কী সেটআপ (Streamlit Secrets থেকে নেওয়া হচ্ছে)
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "YOUR_GEMINI_API_KEY_HERE" # লোকাল টেস্টের জন্য এখানে আপনার এপিআই কী বসাতে পারেন

# Gemini ক্লায়েন্ট তৈরি
client = genai.Client(api_key=API_KEY)

# ৩. চ্যাট হিস্ট্রি (মেসেজ রেকর্ড) ধরে রাখার ব্যবস্থা
if "messages" not in st.session_state:
    st.session_state.messages = []

# আগের কথাগুলো স্ক্রিনে দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৪. ইউজারের কাছ থেকে ইনপুট নেওয়া
if user_input := st.chat_input("আমাকে যেকোনো প্রশ্ন করুন..."):
    
    # ইউজারের মেসেজ স্ক্রিনে দেখানো এবং হিস্ট্রিতে সেভ করা
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # বটের উত্তরের জন্য লোডিং অ্যানিমেশন
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Gemini থেকে উত্তর আনা
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_input,
            )
            bot_reply = response.text
            
            # বটের উত্তর স্ক্রিনে দেখানো
            message_placeholder.markdown(bot_reply)
            
            # বটের উত্তর হিস্ট্রিতে সেভ করা
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            message_placeholder.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")
      
