import pandas as pd
from candle_indicators import CandleIndicators
from trend import TrendIndicators

def analyze_from_csv(file_path="candles.csv"):
    """Phân tích dữ liệu từ file CSV với các chỉ báo xu hướng"""
    try:
        df = pd.read_csv(file_path)
        
        # Khởi tạo chỉ báo xu hướng
        indicator = TrendIndicators(df)
        # Tính các chỉ báo xu hướng
        indicator.SMA(20)
        indicator.EMA(20)
        indicator.MACD()
        indicator.RSI(14)
        indicator.Bollinger_Bands()
        
        # Thêm đặc điểm nến đơn
        indicator.add_candle_features()
        
        # Lấy DataFrame kết quả
        final_df = indicator.get_dataframe()
        
        print("\n" + "="*60)
        print("KẾT QUẢ PHÂN TÍCH TỪ FILE CSV")
        print("="*60)
        print(f"Số lượng nến: {len(final_df)}")
        print(f"Các chỉ báo đã tính: {[col for col in final_df.columns if 'SMA' in col or 'EMA' in col or 'MACD' in col or 'RSI' in col or 'BB_' in col]}")
        print("\n5 nến gần nhất:")
        print(final_df.tail())
        
        # Lưu kết quả ra file
        output_file = "candles_analyzed.csv"
        final_df.to_csv(output_file, index=False)
        print(f"\nĐã lưu kết quả vào: {output_file}")
        
        return final_df
        
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
        print("Vui lòng kiểm tra đường dẫn hoặc chọn chức năng khác.")
        return None
    except Exception as e:
        print(f"Lỗi khi đọc file CSV: {e}")
        return None

def get_candle_data_from_keyboard():
    """
    Nhập dữ liệu nến từ bàn phím
    
    Returns:
    --------
    tuple: (open_price, high_price, low_price, close_price)
    """
    print("\n" + "="*50)
    print("NHẬP DỮ LIỆU NẾN TỪ BÀN PHÍM")
    print("="*50)
    
    try:
        open_price = float(input("Nhập giá MỞ cửa (Open): "))
        high_price = float(input("Nhập giá CAO nhất (High): "))
        low_price = float(input("Nhập giá THẤP nhất (Low): "))
        close_price = float(input("Nhập giá ĐÓNG cửa (Close): "))
        
        # Kiểm tra tính hợp lệ của dữ liệu
        if high_price < low_price:
            print("Cảnh báo: High phải lớn hơn hoặc bằng Low!")
            high_price, low_price = max(high_price, low_price), min(high_price, low_price)
            print(f"Đã tự động điều chỉnh: High={high_price}, Low={low_price}")
        
        if high_price < max(open_price, close_price):
            print("Cảnh báo: High phải lớn hơn hoặc bằng Open và Close!")
            high_price = max(open_price, close_price, high_price)
            print(f"Đã tự động điều chỉnh: High={high_price}")
        
        if low_price > min(open_price, close_price):
            print("Cảnh báo: Low phải nhỏ hơn hoặc bằng Open và Close!")
            low_price = min(open_price, close_price, low_price)
            print(f"Đã tự động điều chỉnh: Low={low_price}")
        
        return open_price, high_price, low_price, close_price
        
    except ValueError:
        print("Lỗi: Vui lòng nhập số hợp lệ!")
        return None

