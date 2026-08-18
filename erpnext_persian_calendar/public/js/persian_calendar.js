frappe.provide("erpnext_persian_calendar");

erpnext_persian_calendar.gregorian_to_jalali = (gy, gm, gd) => {
    const g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
    const gy2 = (gm > 2) ? (gy + 1) : gy;
    let days = 355666 + (365 * gy) + Math.floor((gy2 + 3) / 4) - 
               Math.floor((gy2 + 99) / 100) + Math.floor((gy2 + 399) / 400) + 
               gd + g_d_m[gm - 1];
    
    let jy = -159 + Math.floor(33 * days / 12053);
    days -= Math.floor(1461 * jy / 4);
    const jm = 1 + Math.floor((days - Math.floor(146097 * jy / 4800)) / 30);
    const jd = days - Math.floor(146097 * jy / 4800) - 30 * jm + 1;
    
    return { year: jy, month: jm, day: jd };
};

erpnext_persian_calendar.format_shamsi = (date_str, format = "YYYY/MM/DD") => {
    if (!date_str) return "";
    
    const [gy, gm, gd] = date_str.split("-").map(Number);
    const jalali = erpnext_persian_calendar.gregorian_to_jalali(gy, gm, gd);
    
    return format
        .replace("YYYY", jalali.year)
        .replace("MM", String(jalali.month).padStart(2, '0'))
        .replace("DD", String(jalali.day).padStart(2, '0'));
};

console.log("ERPNext Persian Calendar App loaded.");
