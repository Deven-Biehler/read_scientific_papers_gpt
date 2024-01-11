import json

fileInput = "backup data/output_gpt_4_old.json"
fileOutput = "output_gpt_4.json"
with open(fileInput, 'r') as file:
    data = json.load(file)

corrected_data = []

for entry in data:
    paperFileName = entry["paperFileName"]
    extractData = entry["extractData"]

    # Check if paperFileName already exists in corrected_data
    existing_entry = next((item for item in corrected_data if item["paperFileName"] == paperFileName), None)
    if existing_entry:
        for extract in extractData:
            if extract not in existing_entry["extractData"]:
                existing_entry["extractData"].append(extract)
    else:
        corrected_data.append(entry)




with open(fileOutput, 'w') as file:
    json.dump(corrected_data, file, indent=4)