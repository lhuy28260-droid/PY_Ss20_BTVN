import logging

logging.basicConfig(
    filename='fantasy_league.log',
    filemode='a',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    encoding='utf-8'
)

players = [
    {
        "player_id": "T101",
        "name": "Faker",
        "market_value": 5000,
        "fan_tokens": 1500,     
        "match_points": 0,      
        "form_multiplier": 1.0  
    },
    {
        "player_id": "GEN01",
        "name": "Chovy",
        "market_value": 4800,
        "fan_tokens": 800,
        "match_points": 500,
        "form_multiplier": 1.2
    },
    {
        "player_id": "DRX01",
        "name": "Deft",
        "market_value": 3000,
        "fan_tokens": 0,
        "match_points": 0,
        "form_multiplier": 0.8
    }
]


def display_market(player_list):
    """Chức năng 1: Xem Sàn Giao Dịch Tuyển Thủ"""
    logging.info("User viewed the player market.")
    
    if len(player_list) == 0:
        print("Sàn giao dịch hiện chưa có tuyển thủ nào.")
        return
        
    print("\n--- SÀN GIAO DỊCH TUYỂN THỦ ---")
    print(f"{'ID':<7} | {'Tên tuyển thủ':<15} | {'Giá trị thị trường':<18} | {'Fan Token':<10} | {'Điểm trận':<10} | {'Hệ số':<6} | Trạng thái đầu tư")
    print("-" * 105)
    
    for p in player_list:
        p_id = p.get("player_id", "T999")
        name = p.get("name", "Unknown")
        m_value = p.get("market_value", 0)
        f_tokens = p.get("fan_tokens", 0)
        m_points = p.get("match_points", 0)
        f_mult = p.get("form_multiplier", 1.0)
        
        if f_tokens == 0:
            inv_status = "Chưa có người đầu tư"
        elif 0 < f_tokens <= 1000:
            inv_status = "Đang thu hút"
        else:
            inv_status = "Tuyển thủ Hot"
            
        fmt_m_value = f"{m_value:,}"
        fmt_f_tokens = f"{f_tokens:,}"
        fmt_m_points = f"{m_points:,}"
        fmt_f_mult = f"{f_mult:.1f}"
        
        print(f"{p_id:<7} | {name:<15} | {fmt_m_value:<18} | {fmt_f_tokens:<10} | {fmt_m_points:<10} | {fmt_f_mult:<6} | {inv_status}")


def invest_tokens(player_list):
    """Chức năng 2: Đầu tư Fan Token"""
    print("\n--- ĐẦU TƯ FAN TOKEN ---")
    
    p_id = input("Nhập mã tuyển thủ: ").strip().upper()
    
    target_player = None
    for player in player_list:
        if player.get("player_id", "").upper() == p_id:
            target_player = player
            break
            
    if target_player is None:
        print("Không tìm thấy tuyển thủ!")
        logging.warning(f"Invest failed - Player {p_id} not found")
        return

    while True:
        try:
            raw_tokens = input("Nhập số token muốn đầu tư: ").strip()
            tokens_to_invest = int(raw_tokens)
            
            if tokens_to_invest <= 0:
                print("Số token phải là số nguyên dương. Vui lòng nhập lại.")
                logging.warning("Invalid token input while investing")
                continue
                
            break 
            
        except ValueError:
            print("Số token phải là số nguyên dương. Vui lòng nhập lại.")
            logging.warning("Invalid token input while investing")
            
    target_player["fan_tokens"] = target_player.get("fan_tokens", 0) + tokens_to_invest
    current_tokens = target_player["fan_tokens"]
    player_name = target_player.get("name", "Unknown")
    
    print(f"\nThành công: Đã đầu tư {tokens_to_invest:,} token vào tuyển thủ {p_id}.")
    print(f"Số Fan Token hiện tại của {player_name}: {current_tokens:,}")
    
    logging.info(f"Invested {tokens_to_invest} tokens into {p_id}")


def withdraw_tokens(player_list):
    """Chức năng 3: Rút vốn (Hoàn trả Token)"""
    print("--- RÚT VỐN FAN TOKEN ---")
    
    p_id = input("Nhập mã tuyển thủ: ").strip().upper()
    
    target_player = None
    for player in player_list:
        if player.get("player_id", "").upper() == p_id:
            target_player = player
            break
            
    if target_player is None:
        print("Không tìm thấy tuyển thủ!")
        logging.warning(f"Withdraw failed - Player {p_id} not found")
        return

    player_name = target_player.get("name", "Unknown")
    current_tokens = target_player.get("fan_tokens", 0)

    while True:
        try:
            raw_tokens = input("Nhập số token muốn rút: ").strip()
            tokens_to_withdraw = int(raw_tokens)
            
            if tokens_to_withdraw <= 0:
                print("Số token phải là số nguyên dương. Vui lòng nhập lại.")
                logging.warning("Invalid token input while withdrawing")
                continue
                
            break 
            
        except ValueError:
            print("Số token phải là số nguyên dương. Vui lòng nhập lại.")
            logging.warning("Invalid token input while withdrawing")

    if tokens_to_withdraw > current_tokens:
        print("Không thể rút. Số token muốn rút vượt quá số Fan Token hiện có.")
        print(f"Fan Token hiện có của {player_name}: {current_tokens:,}")
        logging.warning("Withdraw failed - Amount exceeds current fan tokens")
        return

    fee = tokens_to_withdraw * 0.10
    actual_received = tokens_to_withdraw - fee
    
    target_player["fan_tokens"] -= tokens_to_withdraw
    remaining_tokens = target_player["fan_tokens"]
    
    print(f"Thành công: Đã rút {tokens_to_withdraw:,} token khỏi tuyển thủ {p_id}.")
    print(f"Phí giao dịch 10%: {fee:,.1f} token")
    print(f"Số token thực nhận về ví: {actual_received:,.1f} token")
    print(f"Fan Token còn lại của {player_name}: {remaining_tokens:,}")
    
    logging.info(f"Withdrawn {tokens_to_withdraw} tokens from {p_id}. Actual received: {actual_received}")


