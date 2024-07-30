import streamlit as st
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="xxxx",
        database="users"
    )

def fetch_subscription_plans():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    query = "SELECT subscription_id, plan_name, features, price, duration FROM subscription"
    cursor.execute(query)
    plans = cursor.fetchall()
    cursor.close()
    db.close()
    return plans

def fetch_user_id(email):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    query = "SELECT user_id, name, email, phno FROM user WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return user

def fetch_user_subscription(user_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT us.subscription_id, s.plan_name, us.start_date, us.end_date
    FROM user_subscription us
    JOIN subscription s ON us.subscription_id = s.subscription_id
    WHERE us.user_id = %s AND us.end_date >= CURDATE()
    """
    cursor.execute(query, (user_id,))
    subscription = cursor.fetchone()
    cursor.close()
    db.close()
    return subscription

def create_user_subscription(user_id, subscription_id):
    db = get_db_connection()
    cursor = db.cursor()
    query = "INSERT INTO user_subscription (user_id, subscription_id, start_date, end_date) VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 1 MONTH))"
    cursor.execute(query, (user_id, subscription_id))
    db.commit()
    cursor.close()
    db.close()

def subscription():
    st.header("Subscription")
    
    # Description
    st.write("""
        Subscribe to our premium services to unlock additional features and benefits.
        Our subscription plans are designed to suit your needs and help you get the most out of our platform.
    """)

    # Fetch subscription plans from the database
    plans = fetch_subscription_plans()
    
    if not plans:
        st.error("No subscription plans available.")
        return

    # Initialize session state for selected plan
    if "selected_plan" not in st.session_state:
        st.session_state.selected_plan = None

    # Subscription Options
    st.subheader("Choose Your Plan")
    
    col1, col2, col3, col4 = st.columns(4)
    
    for i, plan in enumerate(plans):
        with eval(f"col{i+1}"):
            st.markdown("""
            <style>
            .card {
                background-color: lightblue;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
                text-align: center;
            }
            .card-title {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .card-features {
                text-align: left;
            }
            </style>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card">
                <div class="card-title">{plan['plan_name']}</div>
                <div class="card-features">
                    <ul>
                        {''.join([f'<li>{feature}</li>' for feature in plan['features'].split(', ')])}
                        <li>Price: {plan['price']}$</li>
                        <li>Duration: {plan['duration']}</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            # if st.button(f"Subscribe - {plan['plan_name']}"):
            #     st.session_state.selected_plan = plan['subscription_id']
    with col4:
        st.write("**Select Plan from here**")
        with st.form(key="plan_form"):
            if st.form_submit_button("Subscribe - Basic"):
                st.session_state.selected_plan = next((plan['subscription_id'] for plan in plans if plan['plan_name'] == "Basic Plan"), None)
            if st.form_submit_button("Subscribe - Standard"):
                st.session_state.selected_plan = next((plan['subscription_id'] for plan in plans if plan['plan_name'] == "Standard Plan"), None)
            if st.form_submit_button("Subscribe - Premium"):
                st.session_state.selected_plan = next((plan['subscription_id'] for plan in plans if plan['plan_name'] == "Premium Plan"), None)
                
    # User Information Form
    st.subheader("Enter Your Details")
    with st.form("subscription_form"):
        email = st.text_input("Email")
        user = fetch_user_id(email)
        user_id=0
        subscription = None
        if user:
            user_id = user['user_id']
            subscription = fetch_user_subscription(user_id)
        col1, col2 = st.columns(2)
        with col1:
            s1 = st.form_submit_button("Check subscription")
        with col2:
            s2 = None  # Initialize s2 to None
            if not subscription:
                s2 = st.form_submit_button("Subscribe Now!")
            else:
                st.success("Already subscribed!")

        if s1:
            if user:
                # st.write(f"User found: {user['name']}")
                name = st.text_input("Name", value=user['name'])
                phone = st.text_input("Phone", value=user['phno'])
                user_id = user['user_id']
                subscription = fetch_user_subscription(user_id)

                if subscription:
                    st.success(f"You are already subscribed to the {subscription['plan_name']} plan until {subscription['end_date']}.")
                    st.stop()  # Stop further execution if already subscribed
                else:
                    st.error("Not subscribed")
                    st.warning("Note: If you want to subscribe please select the plan first and then click on subscribe button.")
            else:
                st.error("User not found. Please register first.")
        
        if s2:
            if user:
                st.write(f"User found: {user['name']}")
                name = st.text_input("Name", value=user['name'])
                phone = st.text_input("Phone", value=user['phno'])
                user_id = user['user_id']
                plan_id = st.text_input("Selected Plan ID", value=st.session_state.selected_plan, disabled=True)
                create_user_subscription(user_id, st.session_state.selected_plan)
                st.success("Thank you for subscribing!")
                # st.write(f"Name: {name}")
                st.write(f"Selected Plan: {plan_id}")
            else:
                st.error("User not found. Please register first.")

if __name__ == "__main__":
    subscription()