def analyze_single_candle_interactive():
    """Phân tích một cây nến với dữ liệu nhập từ bàn phím"""
    while True:
        # Nhập dữ liệu từ bàn phím
        data = get_candle_data_from_keyboard()
        if data is None:
            print("Dữ liệu không hợp lệ. Vui lòng thử lại!")
            continue
        
        open_price, high_price, low_price, close_price = data
        
        # Tạo đối tượng phân tích
        candle = CandleIndicators(open_price, high_price, low_price, close_price)
        
        # Phân tích các chỉ số
        print("\n" + "="*50)
        print(" KẾT QUẢ PHÂN TÍCH NẾN")
        print("="*50)
        print(f"Giá mở (Open): {open_price:,.2f}")
        print(f"Giá cao (High): {high_price:,.2f}")
        print(f"Giá thấp (Low): {low_price:,.2f}")
        print(f"Giá đóng (Close): {close_price:,.2f}")
        print("-" * 50)
        print(f"Biên độ nến: {candle.candle_range():,.2f}")
        print(f" Kích thước thân: {candle.body_size():,.2f}")
        print(f" Tỷ lệ thân: {candle.body_ratio():.2%}")
        
        # Hiển thị hướng nến
        direction = candle.candle_direction()
        direction_text = "TĂNG " if direction == 1 else "GIẢM " if direction == -1 else "DOJI ⚪"
        print(f" Hướng nến: {direction_text} ({direction})")
        
        print(f" Bóng trên: {candle.upper_shadow():,.2f}")
        print(f" Bóng dưới: {candle.lower_shadow():,.2f}")
        print(f" Vị trí đóng cửa: {candle.close_position():.2%}")
        
        # Phân loại nến
        print("\n" + "="*50)
        print(" PHÂN LOẠI MẪU HÌNH NẾN")
        print("="*50)
        
        patterns = []
        if candle.is_doji():
            patterns.append(" Doji (Nến do dự)")
        if candle.is_hammer():
            patterns.append(" Hammer (Búa - Tín hiệu tăng)")
        if candle.is_shooting_star():
            patterns.append(" Shooting Star (Sao băng - Tín hiệu giảm)")
        if candle.is_marubozu():
            patterns.append(" Marubozu (Nến không bóng)")
        
        if patterns:
            for pattern in patterns:
                print(f" {pattern}")
        else:
            print("  Không phát hiện mẫu hình đặc biệt")
        
        # Lấy tất cả thông tin
        print("\n" + "="*50)
        print(" TỔNG HỢP CHỈ SỐ CHI TIẾT")
        print("="*50)
        candle_info = candle.get_candle_type()
        
        # Format hiển thị đẹp hơn
        info_display = {
            'direction': 'Tăng' if candle_info['direction'] == 1 else 
                        'Giảm' if candle_info['direction'] == -1 else 'Doji',
            'is_doji': 'Có' if candle_info['is_doji'] else 'Không',
            'is_hammer': 'Có' if candle_info['is_hammer'] else 'Không',
            'is_shooting_star': 'Có' if candle_info['is_shooting_star'] else 'Không',
            'is_marubozu': 'Có' if candle_info['is_marubozu'] else 'Không',
            'body_ratio': f"{candle_info['body_ratio']:.2%}",
            'upper_shadow_ratio': f"{candle_info['upper_shadow_ratio']:.2%}",
            'lower_shadow_ratio': f"{candle_info['lower_shadow_ratio']:.2%}",
            'close_position': f"{candle_info['close_position']:.2%}",
            'range': f"{candle_info['range']:,.2f}",
            'body_size': f"{candle_info['body_size']:,.2f}"
        }
        
        for key, value in info_display.items():
            # Chuyển tên key sang tiếng Việt
            display_names = {
                'direction': 'Hướng nến',
                'is_doji': 'Có phải Doji',
                'is_hammer': 'Có phải Hammer',
                'is_shooting_star': 'Có phải Shooting Star',
                'is_marubozu': 'Có phải Marubozu',
                'body_ratio': 'Tỷ lệ thân',
                'upper_shadow_ratio': 'Tỷ lệ bóng trên',
                'lower_shadow_ratio': 'Tỷ lệ bóng dưới',
                'close_position': 'Vị trí đóng cửa',
                'range': 'Biên độ',
                'body_size': 'Kích thước thân'
            }
            print(f"{display_names[key]}: {value}")
        
        # Hỏi người dùng có muốn tiếp tục không
        print("\n" + "="*50)
        choice = input("Bạn có muốn phân tích nến khác? (y/n): ").lower()
        if choice != 'y':
            break

def analyze_multiple_candles_interactive():
    """Phân tích nhiều cây nến với dữ liệu nhập từ bàn phím"""
    results = []
    
    print("\n" + "="*50)
    print(" PHÂN TÍCH NHIỀU NẾN")
    print("="*50)
    
    try:
        n = int(input("Nhập số lượng nến muốn phân tích: "))
        if n <= 0:
            print(" Số lượng nến phải lớn hơn 0!")
            return None
        
        prev_close = None
        
        for i in range(n):
            print(f"\n--- Nến thứ {i+1} ---")
            
            # Nhập dữ liệu cho từng nến
            data = get_candle_data_from_keyboard()
            if data is None:
                print(" Dữ liệu không hợp lệ, bỏ qua nến này!")
                continue
            
            open_price, high_price, low_price, close_price = data
            
            # Tạo đối tượng phân tích
            candle = CandleIndicators(open_price, high_price, low_price, close_price)
            
            # Tính True Range nếu có nến trước
            tr = candle.candle_range()
            if prev_close is not None:
                tr = candle.true_range(prev_close)
            
            results.append({
                'STT': i+1,
                'Open': open_price,
                'High': high_price,
                'Low': low_price,
                'Close': close_price,
                'Direction': 'Tăng' if candle.candle_direction() == 1 else 
                            'Giảm' if candle.candle_direction() == -1 else 'Doji',
                'Body_Ratio': f"{candle.body_ratio():.2%}",
                'Is_Doji': 'Có' if candle.is_doji() else 'Không',
                'Is_Hammer': 'Có' if candle.is_hammer() else 'Không',
                'True_Range': f"{tr:.2f}"
            })
            
            prev_close = close_price
        
        return pd.DataFrame(results)
        
    except ValueError:
        print(" Vui lòng nhập số hợp lệ!")
        return None