def update_form_multiplier(player_list):
    """Chức năng 4: Biến động phong độ"""
    print("--- CẬP NHẬT HỆ SỐ PHONG ĐỘ ---")
    
    p_id = input("Nhập mã tuyển thủ: ").strip().upper()
    
    target_player = None
    for player in player_list:
        if player.get("player_id", "").upper() == p_id:
            target_player = player
            break
            
    if target_player is None:
        print("Không tìm thấy tuyển thủ!")
        logging.warning(f"Update form failed - Player {p_id} not found")
        return

    player_name = target_player.get("name", "Unknown")

    while True:
        try:
            raw_mult = input("Nhập hệ số phong độ mới (0.5 - 2.5): ").strip()
            new_multiplier = float(raw_mult)
            
            if not (0.5 <= new_multiplier <= 2.5):
                print("Hệ số phong độ chỉ được nằm trong khoảng 0.5 đến 2.5.")
                logging.warning("Update form failed - Multiplier out of bounds")
                continue
                
            break 
            
        except ValueError:
            print("Hệ số phong độ phải là số thực. Vui lòng nhập lại.")
            logging.warning("Update form failed - Invalid float input")
            
    target_player["form_multiplier"] = new_multiplier
    
    print(f"\nThành công: Đã cập nhật hệ số phong độ cho {player_name}.")
    print(f"Hệ số mới: x{new_multiplier:.1f}")
    
    logging.info(f"Updated form multiplier for {p_id} to {new_multiplier:.1f}")


def calculate_match_points(player_list):
    """Chức năng 5: Chấm điểm sau trận đấu"""
    print("--- CHẤM ĐIỂM SAU TRẬN ĐẤU ---")
    
    p_id = input("Nhập mã tuyển thủ: ").strip().upper()
    
    target_player = None
    for player in player_list:
        if player.get("player_id", "").upper() == p_id:
            target_player = player
            break
            
    if target_player is None:
        print("Không tìm thấy tuyển thủ!")
        logging.warning(f"Score match failed - Player {p_id} not found")
        return

    player_name = target_player.get("name", "Unknown")
    form_multiplier = target_player.get("form_multiplier", 1.0)

    while True:
        try:
            raw_base = input("Nhập điểm gốc của trận đấu: ").strip()
            base_points = float(raw_base)
            if base_points < 0:
                print("Điểm gốc không được âm. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("Điểm gốc phải là số. Vui lòng nhập lại.")
            
    actual_points = base_points * form_multiplier
    
    target_player["match_points"] = target_player.get("match_points", 0) + actual_points
    total_points = target_player["match_points"]
    
    
    print(f"\n>> Tuyển thủ {player_name} nhận được {actual_points:g} điểm (Hệ số x{form_multiplier}).")
    print(f"Tổng điểm: {total_points:g}")
    
    logging.info(f"Added {actual_points:.1f} match points to {p_id}")



def main():
    logging.info("Hệ thống Rikkei Esports Fantasy đã khởi động.")
    
    while True:
        print("===== HỆ THỐNG RIKKEI ESPORTS FANTASY =====")
        print("1. Xem Sàn Giao Dịch Tuyển Thủ")
        print("2. Đầu tư Fan Token")
        print("3. Rút vốn (Hoàn trả Token)")
        print("4. Biến động phong độ (Cập nhật hệ số)")
        print("5. Chấm điểm sau trận đấu")
        print("6. Thoát hệ thống")
        print("===========================================")
        
        choice = input("Chọn chức năng (1-6): ").strip()
        
        if choice == '1':
            display_market(players)
        elif choice == '2':
            invest_tokens(players)
        elif choice == '3':
            withdraw_tokens(players)
        elif choice == '4':
            update_form_multiplier(players)
        elif choice == '5':
            calculate_match_points(players)
        elif choice == '6':
            logging.info("Hệ thống đóng và thoát chương trình an toàn.")
            print("Đóng hệ thống Rikkei Esports Fantasy.")
            break  
        else:
            logging.warning("Invalid menu choice selected.")
            print("Lựa chọn không hợp lệ. Vui lòng nhập lại số từ 1-6!")

if __name__ == "__main__":
    main()