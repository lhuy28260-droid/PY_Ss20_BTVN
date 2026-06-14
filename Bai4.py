import logging

logging.basicConfig(
    filename='roster_app.log',
    filemode='a',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    encoding='utf-8'
)

roster = [
    {
        "player_id": "P01",
        "name": "Faker",
        "role": "Mid Lane",
        "salary": 5000.0,
        "status": "Active"
    },
    {
        "player_id": "P02",
        "name": "Oner",
        "role": "Jungle",
        "salary": 3500.0,
        "status": "Active"
    },
    {
        "player_id": "P03",
        "name": "Ruler",
        "role": "ADC",
        "salary": 6000.0,
        "status": "Benched" 
    }
]

def display_roster(roster_list):
    """Chức năng 1: Xem đội hình thi đấu hiện tại (Có bẫy KeyError cho trạng thái)"""
    logging.info("Coach viewed the team roster.")
    
    if len(roster_list) == 0:
        print("Đội hình hiện đang trống.")
        return
        
    print("\n--- ĐỘI HÌNH RIKKEI ESPORTS ---")
    print(f"{'ID':<7} | {'Tên tuyển thủ':<18} | {'Vị trí':<12} | {'Lương':<10} | Trạng thái")
    print("-" * 75)
    
    for player in roster_list:
        p_id = player.get("player_id", "Unknown")
        name = player.get("name", "Unknown")
        role = player.get("role", "Unknown")
        salary = player.get("salary", 0.0)
        
        try:
            status = player["status"]
        except KeyError:
            status = "Unknown"
            logging.error(f"Missing 'status' key for player ID {p_id}")
        
        display_name = f"{name} [DỰ BỊ]" if status == "Benched" else name
        formatted_salary = f"{salary:,.1f}"
        
        print(f"{p_id:<7} | {display_name:<18} | {role:<12} | {formatted_salary:<10} | {status}")


def sign_player(roster_list):
    """Chức năng 2: Chiêu mộ tuyển thủ mới""" 
    # Bẫy 3: Tự động .strip().upper() loại bỏ mã rác
    p_id = input("Nhập mã tuyển thủ: ").strip().upper()
    
    if not p_id:
        print("Mã tuyển thủ không được để trống.")
        return
        
    for player in roster_list:
        if player.get("player_id", "").upper() == p_id:
            print(f"Mã tuyển thủ {p_id} đã tồn tại.")
            logging.warning(f"Failed to sign player - Duplicate player ID {p_id}")
            return
            
    name = input("Nhập tên tuyển thủ: ").strip().title()
    role = input("Nhập vị trí thi đấu: ").strip()
    
    while True:
        try:
            raw_salary = input("Nhập mức lương hàng tháng: ").strip()
            salary = float(raw_salary)
            if salary <= 0:
                print("Lương phải là số dương. Vui lòng nhập lại.")
                logging.warning("Failed to sign player - Invalid salary input")
                continue 
            break 
        except ValueError:
            print("Lương phải là số. Vui lòng nhập lại.")
            logging.warning("Failed to sign player - Invalid salary input")
    
    new_player = {
        "player_id": p_id,
        "name": name,
        "role": role,
        "salary": salary,
        "status": "Active"
    }
    
    roster_list.append(new_player)
    print(f"Thành công: Đã chiêu mộ tuyển thủ {name}.")
    logging.info(f"Signed new player {name} with salary {salary}")


