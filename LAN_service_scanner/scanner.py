import socket
import threading
import queue
import time
import tkinter as tk
from tkinter import ttk, messagebox

SSDP_ADDR = ("239.255.255.250", 1900)
MSEARCH = (
    "M-SEARCH * HTTP/1.1\r\n"
    "HOST: 239.255.255.250:1900\r\n"
    "MAN: \"ssdp:discover\"\r\n"
    "MX: 2\r\n"
    "ST: ssdp:all\r\n"
    "\r\n"
).encode("ascii")

def get_default_iface_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"

def parse_ssdp_response(data: bytes, addr):
    try:
        text = data.decode("utf-8", errors="replace")
        lines = text.split("\r\n")
        if not lines or "HTTP/1.1 200 OK" not in (lines[0] or ""):
            return None
        headers = {}
        for line in lines[1:]:
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip().upper()] = v.strip()
        return {
            "ip": addr[0],
            "st": headers.get("ST", ""),
            "usn": headers.get("USN", ""),
            "server": headers.get("SERVER", ""),
            "location": headers.get("LOCATION", ""),
        }
    except Exception:
        return None

def ssdp_discover(timeout=4.0, iface_ip="0.0.0.0", stop_event=None, result_q=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        try:
            if iface_ip and iface_ip != "0.0.0.0":
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(iface_ip))
        except OSError:
            pass

        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.settimeout(0.5)

        try:
            if iface_ip and iface_ip != "0.0.0.0":
                sock.bind((iface_ip, 0))
            else:
                sock.bind(("", 0))
        except OSError:
            pass

        for _ in range(3):
            try:
                sock.sendto(MSEARCH, SSDP_ADDR)
            except OSError:
                break
            time.sleep(0.1)

        seen = set()
        t_end = time.time() + timeout
        while time.time() < t_end and (stop_event is None or not stop_event.is_set()):
            try:
                data, addr = sock.recvfrom(65535)
            except socket.timeout:
                continue
            except OSError:
                break
            parsed = parse_ssdp_response(data, addr)
            if parsed:
                key = (parsed["ip"], parsed["usn"], parsed["st"])
                if key not in seen:
                    seen.add(key)
                    if result_q:
                        result_q.put(parsed)

        if result_q:
            result_q.put({"__done__": True})
    finally:
        sock.close()

class SSDPScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SSDP/UPnP Network Scanner")
        self.stop_event = threading.Event()
        self.result_q = queue.Queue()
        self.rows_count = 0

        frm = ttk.Frame(root, padding=10)
        frm.pack(fill="both", expand=True)

        controls = ttk.Frame(frm)
        controls.pack(fill="x")

        ttk.Label(controls, text="Timeout (s):").pack(side="left")
        self.timeout_var = tk.StringVar(value="5")
        ttk.Entry(controls, width=5, textvariable=self.timeout_var).pack(side="left", padx=(4, 12))

        ttk.Button(controls, text="Scan", command=self.start_scan).pack(side="left")
        ttk.Button(controls, text="Stop", command=self.stop_scan).pack(side="left", padx=(6, 0))

        self.iface_ip = get_default_iface_ip()
        ttk.Label(controls, text=f"Interface: {self.iface_ip}").pack(side="left", padx=(12, 0))

        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(frm, textvariable=self.status_var).pack(anchor="w", pady=(6, 4))

        cols = ("ip", "st", "usn", "server", "location")
        self.tree = ttk.Treeview(frm, columns=cols, show="headings", height=14)
        headings = {
            "ip": "IP",
            "st": "Service Type (ST)",
            "usn": "USN",
            "server": "Server",
            "location": "Location",
        }
        for c in cols:
            self.tree.heading(c, text=headings[c])
            self.tree.column(c, width=140 if c in ("ip",) else 260, anchor="w")
        self.tree.pack(fill="both", expand=True)

        self.root.after(100, self._drain_results)

    def start_scan(self):
        if hasattr(self, "scan_thread") and self.scan_thread.is_alive():
            messagebox.showinfo("Scan running", "A scan is already in progress.")
            return
        self.tree.delete(*self.tree.get_children())
        self.rows_count = 0
        self.stop_event.clear()
        try:
            timeout = float(self.timeout_var.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Timeout must be a number.")
            return
        self.status_var.set(f"Scanning via SSDP… timeout {timeout:.1f}s")
        self.scan_thread = threading.Thread(
            target=ssdp_discover,
            args=(timeout, self.iface_ip, self.stop_event, self.result_q),
            daemon=True,
        )
        self.scan_thread.start()

    def stop_scan(self):
        self.stop_event.set()
        self.status_var.set("Stopping scan…")

    def _drain_results(self):
        drained = 0
        done_signal = False
        try:
            while True:
                item = self.result_q.get_nowait()
                if "__done__" in item:
                    done_signal = True
                    continue
                drained += 1
                self.rows_count += 1
                self.tree.insert("", "end",
                                 values=(item["ip"], item["st"], item["usn"], item["server"], item["location"]))
        except queue.Empty:
            pass

        if hasattr(self, "scan_thread") and self.scan_thread.is_alive():
            self.status_var.set(f"Receiving responses… ({drained} new)")
        else:
            if done_signal or not (hasattr(self, "scan_thread") and self.scan_thread.is_alive()):
                if self.rows_count == 0:
                    self.status_var.set("Scan complete — no devices responded (UPnP may be disabled or blocked).")
                else:
                    self.status_var.set("Scan complete.")

        self.root.after(150, self._drain_results)

def main():
    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 1.2)
    except Exception:
        pass
    app = SSDPScannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
