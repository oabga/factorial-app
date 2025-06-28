import streamlit as st
import os

def calculate_factorial(n):
    if(n == 0):
        return 1
    return n * calculate_factorial(n-1)

def load_users():
    try:
        if os.path.exists('user.txt'):
            with open(file='user.txt', encoding='utf-8') as f:
                users = [line.strip() for line in f.readlines()]
            return users
        else:
            st.error('File user.txt không tồn tại!')
    except Exception as e:
        st.error(f'Lỗi khi đọc file user.txt: {e}')
        return []
    return users
    
    
def logging_page():
    st.title("Đăng nhập")

    # Input username    
    username = st.text_input("Nhập tên người dùng:")

    if st.button("Đăng nhập"):
        if username:
            if username in load_users():
                st.session_state['right_permission'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                # Nếu user không có quyền
                st.session_state['username'] = username
                st.session_state['show_greeting'] = True
                st.rerun()
        else:
            st.warning("Vui lòng nhập tên người dùng!")


def factorial_page():
    st.title("Factorial Calculator")
    number = st.number_input(label='Enter a number:', min_value=0, max_value=900, format='%d')

    if st.button("Calculate"):
        st.markdown(f'<span style="color:green">The factorial of {number} \
                    is {calculate_factorial(number)}</span>',
                    unsafe_allow_html=True)
    
    if st.button("Exit"):
        st.session_state['right_permission'] = False
        st.session_state['username'] = ''
        st.rerun()
        

# page cho user không có quyền truy cập factorial
def greeting_page():
    st.title(f"Hello {st.session_state['username']}")
    st.markdown("## You don't have permission to factorial app")
    if st.button('Exit'):
        st.session_state['username'] = ''
        st.session_state['show_greeting'] = False
        st.rerun()
    

def main():

    if 'right_permission' not in st.session_state:
        st.session_state['right_permission'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = ''
    if 'show_greeting' not in st.session_state:
        st.session_state['show_greeting'] = False
    
    if st.session_state.show_greeting:
        greeting_page()
    elif st.session_state.right_permission:
        factorial_page()
    else:
        logging_page()
    

if __name__ == '__main__':
    main()

