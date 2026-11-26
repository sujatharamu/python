import streamlit as st

st.set_page_config(
    page_title="Cinema Ticket Booking",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Cinema Ticket Booking System")
st.write("Book your favourite movie tickets!")

# Default ticket prices
default_prices = {
    "Premium Class": 300,
    "First Class": 200,
    "Second Class": 120
}

# Available seats
seat_capacity = {
    "Premium Class": 30,
    "First Class": 50,
    "Second Class": 80
}

# Initialize session state
if "prices" not in st.session_state:
    st.session_state.prices = default_prices.copy()

if "bookings" not in st.session_state:
    st.session_state.bookings = []

# Admin price control
with st.expander("⚙️ Admin: Change Ticket Prices"):
    st.write("Update the price of each seat category.")

    for seat, price in st.session_state.prices.copy().items():
        st.session_state.prices[seat] = st.number_input(
            f"{seat} Price (₹)",
            min_value=1,
            max_value=5000,
            value=int(price),
            step=10,
            key=f"price_{seat}"
        )

# Customer details
st.subheader("Customer Details")

name = st.text_input("Enter Customer Name")

email = st.text_input("Enter Email Address")

# Movie selection
st.subheader("Movie Selection")

movies = [
    "Choose a Movie",
    "Avengers",
    "Avatar",
    "Jawan",
    "Pushpa 2",
    "KGF"
]

movie = st.selectbox("Select Movie", movies)

# Seat selection
st.subheader("Seat Selection")

seat_type = st.radio(
    "Choose Seat Type",
    ["Premium Class", "First Class", "Second Class"]
)

# Automatically get price
ticket_price = st.session_state.prices[seat_type]

available = seat_capacity[seat_type]

st.info(f"Ticket Price: ₹{ticket_price}")

st.write(f"Available seats: {available}")

# Ticket quantity
quantity = st.number_input(
    "Number of Tickets",
    min_value=1,
    max_value=10,
    value=1,
    step=1
)

# Calculate amount
total_price = ticket_price * quantity

st.subheader("Booking Summary")

st.write(f"**Movie:** {movie}")
st.write(f"**Seat Type:** {seat_type}")
st.write(f"**Tickets:** {quantity}")
st.write(f"**Price per Ticket:** ₹{ticket_price}")

st.markdown(f"### Total Amount: ₹{total_price}")

# Booking validation
if st.button("🎟️ Book Tickets", use_container_width=True):

    errors = []

    if not name.strip():
        errors.append("Customer name cannot be empty.")

    if not email.strip() or "@" not in email or "." not in email.split("@")[-1]:
        errors.append("Enter a valid email address.")

    if movie == "Choose a Movie":
        errors.append("Please select a movie.")

    if quantity < 1 or quantity > 10:
        errors.append("Ticket quantity must be between 1 and 10.")

    if quantity > available:
        errors.append("Not enough seats available.")

    if ticket_price <= 0:
        errors.append("Ticket price must be greater than zero.")

    if errors:
        for error in errors:
            st.error(error)

    else:
        booking = {
            "Customer": name,
            "Email": email,
            "Movie": movie,
            "Seat Type": seat_type,
            "Tickets": quantity,
            "Price": ticket_price,
            "Total": total_price
        }

        st.session_state.bookings.append(booking)

        st.success("🎉 Booking Successful!")

        st.write("### Your Ticket Details")

        st.write(f"Customer: {name}")
        st.write(f"Movie: {movie}")
        st.write(f"Seat Type: {seat_type}")
        st.write(f"Number of Tickets: {quantity}")
        st.write(f"Total Payment: ₹{total_price}")

        st.balloons()

# Booking history
st.divider()

st.subheader("📋 Booking History")

if st.session_state.bookings:
    st.dataframe(
        st.session_state.bookings,
        use_container_width=True
    )
else:
    st.info("No bookings available yet.")
