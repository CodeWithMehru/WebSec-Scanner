import requests
import socket
import ssl

def scan_website(url):
    result = ""

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            result += "✔️ Website is reachable.\n"
        else:
            result += f"❌ Website returned status code: {response.status_code}\n"
    except Exception as e:
        result += f"❌ Error reaching website: {e}\n"

    try:
        domain = url.replace("https://", "").replace("http://", "").split('/')[0]
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080, 8443]
        open_ports = []
        
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)  
            result_code = sock.connect_ex((domain, port))
            if result_code == 0:
                open_ports.append(port)
            sock.close()

        if open_ports:
            result += f"🛡️ Open Ports: {', '.join(map(str, open_ports))}\n"
        else:
            result += "✅ No common open ports found.\n"
    except Exception as e:
        result += f"⚠️ Port scan failed: {e}\n"


    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                if cert:
                    result += f"🔒 SSL Certificate Issued To: {cert['subject'][0][0][1]}\n"
                    result += f"🔒 SSL Valid Until: {cert['notAfter']}\n"
                else:
                    result += "⚠️ No SSL certificate found.\n"
    except ssl.SSLError as e:
        result += f"⚠️ SSL Error: {e}\n"
    except Exception as e:
        result += f"⚠️ SSL Check failed: {e}\n"


    try:
        headers = response.headers
        result += "\n🔎 **Security Headers Check:**\n"
        missing_headers = []

        if 'X-Content-Type-Options' in headers:
            result += "✔️ X-Content-Type-Options: Present ✅\n"
        else:
            missing_headers.append('X-Content-Type-Options')

        if 'X-Frame-Options' in headers:
            result += "✔️ X-Frame-Options: Present ✅\n"
        else:
            missing_headers.append('X-Frame-Options')

        if 'Content-Security-Policy' in headers:
            result += "✔️ Content-Security-Policy: Present ✅\n"
        else:
            missing_headers.append('Content-Security-Policy')

        if 'Strict-Transport-Security' in headers:
            result += "✔️ Strict-Transport-Security: Present ✅\n"
        else:
            missing_headers.append('Strict-Transport-Security')

        if 'X-XSS-Protection' in headers:
            result += "✔️ X-XSS-Protection: Present ✅\n"
        else:
            missing_headers.append('X-XSS-Protection')

        if missing_headers:
            result += f"⚠️ Missing Headers: {', '.join(missing_headers)}\n"
    except Exception as e:
        result += f"⚠️ Header Check failed: {e}\n"

    return result
