import logging

# ================================================================
# CẤU HÌNH HỆ THỐNG GHI NHẬT KÝ (LOGGING)
# ================================================================
logging.basicConfig(
    filename='tournament_app.log',
    filemode='a',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    encoding='utf-8'
)

# ================================================================
# THIẾT LẬP CẤU TRÚC DỮ LIỆU & MOCK DATA
# ================================================================
matches = [
    {
        "match_id": "M01",
        "team_a": "T1",
        "team_b": "GenG",
        "score_a": 2,
        "score_b": 1,
        "status": "Completed"
    },
    {
        "match_id": "M02",
        "team_a": "JDG",
        "team_b": "BLG",
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    }
]


def display_matches(match_list):
    """Chức năng 1: Hiển thị lịch thi đấu & Kết quả (Bổ sung bẫy KeyError)"""
    logging.info("User viewed the match list.")
    
    if len(match_list) == 0:
        print("Hiện chưa có trận đấu nào trong hệ thống.")
        return
        
    print("\n--- LỊCH THI ĐẤU & KẾT QUẢ ---")
    print(f"{'Mã trận':<8} | {'Đội A':<14} | {'Đội B':<14} | {'Tỷ số':<7} | Trạng thái")
    print("-" * 70)
    
    for match in match_list:
        m_id = match.get("match_id", "Unknown")
        team_a = match.get("team_a", "Unknown")
        team_b = match.get("team_b", "Unknown")
        status = match.get("status", "Unknown")
        
        # Bẫy 3: Sử dụng try...except KeyError để phòng hờ API trả thiếu dữ liệu điểm
        try:
            score_a = match["score_a"]
            score_b = match["score_b"]
            score = f"{score_a}-{score_b}"
        except KeyError:
            score = "N/A"
            logging.error(f"Missing score keys in match {m_id} from database.")
            
        print(f"{m_id:<8} | {team_a:<14} | {team_b:<14} | {score:<7} | {status}")


def add_match(match_list):
    """Chức năng 2: Thêm trận đấu mới"""
    print(" --- THÊM TRẬN ĐẤU MỚI --- ")
    
    m_id = input("Nhập mã trận đấu: ").strip()
    if not m_id:
        print("Mã trận đấu không được để trống.")
        logging.warning("User tried to add a match with empty match ID.")
        return
        
    for match in match_list:
        if match.get("match_id") == m_id:
            print(f"Lỗi: Mã trận đấu {m_id} đã tồn tại.")
            logging.warning(f"Match ID {m_id} already exists.")
            return
            
    team_a = input("Nhập tên Đội A: ").strip()
    team_b = input("Nhập tên Đội B: ").strip()
    
    if not team_a or not team_b:
        print("Tên đội không được để trống.")
        logging.warning("User tried to add a match with empty team name.")
        return
    
    new_match = {
        "match_id": m_id,
        "team_a": team_a,
        "team_b": team_b,
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    }
    
    match_list.append(new_match)
    print(f"\nThành công: Đã thêm trận đấu {m_id}.")
    logging.info(f"Match {m_id} added successfully")


