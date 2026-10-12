
import platform
import psutil


def get_system_info():
    memory = psutil.virtual_memory()

    return {
        "os": platform.system(),
        "processor": platform.processor() or "Onbekend",
        "cores": psutil.cpu_count(logical=False) or 0,
        "threads": psutil.cpu_count(logical=True) or 0,
        "total_ram": round(memory.total / (1024 ** 3), 1),
    }


def get_live_stats():
    memory = psutil.virtual_memory()

    # Gebruik de Windows-systeemschijf
    disk = psutil.disk_usage("C:\\")

    return {
        "cpu": psutil.cpu_percent(interval=None),
        "ram": memory.percent,
        "ram_used": round(memory.used / (1024 ** 3), 1),
        "disk": disk.percent,
        "disk_free": round(disk.free / (1024 ** 3), 1),
    }


if __name__ == "__main__":
    print("CorePulse - System Information")
    print(get_system_info())
    print(get_live_stats())
