import psutil
import platform
import os

def can_handle(command):
    return any(keyword in command.lower() for keyword in ["detailed system info", "cpu temperature", "network status", "disk usage"])

def execute(command):
    try:
        if "detailed system info" in command.lower():
            info = f"OS: {platform.system()} {platform.release()} ({platform.version()})\n"
            info += f"Architecture: {platform.machine()}\n"
            info += f"Processor: {platform.processor()}\n"
            info += f"CPU Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical\n"
            info += f"Total RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB\n"
            return info
        elif "cpu temperature" in command.lower():
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if "coretemp" in temps:
                    core_temps = temps["coretemp"]
                    avg_temp = sum([t.current for t in core_temps]) / len(core_temps)
                    return f"Average CPU temperature: {avg_temp:.1f}°C"
                return "CPU temperature data available, but 'coretemp' not found."
            return "CPU temperature monitoring not supported on this system."
        elif "network status" in command.lower():
            net_io = psutil.net_io_counters()
            return f"Network: Sent {round(net_io.bytes_sent / (1024**2), 2)} MB, Received {round(net_io.bytes_recv / (1024**2), 2)} MB"
        elif "disk usage" in command.lower():
            disk = psutil.disk_usage('/')
            return f"Disk Usage: Total {round(disk.total / (1024**3), 2)} GB, Used {round(disk.used / (1024**3), 2)} GB ({disk.percent}%)"
        return "Advanced system info command not understood."
    except Exception as e:
        return f"Error getting advanced system info: {e}"