def update_score(match_list):
    """Chức năng 3: Cập nhật tỷ số trận đấu"""
    print("\n--- CẬP NHẬT TỶ SỐ TRẬN ĐẤU ---")
    m_id = input("Nhập mã trận đấu cần cập nhật: ").strip()
    
    target_match = None
    for match in match_list:
        if match.get("match_id") == m_id:
            target_match = match
            break
            
    if target_match is None:
        print(f"\nKhông tìm thấy trận đấu mang mã {m_id}.")
        logging.warning(f"User tried to update non-existing match {m_id}")
        return

    team_a = target_match.get("team_a", "Team A")
    team_b = target_match.get("team_b", "Team B")
    status = target_match.get("status", "Unknown")
    print(f"\nTrận đấu: {team_a} vs {team_b} ({status})")
    
    # Bẫy lỗi ValueError cho dữ liệu nhập vào
    while True:
        try:
            raw_input_a = input(f"Nhập điểm Đội {team_a}: ").strip()
            score_a = int(raw_input_a)
            if score_a < 0:
                print("\nĐiểm số phải lớn hơn hoặc bằng 0.")
                logging.error(f"Negative score input detected: {score_a}")
                continue
            break
        except ValueError as e:
            print("Điểm số phải là số nguyên. Vui lòng nhập lại.")
            logging.error(f"Invalid score input. Error: {e}")

    while True:
        try:
            raw_input_b = input(f"Nhập điểm Đội {team_b}: ").strip()
            score_b = int(raw_input_b)
            if score_b < 0:
                print("Điểm số phải lớn hơn hoặc bằng 0.")
                logging.error(f"Negative score input detected: {score_b}")
                continue
            break
        except ValueError as e:
            print("\nĐiểm số phải là số nguyên. Vui lòng nhập lại.")
            logging.error(f"Invalid score input. Error: {e}")
            
    target_match["score_a"] = score_a
    target_match["score_b"] = score_b
    
    # Bẫy 1 - Lỗi Logic Ẩn: Chỉ gán "Completed" khi ít nhất 1 đội có điểm, hoặc trọng tài xác nhận 0-0
    if score_a == 0 and score_b == 0:
        confirm = input("\nTỷ số đang là 0-0. Trọng tài có xác nhận trận đã hoàn thành không? (y/n): ").strip().lower()
        if confirm == 'y':
            target_match["status"] = "Completed"
        else:
            target_match["status"] = "Pending"
    else:
        target_match["status"] = "Completed"
    
    print(f"\nThành công: Đã cập nhật tỷ số trận đấu {m_id}.")
    logging.info(f"Match {m_id} score updated successfully. Status: {target_match['status']}")


# --- Helper Function cho Chức năng 4 ---
def determine_winner(match):
    """Hàm phụ trợ xác định đội chiến thắng hoặc kết quả hòa (Bổ sung bẫy KeyError)"""
    if match.get("status") == "Pending":
        return "Not Started"
        
    try:
        score_a = match["score_a"]
        score_b = match["score_b"]
    except KeyError:
        return "Data Error"
    
    if score_a > score_b:
        return match.get("team_a", "Team A")
    elif score_b > score_a:
        return match.get("team_b", "Team B")
    else:
        return "Draw"


def generate_report(match_list):
    """Chức năng 4: Báo cáo thống kê giải đấu (Bổ sung bẫy KeyError)"""
    print("\n--- BÁO CÁO THỐNG KÊ GIẢI ĐẤU ---")
    
    completed_count = 0
    
    for match in match_list:
        if match.get("status") == "Completed":
            winner = determine_winner(match)
            m_id = match.get("match_id", "Unknown")
            team_a = match.get("team_a", "Team A")
            team_b = match.get("team_b", "Team B")
            
            try:
                score_a = match["score_a"]
                score_b = match["score_b"]
            except KeyError:
                score_a, score_b = "?", "?"
                
            print(f"{m_id}: {team_a} {score_a}-{score_b} {team_b} | Kết quả: {winner}")
            completed_count += 1
            
    if completed_count == 0:
        print("Chưa có trận đấu nào hoàn thành.")
        
    print(f"Tổng số trận đã hoàn thành: {completed_count}")
    logging.info("User generated tournament report.")


# ================================================================
# HÀM ĐIỀU HÀNH CHÍNH (MAIN FUNCTION)
# ================================================================
def main():
    logging.info("Hệ thống Rikkei Esports đã khởi động an toàn.")
    
    while True:
        print("\n===== HỆ THỐNG QUẢN LÝ GIẢI ĐẤU RIKKEI ESPORTS =====")
        print("1. Hiển thị lịch thi đấu & Kết quả")
        print("2. Thêm trận đấu mới")
        print("3. Cập nhật tỷ số trận đấu")
        print("4. Báo cáo thống kê")
        print("5. Thoát chương trình")
        print("====================================================")
        
        choice = input("Chọn chức năng (1-5): ").strip()
        
        if choice == '1':
            display_matches(matches)
        elif choice == '2':
            add_match(matches)
        elif choice == '3':
            update_score(matches)
        elif choice == '4':
            generate_report(matches)
        elif choice == '5':
            logging.info("Hệ thống đóng và thoát chương trình. Tạm biệt!")
            print("Đã thoát chương trình an toàn. Hẹn gặp lại!")
            break  
        else:
            # Bẫy 2: Nhập sai lựa chọn menu (Log chuẩn xác theo yêu cầu)
            logging.warning("Invalid menu choice selected")
            print("Lựa chọn không hợp lệ. Vui lòng nhập lại số từ 1-5!")


if __name__ == "__main__":
    main()