import logging

logging.basicConfig(
    filename='arena_tickets.log',
    filemode='a',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    encoding='utf-8'
)

ticket_db = [
    {"ticket_id": "T01", "buyer_name": "Nguyen Van A", "price": 500.0, "status": "Booked", "seat": ("A", 1)},
    {"ticket_id": "T02", "buyer_name": "Tran Thi B", "price": 300.0, "status": "Cancelled", "seat": ("B", 5)},
    {"ticket_id": "T03", "buyer_name": "Le Van C", "price": 500.0, "status": "Booked", "seat": ("A", 2)}
]

def display_tickets(ticket_list):
    """Chức năng 1: Xem danh sách vé đã bán"""
    logging.info("User viewed ticket list.")
    
    if len(ticket_list) == 0:
        print("Hiện chưa có vé nào trong hệ thống.")
        return
        
    print(f"{'Mã Vé':<7} | {'Tên Khách Hàng':<16} | {'Giá Vé':<8} | {'Chỗ Ngồi':<10} | Trạng Thái")
    print("-" * 75)
    
    for ticket in ticket_list:
        try:
            t_id = ticket["ticket_id"]
            name = ticket["buyer_name"]
            price = ticket["price"]
            seat = ticket["seat"]  
            status = ticket["status"]
            
            seat_str = f"{seat[0]}-{seat[1]}"
            display_status = f"{status} [ĐÃ HỦY]" if status == "Cancelled" else status
            
            print(f"{t_id:<7} | {name:<16} | {price:<8.1f} | {seat_str:<10} | {display_status}")
            
        except KeyError as e:
            print("Lỗi: Một vé đang bị thiếu dữ liệu, vui lòng kiểm tra lại.")
            logging.error(f"Missing key while displaying ticket: {e}")
            
    print("-" * 75)


