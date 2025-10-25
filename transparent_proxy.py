"""
Transparent Proxy - Automatically routes ALL traffic through IPRoyal proxy
No browser configuration needed!
"""
import subprocess
import sys
import os
import time
import requests
from threading import Thread

# IPRoyal residential proxy configuration
PROXY_HOST = "geo.iproyal.com"
PROXY_PORT = 12321
PROXY_USER = "TmwjTsVQHgTiXElI"
PROXY_PASS = "Topproducer2026_country-us_city-lasvegas_session-QNpU9Vlz_lifetime-168h"

def check_admin():
    """Check if running as administrator"""
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()

def setup_system_proxy():
    """Configure Windows system proxy automatically"""
    try:
        import winreg
        
        # Registry path for proxy settings
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE) as key:
            # Enable proxy
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
            # Set proxy server
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, "127.0.0.1:8888")
            # Set proxy override (bypass for local addresses)
            winreg.SetValueEx(key, "ProxyOverride", 0, winreg.REG_SZ, "localhost;127.*;10.*;172.16.*;172.17.*;172.18.*;172.19.*;172.20.*;172.21.*;172.22.*;172.23.*;172.24.*;172.25.*;172.26.*;172.27.*;172.28.*;172.29.*;172.30.*;172.31.*;192.168.*")
            
        print("✅ System proxy configured automatically!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to configure system proxy: {e}")
        return False

def restore_system_proxy():
    """Restore original proxy settings"""
    try:
        import winreg
        
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE) as key:
            # Disable proxy
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
            
        print("✅ System proxy restored!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to restore system proxy: {e}")
        return False

def start_local_proxy():
    """Start the local proxy server"""
    from proxy_server import start_proxy_server
    start_proxy_server()

def test_proxy_connection():
    """Test if proxy is working"""
    try:
        # Test without proxy (should show real IP)
        response_real = requests.get('https://ipv4.icanhazip.com', timeout=10)
        real_ip = response_real.text.strip()
        
        # Test with proxy (should show proxy IP)
        proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
        proxies = {'http': proxy_url, 'https': proxy_url}
        
        response_proxy = requests.get('https://ipv4.icanhazip.com', proxies=proxies, timeout=10)
        proxy_ip = response_proxy.text.strip()
        
        print(f"🌐 Real IP: {real_ip}")
        print(f"🔒 Proxy IP: {proxy_ip}")
        
        if real_ip != proxy_ip:
            print("✅ Proxy is working! Your IP is hidden!")
            return True
        else:
            print("❌ Proxy not working - IPs are the same")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main function"""
    print("="*60)
    print("🚀 TRANSPARENT PROXY - NO BROWSER CONFIG NEEDED!")
    print("="*60)
    
    # Check if running as admin
    if not check_admin():
        print("⚠️  WARNING: Not running as administrator")
        print("   Some features may not work properly")
        print("   Right-click and 'Run as administrator' for full functionality")
        print()
    
    # Test proxy connection first
    print("🧪 Testing IPRoyal proxy connection...")
    if not test_proxy_connection():
        print("❌ Cannot connect to IPRoyal proxy. Check your credentials.")
        return
    
    print("\n🔧 Configuring system proxy automatically...")
    if not setup_system_proxy():
        print("❌ Failed to configure system proxy automatically")
        print("   You may need to configure your browser manually:")
        print("   HTTP Proxy: 127.0.0.1:8888")
        print("   HTTPS Proxy: 127.0.0.1:8888")
        return
    
    print("\n🚀 Starting local proxy server...")
    print("   This will route ALL your traffic through IPRoyal!")
    print("   Press Ctrl+C to stop and restore original settings")
    print("="*60)
    
    try:
        # Start the proxy server
        start_local_proxy()
    except KeyboardInterrupt:
        print("\n🛑 Stopping proxy...")
        print("🔧 Restoring original proxy settings...")
        restore_system_proxy()
        print("✅ Done! Your original settings have been restored.")

if __name__ == "__main__":
    main()