def create_sample_data():
    """Tạo dữ liệu mẫu và phân tích với trend indicators"""
    import numpy as np
    
    print("\n" + "="*60)
    print("TẠO VÀ PHÂN TÍCH DỮ LIỆU MẪU")
    print("="*60)
    
    try:
        num_candles = int(input("Nhập số lượng nến mẫu muốn tạo (mặc định 50): ") or "50")
        
        if num_candles < 20:
            print("Cảnh báo: Cần ít nhất 20 nến để tính các chỉ báo xu hướng!")
            num_candles = max(num_candles, 20)
            print(f"Đã điều chỉnh thành {num_candles} nến")
        
        # Tạo dữ liệu mẫu ngẫu nhiên nhưng có xu hướng
        np.random.seed(42)  # Để kết quả có thể tái lặp
        
        # Tạo giá đóng cửa cơ bản với xu hướng tăng nhẹ
        base_price = 100
        close_prices = [base_price]
        
        for i in range(1, num_candles):
            # Thêm biến động ngẫu nhiên
            change = np.random.normal(0.1, 2)  # Xu hướng tăng nhẹ 0.1
            new_price = close_prices[-1] + change
            close_prices.append(max(new_price, 1))  # Đảm bảo giá > 0
        
        # Tạo Open, High, Low từ Close
        opens = []
        highs = []
        lows = []
        
        for i in range(num_candles):
            close = close_prices[i]
            
            # Open gần với close của nến trước (trừ nến đầu)
            if i == 0:
                open_price = close * np.random.uniform(0.95, 1.05)
            else:
                open_price = close_prices[i-1] * np.random.uniform(0.98, 1.02)
            
            # Xác định phạm vi biến động trong phiên
            volatility = abs(close - open_price) * np.random.uniform(1.5, 3)
            
            # High và Low
            high = max(open_price, close) + volatility * np.random.uniform(0.2, 0.6)
            low = min(open_price, close) - volatility * np.random.uniform(0.2, 0.6)
            
            # Đảm bảo High >= Open, Close và Low <= Open, Close
            high = max(high, open_price, close)
            low = min(low, open_price, close)
            
            opens.append(round(open_price, 2))
            highs.append(round(high, 2))
            lows.append(round(low, 2))
            close_prices[i] = round(close, 2)
        
        # Tạo DataFrame
        dates = pd.date_range(start='2024-01-01', periods=num_candles, freq='D')
        df = pd.DataFrame({
            'Date': dates,
            'Open': opens,
            'High': highs,
            'Low': lows,
            'Close': close_prices
        })
        
        print(f"\nĐã tạo {num_candles} nến mẫu:")
        print(df.head(10))
        
        if num_candles > 10:
            print(f"... và {num_candles - 10} nến còn lại")
        
        # Lưu dữ liệu mẫu ra file CSV
        sample_file = "sample_candles.csv"
        df.to_csv(sample_file, index=False)
        print(f"\nĐã lưu dữ liệu mẫu vào: {sample_file}")
        
        # Phân tích với trend indicators
        print("\n" + "="*60)
        print("PHÂN TÍCH DỮ LIỆU MẪU VỚI CHỈ BÁO XU HƯỚNG")
        print("="*60)
        
        indicator = TrendIndicators(df)
        
        # Tính các chỉ báo xu hướng
        indicator.SMA(20)
        indicator.EMA(20)
        indicator.MACD()
        indicator.RSI(14)
        indicator.Bollinger_Bands()
        
        # Thêm đặc điểm nến đơn
        indicator.add_candle_features()
        
        # Lấy DataFrame kết quả
        final_df = indicator.get_dataframe()
        
        # Hiển thị thống kê
        print(f"\nTổng số nến: {len(final_df)}")
        
        if 'direction' in final_df.columns:
            direction_counts = final_df['direction'].value_counts()
            print(f"Số nến tăng (direction=1): {direction_counts.get(1, 0)}")
            print(f"Số nến giảm (direction=-1): {direction_counts.get(-1, 0)}")
            print(f"Số nến Doji (direction=0): {direction_counts.get(0, 0)}")
        
        # Hiển thị các chỉ báo tính được
        print("\nCác chỉ báo đã tính toán:")
        trend_cols = [col for col in final_df.columns if any(x in col for x in ['SMA', 'EMA', 'MACD', 'RSI', 'BB_', 'is_'])]
        for col in trend_cols:
            non_na_count = final_df[col].notna().sum()
            print(f"  - {col}: có giá trị cho {non_na_count}/{len(final_df)} nến")
        
        # Hiển thị 5 nến cuối với đầy đủ thông tin
        print("\n5 nến cuối cùng với chỉ báo:")
        display_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'direction']
        if 'SMA_20' in final_df.columns:
            display_cols.append('SMA_20')
        if 'EMA_20' in final_df.columns:
            display_cols.append('EMA_20')
        if 'RSI' in final_df.columns:
            display_cols.append('RSI')
        
        display_df = final_df[display_cols].tail()
        print(display_df.to_string(index=False))
        
        # Lưu kết quả phân tích
        analyzed_file = "sample_analyzed.csv"
        final_df.to_csv(analyzed_file, index=False)
        print(f"\nĐã lưu kết quả phân tích vào: {analyzed_file}")
        
        return final_df
        
    except ValueError:
        print("Vui lòng nhập số hợp lệ!")
        return None