def book_ticket(ticket_list):
    """Chức năng 2: Đặt vé mới"""
    
    t_id = input("Nhập mã vé: ").strip().upper()
    
    for ticket in ticket_list:
        if ticket.get("ticket_id", "").upper() == t_id:
            print(f"Lỗi: Mã vé {t_id} đã tồn tại.")
            logging.warning(f"Duplicate ticket ID entered: {t_id}")
            return
            
    name = input("Nhập tên khách hàng: ").strip().title()
    
    while True:
        try:
            raw_price = input("Nhập giá vé: ").strip()
            price = float(raw_price)
            if price <= 0:
                print("Giá vé phải lớn hơn 0. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("Giá vé phải là số. Vui lòng nhập lại.")
            logging.warning("Invalid price input while booking ticket")
            
    zone = input("Nhập khu vực ghế: ").strip().upper()
    
    while True:
        try:
            raw_seat = input("Nhập số ghế: ").strip()
            seat_number = int(raw_seat)
            if seat_number <= 0:
                print("Số ghế phải lớn hơn 0. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("Số ghế phải là số nguyên. Vui lòng nhập lại.")
            logging.warning("Invalid seat number input while booking ticket")
            
    new_ticket = {
        "ticket_id": t_id,
        "buyer_name": name,
        "price": price,
        "status": "Booked",
        "seat": (zone, seat_number) 
    }
    
    ticket_list.append(new_ticket)
    print(f"\nThành công: Đã đặt vé {t_id} cho khách hàng {name}.")
    logging.info(f"Booked new ticket {t_id} for {name}")


def change_seat(ticket_list):
    """Chức năng 3: Đổi chỗ ngồi (Cập nhật vé bằng Tuple mới)"""
    
    t_id = input("Nhập mã vé cần đổi chỗ: ").strip().upper()
    
    target_ticket = None
    for ticket in ticket_list:
        if ticket.get("ticket_id", "").upper() == t_id:
            target_ticket = ticket
            break
            
    if target_ticket is None:
        print(f"Không tìm thấy vé mang mã {t_id}.")
        logging.warning(f"Change seat failed - Ticket {t_id} not found")
        return
        
    new_zone = input("Nhập khu vực ghế mới: ").strip().upper()
    
    while True:
        try:
            raw_seat = input("Nhập số ghế mới: ").strip()
            new_seat_number = int(raw_seat)
            if new_seat_number <= 0:
                print("Số ghế phải lớn hơn 0. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("Số ghế phải là số nguyên. Vui lòng nhập lại.")
            
    target_ticket["seat"] = (new_zone, new_seat_number)
    
    seat_str = f"{new_zone}-{new_seat_number}"
    print(f"\nThành công: Đã đổi chỗ vé {t_id} sang {seat_str}.")
    logging.info(f"Seat changed for ticket {t_id} to {seat_str}")


def cancel_ticket(ticket_list):
    """Chức năng 4: Hủy vé (Xóa mềm - Soft Delete)"""
    
    t_id = input("Nhập mã vé cần hủy: ").strip().upper()
    
    target_ticket = None
    for ticket in ticket_list:
        if ticket.get("ticket_id", "").upper() == t_id:
            target_ticket = ticket
            break
            
    if target_ticket is None:
        print(f"Không tìm thấy vé mang mã {t_id}.")
        logging.warning(f"Cancel ticket failed - Ticket {t_id} not found")
        return
        
    if target_ticket.get("status") == "Cancelled":
        print(f"Vé {t_id} đã ở trạng thái Cancelled trước đó.")
        return
        
    target_ticket["status"] = "Cancelled"
    
    print(f"\nThành công: Vé {t_id} đã được hủy.")
    logging.warning(f"Ticket {t_id} has been cancelled.")


def generate_revenue_report(ticket_list):
    """Chức năng 5: Báo cáo doanh thu (Xử lý logic kế toán và bắt lỗi KeyError)"""
    print("\n--- BÁO CÁO DOANH THU ---")
    
    booked_count = 0
    cancelled_count = 0
    total_revenue = 0.0
    
    for ticket in ticket_list:
        try:
            status = ticket["status"]
            if status == "Booked":
                booked_count += 1
                total_revenue += ticket["price"]
            elif status == "Cancelled":
                cancelled_count += 1
                
        except KeyError as e:
            print("Lỗi: Một vé đang bị thiếu dữ liệu doanh thu.")
            logging.error(f"Missing key while calculating revenue: {e}")
            
    print(f"Tổng số vé đã đặt: {booked_count}")
    print(f"Tổng số vé đã hủy: {cancelled_count}")
    print(f"Tổng doanh thu hợp lệ: {total_revenue:.1f}")
    
    logging.info(f"Revenue report generated. Total: {total_revenue:.1f}")



def main():
    logging.info("Hệ thống Quản lý Vé Rikkei Esports đã khởi động.")
    
    while True:
        print("\n=== HỆ THỐNG QUẢN LÝ VÉ RIKKEI ESPORTS ===")
        print("1. Xem danh sách vé đã bán")
        print("2. Đặt vé mới")
        print("3. Đổi chỗ ngồi (Cập nhật vé)")
        print("4. Hủy vé")
        print("5. Báo cáo doanh thu")
        print("6. Thoát chương trình")
        print("==========================================")
        
        choice = input("Chọn chức năng (1-6): ").strip()
        
        if choice == '1':
            display_tickets(ticket_db)
        elif choice == '2':
            book_ticket(ticket_db)
        elif choice == '3':
            change_seat(ticket_db)
        elif choice == '4':
            cancel_ticket(ticket_db)
        elif choice == '5':
            generate_revenue_report(ticket_db)
        elif choice == '6':
            print("Cảm ơn bạn đã sử dụng hệ thống quản lý vé Rikkei Esports.")
            logging.info("Ticket management system closed.")
            break  
        else:
            logging.warning("Invalid menu choice selected.")
            print("Lựa chọn không hợp lệ. Vui lòng nhập lại số từ 1-6!")

if __name__ == "__main__":
    main()