import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def enhanced_stock_predictor():
    print("\nWelcome to the Detailed Stock Price Predictor with Metrics and Visualization!")
    ticker = input("Enter stock ticker symbol (e.g., AAPL, TSLA): ").upper()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty or 'Close' not in data.columns:
        print(f"No closing price data available for {ticker}.")
        return
    data = data.reset_index()
    data['Day_Num'] = np.arange(len(data))
    train_size = int(len(data)*0.8)
    train = data.iloc[:train_size]
    test = data.iloc[train_size:]
    X_train = train[['Day_Num']].values
    y_train = train['Close'].values
    X_test = test[['Day_Num']].values
    y_test = test['Close'].values
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"\nModel Performance on test set:")
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"R-squared: {r2:.4f}")
    future_days = np.arange(len(data), len(data) + 5).reshape(-1, 1)
    future_preds = model.predict(future_days)
    print(f"\nNext 5 day stock price predictions for {ticker}:")
    for i, price in enumerate(future_preds, 1):
        pred_date = end_date + timedelta(days=i)
        print(f"{pred_date.strftime('%Y-%m-%d')}: ${price:.2f}")
    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'], data['Close'], label='Historical Close Price')
    plt.plot(test['Date'], y_pred, label='Test Set Prediction')
    future_dates = [end_date + timedelta(days=i) for i in range(1, 6)]
    plt.plot(future_dates, future_preds, 'ro--', label='Future Predictions')
    plt.title(f"Stock Price Prediction with Linear Regression - {ticker}")
    plt.xlabel('Date')
    plt.ylabel('Close Price ($)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    enhanced_stock_predictor()
