import json

def load_data():
    with open("C:\\Users\\syezzu\\OneDrive - Capgemini\\Desktop\\Box\\Iteam.json", 'r') as f:
        items_data = json.load(f)
    
    with open("C:\\Users\\syezzu\\OneDrive - Capgemini\\Desktop\\Box\\Box.json", 'r') as f:
        boxes_data = json.load(f)
    
    return items_data, boxes_data

def calculate_item_volume(item_code, items_data):
    item = items_data[item_code]
    length = item['dimension']['length']
    width = item['dimension']['width']
    height = item['dimension']['height']
    return length * width * height

def calculate_total_weight(item_code, quantity, items_data):
    item = items_data[item_code]
    return item['weight_per_item'] * quantity

def check_box_fit(box, total_item_volume, total_weight):
    box_volume = box['dimension']['length'] * box['dimension']['width'] * box['dimension']['height']
    return total_weight <= box['max_weight'] and total_item_volume <= box_volume

def calculate_remaining_space(box, total_item_volume):
    box_volume = box['dimension']['length'] * box['dimension']['width'] * box['dimension']['height']
    remaining_space = box_volume - total_item_volume
    return remaining_space if remaining_space >= 0 else 0

def get_packing_info(items_and_quantities):
    
    items_data, boxes_data = load_data()
    
    results = []

    for item_code, quantity in items_and_quantities:
        item_volume = calculate_item_volume(item_code, items_data)
        total_item_volume = item_volume * quantity
        total_weight = calculate_total_weight(item_code, quantity, items_data)
        
        suitable_box_found = False
        
        for box_type, box in boxes_data.items():
            if check_box_fit(box, total_item_volume, total_weight):
                remaining_space = calculate_remaining_space(box, total_item_volume)
                results.append({
                    "item_code": item_code,
                    "quantity": quantity,
                    "box_type": box_type,
                    "total_weight": total_weight,
                    "remaining_space": remaining_space
                })
                suitable_box_found = True
                break
        
        if not suitable_box_found:
            results.append({
                "item_code": item_code,
                "quantity": quantity,
                "message": "No suitable box found"
            })
    
    return results


items_and_quantities = []
while True:
    item_code = input("Enter item code (e.g., item001) or type 'done' to finish: ")
    if item_code.lower() == 'done':
        break
    quantity = int(input(f"Enter quantity for {item_code}: "))
    items_and_quantities.append((item_code, quantity))

results = get_packing_info(items_and_quantities)  # Corrected this line

# Displaying results
for result in results:
    if "message" in result:
        print(f"Item Code: {result['item_code']} (Quantity: {result['quantity']}) - {result['message']}")
    else:
        print(f"Item Code: {result['item_code']} (Quantity: {result['quantity']})")
        print(f"  Box Type: {result['box_type']}")
        print(f"  Total Weight: {result['total_weight']} kg")
        print(f"  Remaining Space: {result['remaining_space']} cubic units")
        print()
