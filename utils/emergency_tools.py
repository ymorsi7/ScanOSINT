def generate_checklist(disaster_type, household_size, special_needs):
    """Generates customized emergency preparedness checklist"""
    base_items = {
        "Water": f"{household_size * 3} gallons (3 days supply)",
        "Food": f"{household_size * 3} days of non-perishable food",
        "Flashlights": f"{household_size} flashlights",
        "Batteries": "Multiple sets",
        "First Aid Kit": "1 comprehensive kit",
        "Emergency Radio": "1 battery-powered or hand-crank radio",
        "Medications": "7-day supply",
        "Important Documents": "Copies in waterproof container",
        "Cash": "Small bills and change",
        "Basic Tools": "Multi-tool, wrench, pliers",
    }
    
    # Add disaster-specific items
    disaster_specific = {
        "Earthquake": {
            "Whistle": "1 per person",
            "Fire Extinguisher": "1",
            "Heavy gloves": f"{household_size} pairs"
        },
        "Hurricane": {
            "Plywood": "For windows",
            "Tarps": "2-3 heavy duty",
            "Sandbags": "As needed"
        },
        "Flood": {
            "Life Jackets": f"{household_size}",
            "Rubber Boots": f"{household_size} pairs",
            "Sandbags": "As needed"
        },
        "Wildfire": {
            "N95 Masks": f"{household_size * 3}",
            "Goggles": f"{household_size}",
            "Emergency blankets": f"{household_size}"
        },
        "Tsunami": {
            "Life Jackets": f"{household_size}",
            "Emergency whistle": f"{household_size}",
            "Rope": "100 feet"
        }
    }
    
    # Add special needs items
    special_items = {
        "Elderly": {
            "Extra medications": "2-week supply",
            "Mobility aids": "As needed",
            "Medical equipment backup": "If applicable"
        },
        "Children": {
            "Baby supplies": "1 week supply",
            "Activities/Games": "Several options",
            "Comfort items": "Favorite toys/blankets"
        },
        "Pets": {
            "Pet food": "1 week supply",
            "Pet medications": "If applicable",
            "Pet carriers": "1 per pet"
        },
        "Medical Conditions": {
            "Medical supplies": "2-week supply",
            "Medical documents": "Copies",
            "Care instructions": "Written copy"
        },
        "Mobility Issues": {
            "Extra mobility aids": "If applicable",
            "Emergency assistance items": "As needed",
            "Medical alert system": "If applicable"
        }
    }
    
    checklist = base_items.copy()
    checklist.update(disaster_specific.get(disaster_type, {}))
    
    for need in special_needs:
        checklist.update(special_items.get(need, {}))
    
    return checklist

def suggest_resources(disaster_type, household_size):
    """Generates resource allocation suggestions"""
    resource_categories = {
        "Essential Supplies": {
            "estimated_cost": household_size * 100,
            "priority": "High",
            "replacement_interval": "6 months"
        },
        "Emergency Equipment": {
            "estimated_cost": household_size * 150,
            "priority": "High",
            "replacement_interval": "Yearly"
        },
        "Communication Devices": {
            "estimated_cost": 200,
            "priority": "Medium",
            "replacement_interval": "2 years"
        },
        "Medical Supplies": {
            "estimated_cost": household_size * 50,
            "priority": "High",
            "replacement_interval": "Yearly"
        }
    }
    
    return resource_categories