def display_menu():
    """Hiển thị menu chọn chức năng"""
    print("\n" + "="*50)
    print(" PHẦN MỀM PHÂN TÍCH NẾN OHLC")
    print("="*50)
    print("1. Phân tích MỘT nến (nhập từ bàn phím)")
    print("2. Phân tích NHIỀU nến (nhập từ bàn phím)")
    print("3. Tạo và phân tích dữ liệu MẪU")
    print("4. Phân tích từ file CSV (candles.csv)")
    print("5. Thoát")
    print("="*50)
    
    try:
        choice = int(input("Chọn chức năng (1-5): "))
        return choice
    except ValueError:
        print(" Vui lòng nhập số từ 1 đến 5!")
        return 0

def main():
    """Hàm chính với menu tương tác"""
    while True:
        choice = display_menu()
        
        if choice == 1:
            print("\n" + "="*50)
            print(" PHÂN TÍCH MỘT NẾN")
            print("="*50)
            analyze_single_candle_interactive()
            
        elif choice == 2:
            print("\n" + "="*50)
            print(" PHÂN TÍCH NHIỀU NẾN")
            print("="*50)
            results = analyze_multiple_candles_interactive()
            
            if results is not None and not results.empty:
                print("\n" + "="*50)
                print(" KẾT QUẢ PHÂN TÍCH")
                print("="*50)
                
                # Hiển thị DataFrame đẹp hơn
                pd.set_option('display.max_columns', None)
                pd.set_option('display.width', None)
                pd.set_option('display.colheader_justify', 'center')
                
                print(results.to_string(index=False))
                
                # Thống kê
                print("\n" + "="*50)
                print(" THỐNG KÊ TỔNG HỢP")
                print("="*50)
                print(f"Tổng số nến: {len(results)}")
                print(f"Số nến tăng: {(results['Direction'] == 'Tăng').sum()}")
                print(f"Số nến giảm: {(results['Direction'] == 'Giảm').sum()}")
                print(f"Số nến Doji: {(results['Direction'] == 'Doji').sum()}")
                print(f"Số nến Doji (theo tiêu chuẩn): {results['Is_Doji'].value_counts().get('Có', 0)}")
                print(f"Số nến Hammer: {results['Is_Hammer'].value_counts().get('Có', 0)}")
                
        elif choice == 3:
            create_sample_data()
            
        elif choice == 4:
            print("\n" + "="*50)
            print(" PHÂN TÍCH TỪ FILE CSV")
            print("="*50)
            file_path = input("Nhập đường dẫn file CSV (mặc định: candles.csv): ").strip()
            if not file_path:
                file_path = "candles.csv"
            analyze_from_csv(file_path)
            
        elif choice == 5:
            print("\n" + "="*50)
            print(" Cảm ơn bạn đã sử dụng phần mềm!")
            print("="*50)
            break
        
        else:
            print(" Lựa chọn không hợp lệ! Vui lòng chọn từ 1 đến 5.")
        
        # Tạm dừng để người dùng xem kết quả
        input("\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()