"""Crop data including optimal conditions and recommendations"""

import pandas as pd
CROP_DATA = {
    "Rice": {
        "name": "Rice",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 35},
            "humidity": {"min": 60, "max": 80},
            "rainfall": {"min": 800, "max": 2000}
        }
    },
    "Wheat": {
        "name": "Wheat",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 30},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 500, "max": 1200}
        }
    },
    "Maize": {
        "name": "Maize",
        "optimal_conditions": {
            "temperature": {"min": 18, "max": 32},
            "humidity": {"min": 50, "max": 75},
            "rainfall": {"min": 600, "max": 1100}
        }
    },
    "Cotton": {
        "name": "Cotton",
        "optimal_conditions": {
            "temperature": {"min": 21, "max": 35},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 500, "max": 1500}
        }
    },
    "Sugarcane": {
        "name": "Sugarcane",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 35},
            "humidity": {"min": 60, "max": 80},
            "rainfall": {"min": 1000, "max": 2000}
        }
    },
    "Potato": {
        "name": "Potato",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 25},
            "humidity": {"min": 50, "max": 75},
            "rainfall": {"min": 500, "max": 1000}
        }
    },
    "Groundnut": {
        "name": "Groundnut",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 30},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 500, "max": 1200}
        }
    },
    "Soybean": {
        "name": "Soybean",
        "description": "A versatile crop used for food, feed, and oil production.",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 30},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 500, "max": 1000}
        }
    },
    "Coconut": {
        "name": "Coconut",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 35},
            "humidity": {"min": 70, "max": 90},
            "rainfall": {"min": 1500, "max": 2500}
        }
    },
    "Banana": {
        "name": "Banana",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 35},
            "humidity": {"min": 70, "max": 90},
            "rainfall": {"min": 1200, "max": 2200}
        }
    },
    "Mango": {
        "name": "Mango",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 35},
            "humidity": {"min": 50, "max": 80},
            "rainfall": {"min": 750, "max": 1500}
        }
    },
    "Tea": {
        "name": "Tea",
        "optimal_conditions": {
            "temperature": {"min": 18, "max": 30},
            "humidity": {"min": 70, "max": 90},
            "rainfall": {"min": 1500, "max": 3000}
        }
    },
    "Coffee": {
        "name": "Coffee",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 28},
            "humidity": {"min": 70, "max": 90},
            "rainfall": {"min": 1500, "max": 2500}
        }
    },
    "Jute": {
        "name": "Jute",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 35},
            "humidity": {"min": 60, "max": 90},
            "rainfall": {"min": 1200, "max": 2000}
        }
    },
    "Rubber": {
        "name": "Rubber",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 35},
            "humidity": {"min": 70, "max": 90},
            "rainfall": {"min": 2000, "max": 4000}
        }
    },
    "Barley": {
        "name": "Barley",
        "description": "A cereal grain that is a key ingredient in beer and animal feed.",
        "optimal_conditions": {
            "temperature": {"min": 10, "max": 25},
            "humidity": {"min": 40, "max": 60},
            "rainfall": {"min": 400, "max": 800}
        }
    },
    "Oats": {
        "name": "Oats",
        "description": "A nutritious grain commonly used for breakfast cereals and livestock feed.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 25},
            "humidity": {"min": 50, "max": 80},
            "rainfall": {"min": 600, "max": 1200}
        }
    },
    "Peas": {
        "name": "Peas",
        "description": "A cool-season crop that is high in protein and fiber.",
        "optimal_conditions": {
            "temperature": {"min": 10, "max": 20},
            "humidity": {"min": 60, "max": 80},
            "rainfall": {"min": 500, "max": 800}
        }
    },
    "Lentils": {
        "name": "Lentils",
        "description": "A legume that is a great source of protein and nutrients.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 25},
            "humidity": {"min": 40, "max": 70},
            "rainfall": {"min": 300, "max": 600}
        }
    },
    "Potatoes": {
        "name": "Potatoes",
        "description": "A starchy root vegetable that is a staple food in many cultures.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 25},
            "humidity": {"min": 60, "max": 80},
            "rainfall": {"min": 500, "max": 1000}
        }
    },
    "Tomatoes": {
        "name": "Tomatoes",
        "description": "A popular fruit used in salads, sauces, and many dishes.",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 30},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 400, "max": 800}
        }
    },
    "Peppers": {
        "name": "Peppers",
        "description": "A versatile vegetable that comes in various colors and flavors.",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 30},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 500, "max": 1000}
        }
    },
    "Carrots": {
        "name": "Carrots",
        "description": "A root vegetable that is rich in beta-carotene and vitamins.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 20},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 300, "max": 600}
        }
    },
    "Onions": {
        "name": "Onions",
        "description": "A bulb vegetable that adds flavor to many dishes.",
        "optimal_conditions": {
            "temperature": {"min": 10, "max": 25},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 400, "max": 800}
        }
    },
    "Garlic": {
        "name": "Garlic",
        "description": "A bulb used for flavoring and medicinal purposes.",
        "optimal_conditions": {
            "temperature": {"min": 10, "max": 25},
            "humidity": {"min": 40, "max": 60},
            "rainfall": {"min": 300, "max": 600}
        }
    },
    "Spinach": {
        "name": "Spinach",
        "description": "A leafy green vegetable that is rich in iron and vitamins.",
        "optimal_conditions": {
            "temperature": {"min": 10, "max": 20},
            "humidity": {"min": 60, "max": 80},
            "rainfall": {"min": 400, "max": 800}
        }
    },
    "Cabbage": {
        "name": "Cabbage",
        "description": "A leafy green vegetable used in salads and cooking.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 25},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 600, "max": 1200}
        }
    },
    "Broccoli": {
        "name": "Broccoli",
        "description": "A green vegetable that is high in vitamins and minerals.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 25},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 600, "max": 1200}
        }
    },
    "Cauliflower": {
        "name": "Cauliflower",
        "description": "A white vegetable that is a good source of vitamins C and K.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 25},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 600, "max": 1200}
        }
    },
    "Eggplant": {
        "name": "Eggplant",
        "description": "A purple vegetable that is used in many cuisines.",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 30},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 400, "max": 800}
        }
    },
    "Zucchini": {
        "name": "Zucchini",
        "description": "A summer squash that is low in calories and high in nutrients.",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 30},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 400, "max": 800}
        }
    },
    "Radishes": {
        "name": "Radishes",
        "description": "A root vegetable known for its peppery flavor.",
        "optimal_conditions": {
            "temperature": {"min": 10, "max": 20},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 300, "max": 600}
        }
    },
    "Wheat": {
        "name": "Wheat",
        "description": "A staple grain used for food and feed.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 30},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 500, "max": 1200}
        }
    },
    "Rice": {
        "name": "Rice",
        "description": "A primary food source for over half the world's population.",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 35},
            "humidity": {"min": 60, "max": 80},
            "rainfall": {"min": 800, "max": 2000}
        }
    },
    "Corn": {
        "name": "Corn",
        "description": "A versatile crop used for food, feed, and fuel.",
        "optimal_conditions": {
            "temperature": {"min": 18, "max": 30},
            "humidity": {"min": 50, "max": 75},
            "rainfall": {"min": 500, "max": 1200}
        }
    },
    "Barley": {
        "name": "Barley",
        "description": "A cereal grain that is a key ingredient in beer and animal feed.",
        "optimal_conditions": {
            "temperature": {"min": 10, "max": 25},
            "humidity": {"min": 40, "max": 60},
            "rainfall": {"min": 400, "max": 800}
        }
    },
    "Soybean": {
        "name": "Soybean",
        "description": "A versatile crop used for food, feed, and oil production.",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 30},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 500, "max": 1000}
        }
    },
    "Potato": {
        "name": "Potato",
        "description": "A starchy root vegetable that is a staple food in many cultures.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 25},
            "humidity": {"min": 60, "max": 80},
            "rainfall": {"min": 500, "max": 1000}
        }
    },
    "Maize": {
        "name": "Maize",
        "description": "A staple crop used for food and livestock feed.",
        "optimal_conditions": {
            "temperature": {"min": 18, "max": 30},
            "humidity": {"min": 50, "max": 75},
            "rainfall": {"min": 600, "max": 1200}
        }
    },
    "Millet": {
        "name": "Millet",
        "description": "A drought-resistant grain that is a staple in many parts of the world.",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 30},
            "humidity": {"min": 40, "max": 60},
            "rainfall": {"min": 400, "max": 800}
        }
    },
    "Sugarcane": {
        "name": "Sugarcane",
        "description": "A tropical grass that is the primary source of sugar.",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 30},
            "humidity": {"min": 60, "max": 80},
            "rainfall": {"min": 1500, "max": 3000}
        }
    },
    "Peas": {
        "name": "Peas",
        "description": "A cool-season crop that is high in protein and fiber.",
        "optimal_conditions": {
            "temperature": {"min": 10, "max": 20},
            "humidity": {"min": 60, "max": 80},
            "rainfall": {"min": 500, "max": 800}
        }
    },
    "Cotton": {
        "name": "Cotton",
        "description": "A soft, fluffy staple fiber that grows in a boll.",
        "optimal_conditions": {
            "temperature": {"min": 21, "max": 35},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 500, "max": 1500}
        }
    },
    "Sorghum": {
        "name": "Sorghum",
        "description": "A drought-resistant cereal grain used for food and animal feed.",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 30},
            "humidity": {"min": 40, "max": 60},
            "rainfall": {"min": 300, "max": 700}
        }
    },
    "Lentil": {
        "name": "Lentil",
        "description": "A legume that is a great source of protein and nutrients.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 25},
            "humidity": {"min": 40, "max": 70},
            "rainfall": {"min": 300, "max": 600}
        }
    },
    "Oats": {
        "name": "Oats",
        "description": "A nutritious grain commonly used for breakfast cereals and livestock feed.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 25},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 600, "max": 1200}
        }
    },
    "Tomato": {
        "name": "Tomato",
        "description": "A popular fruit used in salads, sauces, and many dishes.",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 30},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 400, "max": 800}
        }
    },
    "Carrot": {
        "name": "Carrot",
        "description": "A root vegetable that is rich in beta-carotene and vitamins.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 20},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 300, "max": 600}
        }
    },
    "Onion": {
        "name": "Onion",
        "description": "A bulb vegetable that adds flavor to many dishes.",
        "optimal_conditions": {
            "temperature": {"min": 10, "max": 25},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 400, "max": 800}
        }
    },
    "Garlic": {
        "name": "Garlic",
        "description": "A bulb used for flavoring and medicinal purposes.",
        "optimal_conditions": {
            "temperature": {"min": 10, "max": 25},
            "humidity": {"min": 40, "max": 60},
            "rainfall": {"min": 300, "max": 600}
        }
    },
    "Spinach": {
        "name": "Spinach",
        "description": "A leafy green vegetable that is rich in iron and vitamins.",
        "optimal_conditions": {
            "temperature": {"min": 10, "max": 20},
            "humidity": {"min": 60, "max": 80},
            "rainfall": {"min": 400, "max": 800}
        }
    },
    "Cabbage": {
        "name": "Cabbage",
        "description": "A leafy green vegetable used in salads and cooking.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 25},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 600, "max": 1200}
        }
    },
    "Broccoli": {
        "name": "Broccoli",
        "description": "A green vegetable that is high in vitamins and minerals.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 25},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 600, "max": 1200}
        }
    },
    "Cauliflower": {
        "name": "Cauliflower",
        "description": "A white vegetable that is a good source of vitamins C and K.",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 25},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 600, "max": 1200}
        }
    },
    "Eggplant": {
        "name": "Eggplant",
        "description": "A purple vegetable that is used in many cuisines.",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 30},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 400, "max": 800}
        }
    },
    "Zucchini": {
        "name": "Zucchini",
        "description": "A summer squash that is low in calories and high in nutrients.",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 30},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 400, "max": 800}
        }
    },
    "Radishes": {
        "name": "Radishes",
        "description": "A root vegetable known for its peppery flavor.",
        "optimal_conditions": {
            "temperature": {"min": 10, "max": 20},
            "humidity": {"min": 50, "max": 70},
            "rainfall": {"min": 300, "max": 600}
        }
    },
}

def load_crop_yield_data(file_path):
    """Load crop yield data from a CSV file."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading crop yield data: {str(e)}")
        return pd.DataFrame()

def average_yield_per_crop(data):
    """Calculate average yield per crop."""
    try:
        return data.groupby('Crop')['Yield'].mean()
    except Exception as e:
        print(f"Error calculating average yield: {str(e)}")
        return pd.Series()

# Load the dataset
crop_yield_data = load_crop_yield_data('data/crop_yield.csv')

# Calculate average yield
average_yields = average_yield_per_crop(crop_yield_data)

# Add crops from crop_yields.csv to the CROP_DATA structure
for crop in crop_yield_data['Crop'].unique():
    if crop not in CROP_DATA:
        CROP_DATA[crop] = {
            "name": crop,
            "description": "",
            "optimal_conditions": {
                "temperature": {"min": 0, "max": 0},
                "humidity": {"min": 0, "max": 0},
                "rainfall": {"min": 0, "max": 0}
            }
        }
