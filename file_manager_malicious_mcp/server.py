from mcp.server.fastmcp import FastMCP
import socket

mcp = FastMCP("MyScanner")

@mcp.tool()
def active_scan_lan(target_ip: str) -> str:
    """
    Quét mạng LAN bằng giao thức ARP để tìm các thiết bị đang hoạt động.
    Yêu cầu truyền vào dải IP, ví dụ: '192.168.1.0/24'.
    Trả về danh sách IP và địa chỉ MAC của các thiết bị tìm thấy.
    """
    try:
        # 1. Ép Scapy câm mồm, không in cảnh báo rác làm hỏng chuẩn JSON
        import logging
        logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
        
        # 2. Dời toàn bộ import scapy vào TRONG hàm (Lazy Import)
        from scapy.all import Ether, ARP, srp, conf, IFACES
        
        # Ép dùng card mạng số 14
        conf.iface = IFACES.dev_from_index(14)

        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip)
        answered, _ = srp(packet, timeout=2, verbose=False)
        
        if not answered:
            return f"Không tìm thấy thiết bị nào phản hồi trong dải IP: {target_ip}"
            
        result = [f"Kết quả quét ARP cho {target_ip}:"]
        for sent, received in answered:
            result.append(f" - IP: {received.psrc} | MAC: {received.hwsrc}")
            
        return "\n".join(result)
        
    except Exception as e:
        return f"Lỗi khi thực thi quét ARP: {str(e)}"

@mcp.tool()
def get_my_ip_range() -> str:
    """
    Tự động lấy dải IP mạng LAN hiện tại của máy tính để phục vụ việc quét mạng.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        ip_parts = local_ip.split('.')
        network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        return f"IP hiện tại của máy: {local_ip} | Dải mạng LAN (Target IP): {network_range}"
    except Exception as e:
        return f"Lỗi không thể tự động lấy IP: {str(e)}"

if __name__ == "__main__":
    mcp.run()
    


  #  $env:SNYK_TOKEN="cái_mã_token_của_mày_dán_vào_đây"