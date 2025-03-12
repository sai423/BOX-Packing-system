import json

def load_data():
    try:
        with open("C:\\Users\\syezzu\\OneDrive - Capgemini\\Desktop\\Box\\Iteam.json", 'r') as f:
            items_data = json.load(f)
        
        with open("C:\\Users\\syezzu\\OneDrive - Capgemini\\Desktop\\Box\\Box.json", 'r') as f:
            boxes_data = json.load(f)
        
        return items_data, boxes_data
    except FileNotFoundError as e:
        print(f"Error loading file: {e}")
        return None, None

def calculate_item_volume(item_code, items_data):
    try:
        item = items_data[item_code]
        length = item['dimension']['length']
        width = item['dimension']['width']
        height = item['dimension']['height']
        return length * width * height
    except KeyError:
        print(f"Error: Item code '{item_code}' not found in item data.")
        return 0

def calculate_total_weight(item_code, quantity, items_data):
    try:
        item = items_data[item_code]
        return item['weight_per_item'] * quantity
    except KeyError:
        print(f"Error: Item code '{item_code}' not found in item data.")
        return 0

def check_box_fit(box, total_item_volume, total_weight):
    box_volume = box['dimension']['length'] * box['dimension']['width'] * box['dimension']['height']
    return total_weight <= box['max_weight'] and total_item_volume <= box_volume

def calculate_remaining_space(box, total_item_volume):
    box_volume = box['dimension']['length'] * box['dimension']['width'] * box['dimension']['height']
    remaining_space = box_volume - total_item_volume
    return remaining_space if remaining_space >= 0 else 0

def calculate_remaining_space_percentage(box, remaining_space):
    box_volume = box['dimension']['length'] * box['dimension']['width'] * box['dimension']['height']
    return (remaining_space / box_volume) * 100 if box_volume != 0 else 0

def calculate_items_that_fit_in_box(box, item_volume, box_data):
    box_volume = box['dimension']['length'] * box['dimension']['width'] * box['dimension']['height']
    max_items_by_volume = box_volume // item_volume
    max_items_by_weight = box['max_weight'] // box_data['weight_per_item']
    return min(max_items_by_volume, max_items_by_weight)

def get_packing_info(items_and_quantities):
    items_data, boxes_data = load_data()
    
    if not items_data or not boxes_data:
        return []

    results = []
    
    for item_code, quantity in items_and_quantities:
        item_volume = calculate_item_volume(item_code, items_data)
        if item_volume == 0:
            continue  # Skip if item code is invalid
        
        total_item_volume = item_volume * quantity
        total_weight = calculate_total_weight(item_code, quantity, items_data)
        if total_weight == 0:
            continue  # Skip if total weight calculation failed
        
        suitable_box_found = False
        
        for box_type, box in boxes_data.items():
            if check_box_fit(box, total_item_volume, total_weight):
                remaining_space = calculate_remaining_space(box, total_item_volume)
                remaining_space_percentage = calculate_remaining_space_percentage(box, remaining_space)
                items_that_fit = calculate_items_that_fit_in_box(box, item_volume, items_data[item_code])
                
                results.append({
                    "item_code": item_code,
                    "quantity": quantity,
                    "box_type": box_type,
                    "total_weight": total_weight,
                    "remaining_space": remaining_space,
                    "remaining_space_percentage": remaining_space_percentage,
                    "items_that_fit": items_that_fit
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

results = get_packing_info(items_and_quantities)

if not results:
    print("No results to display.")
else:
    for result in results:
        if "message" in result:
            print(f"Item Code: {result['item_code']} (Quantity: {result['quantity']}) - {result['message']}")
        else:
            print(f"Item Code: {result['item_code']} (Quantity: {result['quantity']})")
            print(f"  Box Type: {result['box_type']}")
            print(f"  Total Weight: {result['total_weight']} kg")
            print(f"  Remaining Space: {result['remaining_space']} cubic units")
            print(f"  Remaining Space Percentage: {result['remaining_space_percentage']:.2f}%")
            print(f"  Items that can fit in box: {result['items_that_fit']}")
            print()
