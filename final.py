import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Stock Stack Manager", page_icon="📈", layout="wide")
#stock list:
TICKERS = {
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Google": "GOOGL"
}
#live prices:
@st.cache_data(ttl=60)
def get_price(ticker):
    try:
        return yf.Ticker(ticker).info.get("regularMarketPrice", 0)
    except:
        return 0

class Transaction:
    def __init__(self, action, ticker, shares, price):
        self.action = action
        self.ticker = ticker
        self.shares = shares
        self.price = price
        self.total = shares * price

    def __str__(self):
        return f"{self.action} | {self.ticker} | {self.shares} shares @ ${self.price:.2f}"

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if not self.is_empty() else None

    def peek(self):
        return self.items[-1] if not self.is_empty() else None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def display(self):
        return list(reversed(self.items))

class Portfolio:
    def __init__(self):
        self.stack = Stack()
        self.history = []

    def add_trade(self, action, ticker, shares):
        price = get_price(ticker)
        tx = Transaction(action, ticker, shares, price)
        self.stack.push(tx)
        self.history.append(
            {
                "Action": tx.action,
                "Ticker": tx.ticker,
                "Shares": tx.shares,
                "Price": round(tx.price, 2),
                "Total": round(tx.total, 2),
            }
        )
        return tx

if "portfolio" not in st.session_state:
    st.session_state.portfolio = Portfolio()

portfolio = st.session_state.portfolio

st.title("📈 Stock Transaction Manager using Stack")
st.caption("Demonstration of LIFO Stack Operations in Data Structures")

left, right = st.columns(2)
with left:
    st.subheader("New Transaction")

    company = st.selectbox("Select Company", list(TICKERS.keys()))
    ticker = TICKERS[company]

    shares = st.number_input("Number of Shares", min_value=1, value=1)

    action = st.radio("Choose Action", ["BUY", "SELL"], horizontal=True)

    if st.button("Push Transaction"):
        tx = portfolio.add_trade(action, ticker, shares)
        st.success(f"PUSH Successful: {tx}")

    st.divider()

    st.subheader("Stack Operations")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Peek Top"):
            top = portfolio.stack.peek()
            if top:
                st.info(f"TOP: {top}")
            else:
                st.warning("Stack is Empty")

    with c2:
        if st.button("Pop Transaction"):
            removed = portfolio.stack.pop()
            if removed:
                st.warning(f"POP Successful: {removed}")
            else:
                st.warning("Stack is Empty")

    st.divider()

    st.metric("Stack Size", portfolio.stack.size())
with right:
    st.subheader("Stack Visualization (LIFO)")

    if portfolio.stack.is_empty():
        st.info("Stack Empty")
    else:
        stack_data = portfolio.stack.display()

        for i, tx in enumerate(stack_data):
            if i == 0:
                st.success(f"🔝 TOP → {tx}")
            else:
                st.write(tx)

    st.divider()

    st.subheader("Transaction History")

    if portfolio.history:
        st.dataframe(pd.DataFrame(portfolio.history), use_container_width=True)
    else:
        st.write("No transactions yet.")