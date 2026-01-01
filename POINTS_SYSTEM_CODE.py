# ============================================
# POINTS SYSTEM - Add to Light/views.py
# ============================================

# Add this at the top of views.py after imports and before model loading

# Points configuration based on waste type
WASTE_POINTS_MAP = {
    'plastic': 10,    # Common recyclable
    'paper': 8,       # Easily recyclable
    'cardboard': 8,   # Similar to paper
    'glass': 12,      # Valuable recyclable
    'metal': 15,      # Most valuable recyclable
    'trash': 5        # General waste (least points)
}

def calculate_points(waste_type, weight_kg=None):
    """
    Calculate points based on waste type and optional weight.
    
    Args:
        waste_type (str): Type of waste (plastic, paper, metal, glass, cardboard, trash)
        weight_kg (float): Optional weight in kg (bonus points for heavier items)
    
    Returns:
        int: Total points earned
    """
    base_points = WASTE_POINTS_MAP.get(waste_type.lower(), 5)
    
    # Bonus points based on weight (1 point per kg)
    weight_bonus = 0
    if weight_kg and weight_kg > 0:
        weight_bonus = int(weight_kg)  # 1 point per kg
    
    total_points = base_points + weight_bonus
    
    return total_points
