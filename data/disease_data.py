"""Disease data for various crops"""

DISEASE_DATA = {
    "rice": {
        "blast": {
            "name": "Rice Blast",
            "scientific_name": "Magnaporthe oryzae",
            "symptoms": [
                "Diamond-shaped lesions on leaves",
                "White to gray-green lesions with darker borders",
                "Lesions on stems and leaf collars"
            ],
            "treatment": [
                "Use resistant varieties",
                "Apply fungicides",
                "Maintain proper water management"
            ]
        },
        "bacterial_blight": {
            "name": "Bacterial Blight",
            "scientific_name": "Xanthomonas oryzae",
            "symptoms": [
                "Water-soaked lesions on leaves",
                "Yellow to white stripes on leaf blades",
                "Wilting of seedlings"
            ],
            "treatment": [
                "Use disease-free seeds",
                "Practice crop rotation",
                "Apply copper-based bactericides"
            ]
        }
    },
    "wheat": {
        "rust": {
            "name": "Wheat Rust",
            "scientific_name": "Puccinia spp.",
            "symptoms": [
                "Rusty brown pustules on leaves",
                "Yellow to brown spots",
                "Reduced grain quality"
            ],
            "treatment": [
                "Plant resistant varieties",
                "Early sowing",
                "Apply fungicides"
            ]
        },
        "powdery_mildew": {
            "name": "Powdery Mildew",
            "scientific_name": "Blumeria graminis",
            "symptoms": [
                "White powdery patches on leaves",
                "Yellowing of leaves",
                "Reduced photosynthesis"
            ],
            "treatment": [
                "Use resistant varieties",
                "Proper spacing between plants",
                "Apply sulfur-based fungicides"
            ]
        }
    },
    "maize": {
        "leaf_blight": {
            "name": "Northern Leaf Blight",
            "scientific_name": "Exserohilum turcicum",
            "symptoms": [
                "Long elliptical gray-green lesions",
                "Lesions turn tan as they mature",
                "Starts from lower leaves"
            ],
            "treatment": [
                "Crop rotation",
                "Remove infected debris",
                "Apply fungicides when needed"
            ]
        },
        "rust": {
            "name": "Common Rust",
            "scientific_name": "Puccinia sorghi",
            "symptoms": [
                "Small reddish-brown pustules",
                "Pustules on both leaf surfaces",
                "Severe infection causes leaf death"
            ],
            "treatment": [
                "Plant resistant hybrids",
                "Early planting",
                "Foliar fungicides"
            ]
        }
    },
    "cotton": {
        "bacterial_blight": {
            "name": "Bacterial Blight",
            "scientific_name": "Xanthomonas axonopodis",
            "symptoms": [
                "Angular water-soaked lesions",
                "Dark brown to black lesions",
                "Premature defoliation"
            ],
            "treatment": [
                "Use disease-free seeds",
                "Crop rotation",
                "Avoid overhead irrigation"
            ]
        },
        "verticillium_wilt": {
            "name": "Verticillium Wilt",
            "scientific_name": "Verticillium dahliae",
            "symptoms": [
                "Yellowing between leaf veins",
                "Wilting of leaves",
                "Internal browning of stems"
            ],
            "treatment": [
                "Use resistant varieties",
                "Crop rotation",
                "Proper irrigation management"
            ]
        }
    },
    "sugarcane": {
        "red_rot": {
            "name": "Red Rot",
            "scientific_name": "Colletotrichum falcatum",
            "symptoms": [
                "Red discoloration in split canes",
                "Drying of leaves",
                "White patches with red margins"
            ],
            "treatment": [
                "Use disease-free setts",
                "Hot water treatment of setts",
                "Remove infected plants"
            ]
        },
        "smut": {
            "name": "Whip Smut",
            "scientific_name": "Sporisorium scitamineum",
            "symptoms": [
                "Black whip-like structure at growing point",
                "Grass-like shoots",
                "Stunted growth"
            ],
            "treatment": [
                "Use resistant varieties",
                "Remove and destroy infected plants",
                "Hot water treatment of setts"
            ]
        }
    }
}
