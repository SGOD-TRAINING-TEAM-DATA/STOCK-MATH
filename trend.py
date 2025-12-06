import pandas as pd
import numpy as np
from candle_indicators import CandleIndicators

class TrendIndicators:
    """
    Tính các chỉ báo kỹ thuật dựa trên NHIỀU nến (time series)
    """

    def __init__(self, df: pd.DataFrame):
        """
        df cần có các cột: Open, High, Low, Close
        """
        self.df = df.copy()
        self._validate_dataframe()
    
    def _validate_dataframe(self):
        """Kiểm tra dữ liệu đầu vào"""
        required_columns = ['Open', 'High', 'Low', 'Close']
        for col in required_columns:
            if col not in self.df.columns:
                raise ValueError(f"Thiếu cột bắt buộc: {col}")
        
        # Kiểm tra tính hợp lệ của OHLC
        mask_invalid = (
            (self.df['High'] < self.df['Low']) |
            (self.df['High'] < self.df[['Open', 'Close']].max(axis=1)) |
            (self.df['Low'] > self.df[['Open', 'Close']].min(axis=1))
        )
        
        if mask_invalid.any():
            print(f"Cảnh báo: Phát hiện {mask_invalid.sum()} nến có dữ liệu OHLC không hợp lệ")
            print("Đang tự động điều chỉnh...")
            
            # Điều chỉnh tự động
            self.df['High'] = self.df[['Open', 'High', 'Close']].max(axis=1)
            self.df['Low'] = self.df[['Open', 'Low', 'Close']].min(axis=1)

    # =========================
    # MOVING AVERAGE
    # =========================
    def SMA(self, window=20):
        if len(self.df) < window:
            print(f"Cảnh báo: Cần ít nhất {window} nến để tính SMA")
            self.df[f"SMA_{window}"] = np.nan
        else:
            self.df[f"SMA_{window}"] = self.df["Close"].rolling(window).mean()
        return self.df[f"SMA_{window}"]

    def EMA(self, window=20):
        if len(self.df) < window:
            print(f"Cảnh báo: Cần ít nhất {window} nến để tính EMA")
            self.df[f"EMA_{window}"] = np.nan
        else:
            self.df[f"EMA_{window}"] = self.df["Close"].ewm(span=window, adjust=False).mean()
        return self.df[f"EMA_{window}"]

    # =========================
    # MACD
    # =========================
    def MACD(self, fast=12, slow=26, signal=9):
        if len(self.df) < slow:
            print(f"Cảnh báo: Cần ít nhất {slow} nến để tính MACD")
            self.df["MACD"] = np.nan
            self.df["MACD_Signal"] = np.nan
            self.df["MACD_Histogram"] = np.nan
        else:
            ema_fast = self.df["Close"].ewm(span=fast, adjust=False).mean()
            ema_slow = self.df["Close"].ewm(span=slow, adjust=False).mean()

            self.df["MACD"] = ema_fast - ema_slow
            self.df["MACD_Signal"] = self.df["MACD"].ewm(span=signal, adjust=False).mean()
            self.df["MACD_Histogram"] = self.df["MACD"] - self.df["MACD_Signal"]

        return self.df[["MACD", "MACD_Signal", "MACD_Histogram"]]

    # =========================
    # RSI
    # =========================
    def RSI(self, window=14):
        if len(self.df) < window + 1:
            print(f"Cảnh báo: Cần ít nhất {window + 1} nến để tính RSI")
            self.df["RSI"] = np.nan
        else:
            delta = self.df["Close"].diff()

            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)

            avg_gain = gain.rolling(window).mean()
            avg_loss = loss.rolling(window).mean()

            rs = avg_gain / avg_loss
            self.df["RSI"] = 100 - (100 / (1 + rs))

        return self.df["RSI"]

    # =========================
    # BOLLINGER BANDS
    # =========================
    def Bollinger_Bands(self, window=20, num_std=2):
        if len(self.df) < window:
            print(f"Cảnh báo: Cần ít nhất {window} nến để tính Bollinger Bands")
            self.df["BB_Middle"] = np.nan
            self.df["BB_Upper"] = np.nan
            self.df["BB_Lower"] = np.nan
        else:
            sma = self.df["Close"].rolling(window).mean()
            std = self.df["Close"].rolling(window).std()

            self.df["BB_Middle"] = sma
            self.df["BB_Upper"] = sma + num_std * std
            self.df["BB_Lower"] = sma - num_std * std

        return self.df[["BB_Upper", "BB_Middle", "BB_Lower"]]

    # =========================
    # COMBINE WITH CANDLE FEATURES
    # =========================
    def add_candle_features(self):
        features = []

        for _, row in self.df.iterrows():
            candle = CandleIndicators(
                row["Open"], row["High"], row["Low"], row["Close"]
            )
            features.append(candle.get_candle_type())

        candle_df = pd.DataFrame(features, index=self.df.index)
        self.df = pd.concat([self.df, candle_df], axis=1)

        return candle_df

    # =========================
    # GET DATA
    # =========================
    def get_dataframe(self):
        return self.df
    
    def get_summary(self):
        """Trả về thống kê tổng quan"""
        summary = {
            'Tổng số nến': len(self.df),
            'Các chỉ báo đã tính': [col for col in self.df.columns if 'SMA' in col or 'EMA' in col or 'MACD' in col or 'RSI' in col or 'BB_' in col],
            'Số nến có chỉ báo nến': self.df['direction'].notna().sum() if 'direction' in self.df.columns else 0
        }
        return summary