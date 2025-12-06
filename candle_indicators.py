class CandleIndicators:
    """
    Phân tích kỹ thuật cho một cây nến OHLC đơn lẻ
    Cung cấp các chỉ báo và mẫu hình nến cơ bản
    """

    def __init__(self, open_, high, low, close):
        """
        Khởi tạo với dữ liệu nến OHLC
        
        Parameters:
        -----------
        open_ : float
            Giá mở cửa
        high : float
            Giá cao nhất
        low : float
            Giá thấp nhất
        close : float
            Giá đóng cửa
        """
        self.open = open_
        self.high = high
        self.low = low
        self.close = close

    # =========================
    # ĐẶC TÍNH CƠ BẢN CỦA NẾN
    # =========================
    
    def candle_range(self):
        """
        Tính biên độ giá của nến (volatility trong phiên)
        
        Returns:
        --------
        float: Biên độ = High - Low
        """
        return self.high - self.low

    def body_size(self):
        """
        Tính kích thước thân nến (body)
        
        Returns:
        --------
        float: |Close - Open|
        """
        return abs(self.close - self.open)

    def body_ratio(self):
        """
        Tính tỷ lệ thân nến so với biên độ
        
        Công thức:
        ----------
        body_ratio = body_size / candle_range
        
        Returns:
        --------
        float: Tỷ lệ từ 0 đến 1
               0: Không có thân (doji hoàn hảo)
               1: Thân chiếm toàn bộ nến (không có bóng)
        """
        rng = self.candle_range()
        return 0 if rng == 0 else self.body_size() / rng

    # =========================
    # XÁC ĐỊNH XU HƯỚNG
    # =========================
    
    def candle_direction(self):
        """
        Xác định hướng của nến
        
        Returns:
        --------
        int: 1  : Nến tăng (tăng giá)
             -1 : Nến giảm (giảm giá)
              0 : Nến trung lập (doji)
        """
        if self.close > self.open:
            return 1
        elif self.close < self.open:
            return -1
        return 0

    # =========================
    # PHÂN TÍCH BÓNG NẾN
    # =========================
    
    def upper_shadow(self):
        """
        Tính độ dài bóng trên (upper shadow/wick)
        
        Returns:
        --------
        float: High - max(Open, Close)
        """
        return self.high - max(self.open, self.close)

    def lower_shadow(self):
        """
        Tính độ dài bóng dưới (lower shadow/wick)
        
        Returns:
        --------
        float: min(Open, Close) - Low
        """
        return min(self.open, self.close) - self.low

    def upper_shadow_ratio(self):
        """
        Tỷ lệ bóng trên so với biên độ
        
        Returns:
        --------
        float: Tỷ lệ từ 0 đến 1
               0: Không có bóng trên
               1: Bóng trên chiếm toàn bộ nến
        """
        rng = self.candle_range()
        return 0 if rng == 0 else self.upper_shadow() / rng

    def lower_shadow_ratio(self):
        """
        Tỷ lệ bóng dưới so với biên độ
        
        Returns:
        --------
        float: Tỷ lệ từ 0 đến 1
               0: Không có bóng dưới
               1: Bóng dưới chiếm toàn bộ nến
        """
        rng = self.candle_range()
        return 0 if rng == 0 else self.lower_shadow() / rng

    # =========================
    # VỊ TRÍ GIÁ TRONG NẾN
    # =========================
    
    def close_position(self):
        """
        Tính vị trí tương đối của giá đóng cửa trong biên độ nến
        
        Công thức:
        ----------
        position = (Close - Low) / (High - Low)
        
        Returns:
        --------
        float: Giá trị từ 0 đến 1
               0: Close = Low
               0.5: Close ở giữa nến
               1: Close = High
        """
        rng = self.candle_range()
        return 0.5 if rng == 0 else (self.close - self.low) / rng

    # =========================
    # ĐO LƯỜNG ĐỘ BIẾN ĐỘNG
    # =========================
    
    def true_range(self, prev_close):
        """
        Tính True Range (TR) - thước đo biến động có tính đến khoảng trống giá
        
        Công thức (theo Welles Wilder):
        TR = max(High - Low, 
                 |High - Previous Close|, 
                 |Low - Previous Close|)
        
        Parameters:
        -----------
        prev_close : float
            Giá đóng cửa của phiên trước
            
        Returns:
        --------
        float: True Range của phiên hiện tại
        """
        return max(
            self.high - self.low,
            abs(self.high - prev_close),
            abs(self.low - prev_close)
        )

    # =========================
    # NHẬN DIỆN MẪU HÌNH NẾN ĐƠN
    # =========================
    
    def is_doji(self, threshold=0.1):
        """
        Nhận diện nến Doji - thể hiện sự do dự của thị trường
        
        Doji là nến có thân rất nhỏ so với biên độ
        
        Parameters:
        -----------
        threshold : float, optional
            Ngưỡng tỷ lệ thân nến (mặc định 0.1 = 10%)
            
        Returns:
        --------
        bool: True nếu là nến Doji
        """
        return self.body_ratio() < threshold

    def is_hammer(self):
        """
        Nhận diện nến Hammer (Búa) - mẫu hình đảo chiều tăng
        
        Đặc điểm:
        ---------
        1. Bóng dưới dài (≥ 50% biên độ)
        2. Thân nhỏ (< 30% biên độ)
        3. Bóng trên rất ngắn hoặc không có
        
        Returns:
        --------
        bool: True nếu là nến Hammer
        """
        return (
            self.lower_shadow_ratio() > 0.5 and  # Bóng dưới chiếm >50%
            self.body_ratio() < 0.3              # Thân <30%
        )

    def is_shooting_star(self):
        """
        Nhận diện nến Shooting Star (Sao băng) - mẫu hình đảo chiều giảm
        
        Đặc điểm:
        ---------
        1. Bóng trên dài (≥ 50% biên độ)
        2. Thân nhỏ (< 30% biên độ)
        3. Bóng dưới rất ngắn hoặc không có
        
        Returns:
        --------
        bool: True nếu là nến Shooting Star
        """
        return (
            self.upper_shadow_ratio() > 0.5 and  # Bóng trên chiếm >50%
            self.body_ratio() < 0.3              # Thân <30%
        )

    def is_marubozu(self, threshold=0.95):
        """
        Nhận diện nến Marubozu - nến không có bóng
        
        Parameters:
        -----------
        threshold : float, optional
            Ngưỡng tỷ lệ thân nến (mặc định 0.95 = 95%)
            
        Returns:
        --------
        bool: True nếu là nến Marubozu
        """
        return self.body_ratio() > threshold

    def get_candle_type(self):
        """
        Phân loại nến theo nhiều đặc điểm
        
        Returns:
        --------
        dict: Dictionary chứa tất cả thông tin phân loại
        """
        return {
            'direction': self.candle_direction(),
            'is_doji': self.is_doji(),
            'is_hammer': self.is_hammer(),
            'is_shooting_star': self.is_shooting_star(),
            'is_marubozu': self.is_marubozu(),
            'body_ratio': self.body_ratio(),
            'upper_shadow_ratio': self.upper_shadow_ratio(),
            'lower_shadow_ratio': self.lower_shadow_ratio(),
            'close_position': self.close_position(),
            'range': self.candle_range(),
            'body_size': self.body_size()
        }