Unit converter:
def unit_converter(value, unit):
if unit == "cm_to_m":
return value / 100
elif unit == "m_to_km":
return value / 1000
elif unit == "c_to_f":
return (value * 9/5) + 32
else:
return "Conversion not supported"
print(unit_converter(100, "cm_to_m"))
print(unit_converter(37, "c_to_f"))