def update_player_status(roster_list):
    """Chức năng 3: Cập nhật lương & Trạng thái thi đấu"""
    # Bẫy 3: Tự động .strip().upper() loại bỏ mã rác
    p_id = input("Nhập mã tuyển thủ cần cập nhật: ").strip().upper()
    
    target_player = None
    for player in roster_list:
        if player.get("player_id", "").upper() == p_id:
            target_player = player
            break
            
    if target_player is None:
        print(f"Không tìm thấy tuyển thủ mang mã {p_id}.")
        logging.warning(f"Failed to update player - Player ID {p_id} not found")
        return

    name = target_player.get("name", "Unknown")
    role = target_player.get("role", "Unknown")
    salary = target_player.get("salary", 0.0)
    status = target_player.get("status", "Unknown")
    
    print(f"Tuyển thủ: {name}")
    print(f"Vị trí: {role}")
    print(f"Lương hiện tại: {salary:,.1f}")
    print(f"Trạng thái hiện tại: {status}")
    
    print("Bạn muốn cập nhật:")
    print("1. Cập nhật lương")
    print("2. Cập nhật trạng thái thi đấu")
    
    sub_choice = input("Chọn chức năng cập nhật (1-2): ").strip()
    
    if sub_choice == '1':
        while True:
            try:
                raw_new_salary = input("Nhập mức lương mới: ").strip()
                new_salary = float(raw_new_salary)
                if new_salary <= 0:
                    print("Lương phải là số dương. Vui lòng nhập lại.")
                    continue
                break
            except ValueError:
                print("Lương phải là số. Vui lòng nhập lại.")
                
        old_salary = target_player["salary"]
        target_player["salary"] = new_salary
        
        print(f"Thành công: Đã cập nhật lương cho tuyển thủ {p_id}.")
        logging.info(f"Updated player {p_id} salary from {old_salary} to {new_salary}")
        
    elif sub_choice == '2':
        print("Chọn trạng thái mới: ")
        print("1. Active")
        print("2. Benched")
        status_choice = input("Nhập lựa chọn trạng thái (1-2): ").strip()
        
        if status_choice == '1':
            new_status = "Active"
        elif status_choice == '2':
            new_status = "Benched"
        else:
            print("Lựa chọn không hợp lệ. Hủy thao tác cập nhật.")
            return
            
        old_status = target_player["status"]
        target_player["status"] = new_status
        
        print(f"Thành công: Đã cập nhật trạng thái cho tuyển thủ {p_id}.")
        logging.info(f"Updated player {p_id} status from {old_status} to {new_status}")
        
    else:
        print("Lựa chọn không hợp lệ. Hủy thao tác cập nhật.")


def generate_payroll_report(roster_list):
    """Chức năng 4: Báo cáo quỹ lương hàng tháng"""
    print("--- BÁO CÁO QUỸ LƯƠNG HÀNG THÁNG ---")
    
    if len(roster_list) == 0:
        print("Đội hình hiện đang trống. Tổng quỹ lương: 0.0")
        return
        
    print(f"{'ID':<7} | {'Tên tuyển thủ':<18} | {'Trạng thái':<10} | {'Lương gốc':<11} | Lương thực nhận")
    print("-" * 75)
    
    total_payroll = 0.0
    
    for player in roster_list:
        try:
            p_id = player["player_id"]
            name = player["name"]
            status = player["status"]
            base_salary = player["salary"]
            
            # Bẫy 2: Lỗi Logic Ẩn - Đảm bảo nhân sự dự bị chỉ nhận 50% lương
            if status == "Benched":
                actual_salary = base_salary * 0.5
            else:
                actual_salary = base_salary
                
            total_payroll += actual_salary
            
            formatted_base = f"{base_salary:,.1f}"
            formatted_actual = f"{actual_salary:,.1f}"
            
            print(f"{p_id:<7} | {name:<18} | {status:<10} | {formatted_base:<11} | {formatted_actual}")
            
        except KeyError as e:
            print("Lỗi: Một tuyển thủ đang bị thiếu dữ liệu.")
            logging.error(f"Missing key while generating payroll report: {e}")
            
    print("-" * 75)
    print(f"Tổng quỹ lương hàng tháng: {total_payroll:,.1f}")
    
    logging.info(f"Generated monthly payroll report. Total: {total_payroll:,.1f}")

def main():
    logging.info("Hệ thống Quản lý Đội hình Rikkei Esports đã khởi động.")
    
    while True:
        print("===== HỆ THỐNG QUẢN LÝ ĐỘI HÌNH RIKKEI ESPORTS =====")
        print("1. Xem đội hình thi đấu hiện tại")
        print("2. Chiêu mộ tuyển thủ mới")
        print("3. Cập nhật lương & Trạng thái thi đấu")
        print("4. Báo cáo quỹ lương hàng tháng")
        print("5. Thoát hệ thống")
        print("====================================================")
        
        choice = input("Chọn chức năng (1-5): ").strip()
        
        if choice == '1':
            display_roster(roster)
        elif choice == '2':
            sign_player(roster)
        elif choice == '3':
            update_player_status(roster)
        elif choice == '4':
            generate_payroll_report(roster)
        elif choice == '5':
            logging.info("Hệ thống đóng và thoát chương trình an toàn.")
            print("Đã thoát chương trình. Tạm biệt!")
            break  
        else:
            logging.warning("Invalid menu choice selected.")
            print("Lựa chọn không hợp lệ. Vui lòng nhập lại số từ 1-5!")


if __name__ == "__main__":
    main()