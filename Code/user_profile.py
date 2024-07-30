import streamlit as st
import mysql.connector
import hashlib

# Function to get database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="xxxxx",
        database="users"
    )

# Function to fetch user info from database
def fetch_user_info(email):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    query = "SELECT user_id, name, email, phno FROM user WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result

# Function to fetch user subscription history
def fetch_user_subscriptions(user_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT s.plan_name, s.price, s.duration, us.start_date, us.end_date 
        FROM user_subscription us
        JOIN subscription s ON us.subscription_id = s.subscription_id
        WHERE us.user_id = %s
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

# Function to update user info in database
def update_user_info(email, name, phone):
    db = get_db_connection()
    cursor = db.cursor()
    query = "UPDATE user SET name = %s, phno = %s WHERE email = %s"
    cursor.execute(query, (name, phone, email))
    db.commit()
    cursor.close()
    db.close()

# Function to change user password
def change_user_password(email, new_password):
    db = get_db_connection()
    cursor = db.cursor()
    query = "UPDATE user SET password = %s WHERE email = %s"
    cursor.execute(query, (new_password, email))
    db.commit()
    cursor.close()
    db.close()

# Function to delete user account
def delete_user_account(email):
    db = get_db_connection()
    cursor = db.cursor()
    query = "DELETE FROM user WHERE email = %s"
    cursor.execute(query, (email,))
    db.commit()
    cursor.close()
    db.close()

def user_profile():
    st.header("User Profile")

    email = st.session_state.get("user")  # Assuming the logged-in user email is stored in session state
    
    if not email:
        st.error("User not logged in!")
        return

    # Fetch user information from the database
    user_info = fetch_user_info(email)
    
    if user_info:
        if "user_info" not in st.session_state:
            st.session_state.user_info = user_info
        else:
            st.session_state.user_info.update(user_info)
    else:
        st.error("User information could not be loaded. Because you are a Guest")
        return

    st.subheader("Edit Your Information")
    
    # User Information Form
    with st.form("user_info_form"):
        name = st.text_input("Name", value=st.session_state.user_info.get("name", ""))
        email = st.text_input("Email", value=st.session_state.user_info.get("email", ""), disabled=True)
        phone = st.text_input("Phone", value=st.session_state.user_info.get("phno", ""))
        submitted = st.form_submit_button("Update Information")
        
        if submitted:
            update_user_info(email, name, phone)
            st.session_state.user_info["name"] = name
            st.session_state.user_info["phno"] = phone
            st.success("Information updated successfully!")

    st.subheader("Your Plan")
    # plan = st.session_state.user_info.get("plan", "Not Set")
    subscriptions = fetch_user_subscriptions(st.session_state.user_info.get("user_id"))
    if subscriptions:
        for sub in subscriptions:
            st.write(f"**Current Name:** {sub['plan_name']}")

    st.subheader("Additional Features")
    st.write("Here you can add more features for the user to interact with.")

    col1, col2= st.columns(2)

    with col1:
        options = ["Select","View Subscription","Change Password", "Delete Account"]
        ch_pass = st.selectbox("Choose an option:", options)

    with col2:
        if ch_pass == "Select":
            pass
        if ch_pass == "View Subscription":
            st.write("**Subscription History**")
            subscriptions = fetch_user_subscriptions(st.session_state.user_info.get("user_id"))
            if subscriptions:
                for sub in subscriptions:
                    st.write(f"**Plan Name:** {sub['plan_name']}")
                    st.write(f"**Price:** {sub['price']}$")
                    st.write(f"**Duration:** {sub['duration']}")
                    st.write(f"**Start Date:** {sub['start_date']}")
                    st.write(f"**End Date:** {sub['end_date']}")
            else:
                st.write("No subscription history available.")
        if ch_pass == "Change Password":
            with st.form("change_password_form"):
                st.write("Change Password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit_password_change = st.form_submit_button("Submit")
                
                if submit_password_change:
                    if new_password == confirm_password:
                        change_user_password(email, new_password)
                        st.success("Password changed successfully!")
                    else:
                        st.error("Passwords do not match.")

        if ch_pass == "Delete Account":
            with st.form("delete_account_form"):
                st.write("Delete Account")
                confirm_delete = st.form_submit_button("Confirm Delete")
                
                if confirm_delete:
                    delete_user_account(email)
                    st.success("Account deleted successfully!")
                    st.session_state.clear()  # Clear session state
                    st.experimental_rerun()  # Redirect to login page (you need to handle the login redirection)

if __name__ == "__main__":
    user_profile()
