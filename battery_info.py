import psutil
import wmi


def get_battery_health():
    # Get current battery status
    battery = psutil.sensors_battery()
    if not battery:
        return "No battery detected."

    # Connect to WMI for design and full charge capacity
    w = wmi.WMI(namespace="root\\WMI")
    battery_info = w.query("SELECT * FROM BatteryFullChargedCapacity")
    design_info = w.query("SELECT * FROM BatteryStaticData")

    if not battery_info or not design_info:
        return "Battery details not available."

    full_charge_capacity = battery_info[0].FullChargedCapacity
    design_capacity = design_info[0].DesignedCapacity

    health = (full_charge_capacity / design_capacity) * 100

    return {
        "percent": battery.percent,
        "plugged_in": battery.power_plugged,
        "design_capacity_mWh": design_capacity,
        "full_charge_capacity_mWh": full_charge_capacity,
        "health_percent": round(health, 2)
    }


if __name__ == "__main__":
    result = get_battery_health()
    print(result)
