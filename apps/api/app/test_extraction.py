from services.extraction import extract_fields

sample = """
Paracetamol Tablets

500 mg

Batch No: AB12345

EXP: 10/2028

Store below 25°C
"""

result = extract_fields(sample)

print(result)
print()
print(result.model_dump())