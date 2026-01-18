"""
Enhanced Natural Remedies System
Comprehensive remedy database with disease-specific treatments
"""

import json
import os
from typing import List, Dict, Optional

class EnhancedRemedySystem:
    """Enhanced remedy system with comprehensive natural treatments."""
    
    def __init__(self):
        self.remedy_database = {}
        self.precautions_database = {}
        self.load_remedy_data()
        self.initialize_comprehensive_remedies()
    
    def load_remedy_data(self):
        """Load existing remedy data."""
        try:
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'remedies.json')
            with open(data_path, 'r') as f:
                data = json.load(f)
            
            self.remedy_database = data.get('remedy_database', {})
            self.precautions_database = data.get('disease_precautions', {})
            
        except Exception as e:
            print(f"Error loading remedy data: {e}")
    
    def initialize_comprehensive_remedies(self):
        """Initialize comprehensive remedy database for all 41 conditions."""
        
        comprehensive_remedies = {
            # Infectious Diseases
            "fungal infection": [
                {
                    "remedy": "Tea Tree Oil",
                    "benefit": "Powerful antifungal properties",
                    "explanation": "Contains terpinen-4-ol which disrupts fungal cell membranes",
                    "usage": "Dilute 2-3 drops in carrier oil, apply topically 2x daily"
                },
                {
                    "remedy": "Apple Cider Vinegar",
                    "benefit": "Creates acidic environment hostile to fungi",
                    "explanation": "Acetic acid restores skin pH and inhibits fungal growth",
                    "usage": "Mix 1:1 with water, apply with cotton ball"
                },
                {
                    "remedy": "Coconut Oil",
                    "benefit": "Natural antifungal and moisturizing",
                    "explanation": "Lauric acid and caprylic acid have antifungal properties",
                    "usage": "Apply virgin coconut oil directly to affected area"
                }
            ],
            
            "viral infection": [
                {
                    "remedy": "Elderberry Syrup",
                    "benefit": "Boosts immune system and reduces viral load",
                    "explanation": "Anthocyanins block viral replication and enhance immunity",
                    "usage": "1 tablespoon 3x daily during illness"
                },
                {
                    "remedy": "Ginger Tea",
                    "benefit": "Anti-inflammatory and immune boosting",
                    "explanation": "Gingerol compounds reduce inflammation and support immune function",
                    "usage": "Steep 1 inch fresh ginger in hot water for 10 minutes"
                },
                {
                    "remedy": "Echinacea",
                    "benefit": "Stimulates immune response",
                    "explanation": "Increases white blood cell activity and cytokine production",
                    "usage": "300mg standardized extract 3x daily"
                }
            ],
            
            # Respiratory Conditions
            "common cold": [
                {
                    "remedy": "Honey and Lemon",
                    "benefit": "Soothes throat and provides vitamin C",
                    "explanation": "Honey has antimicrobial properties, lemon provides immune support",
                    "usage": "Mix 1 tbsp honey with juice of half lemon in warm water"
                },
                {
                    "remedy": "Steam Inhalation with Eucalyptus",
                    "benefit": "Clears nasal congestion",
                    "explanation": "Eucalyptol opens airways and has antimicrobial effects",
                    "usage": "Add 3-4 drops eucalyptus oil to bowl of hot water, inhale steam"
                },
                {
                    "remedy": "Zinc Lozenges",
                    "benefit": "Reduces cold duration and severity",
                    "explanation": "Zinc interferes with viral replication in throat tissues",
                    "usage": "One 13-23mg lozenge every 2 hours while awake"
                }
            ],
            
            "bronchial asthma": [
                {
                    "remedy": "Butterbur Extract",
                    "benefit": "Natural bronchodilator",
                    "explanation": "Petasins reduce inflammation and relax bronchial muscles",
                    "usage": "50-75mg standardized extract twice daily"
                },
                {
                    "remedy": "Magnesium",
                    "benefit": "Relaxes airway muscles",
                    "explanation": "Acts as natural calcium channel blocker, reducing bronchospasm",
                    "usage": "200-400mg magnesium glycinate daily"
                },
                {
                    "remedy": "Quercetin",
                    "benefit": "Stabilizes mast cells and reduces inflammation",
                    "explanation": "Flavonoid that prevents histamine release and reduces airway inflammation",
                    "usage": "500mg twice daily with bromelain for absorption"
                }
            ],
            
            # Digestive Disorders
            "gerd": [
                {
                    "remedy": "Aloe Vera Juice",
                    "benefit": "Soothes esophageal inflammation",
                    "explanation": "Anti-inflammatory compounds reduce acid irritation",
                    "usage": "1/4 cup pure aloe juice 20 minutes before meals"
                },
                {
                    "remedy": "Slippery Elm",
                    "benefit": "Coats and protects digestive tract",
                    "explanation": "Mucilage forms protective barrier against stomach acid",
                    "usage": "1-2 tsp powder mixed in water before meals"
                },
                {
                    "remedy": "D-Limonene",
                    "benefit": "Promotes gastric motility",
                    "explanation": "Citrus extract helps stomach empty faster, reducing reflux",
                    "usage": "1000mg every other day for 20 days"
                }
            ],
            
            "peptic ulcer diseae": [
                {
                    "remedy": "Manuka Honey",
                    "benefit": "Antibacterial against H. pylori",
                    "explanation": "Methylglyoxal kills H. pylori bacteria that cause ulcers",
                    "usage": "1 tablespoon on empty stomach 3x daily"
                },
                {
                    "remedy": "Cabbage Juice",
                    "benefit": "Heals stomach lining",
                    "explanation": "Vitamin U (S-methylmethionine) promotes ulcer healing",
                    "usage": "1/2 cup fresh cabbage juice twice daily"
                },
                {
                    "remedy": "Licorice Root (DGL)",
                    "benefit": "Protects stomach lining",
                    "explanation": "Increases mucus production and promotes healing",
                    "usage": "380mg DGL tablets 20 minutes before meals"
                }
            ],
            
            # Metabolic Conditions
            "diabetes": [
                {
                    "remedy": "Cinnamon",
                    "benefit": "Improves insulin sensitivity",
                    "explanation": "Polyphenols enhance glucose uptake and insulin function",
                    "usage": "1-2 tsp Ceylon cinnamon daily with meals"
                },
                {
                    "remedy": "Bitter Melon",
                    "benefit": "Natural blood sugar control",
                    "explanation": "Contains compounds that mimic insulin action",
                    "usage": "1/2 cup fresh juice or 2g dried extract daily"
                },
                {
                    "remedy": "Chromium Picolinate",
                    "benefit": "Enhances glucose metabolism",
                    "explanation": "Improves insulin sensitivity and glucose tolerance",
                    "usage": "200-400mcg daily with meals"
                }
            ],
            
            "hypothyroidism": [
                {
                    "remedy": "Kelp/Seaweed",
                    "benefit": "Natural iodine source",
                    "explanation": "Iodine is essential for thyroid hormone synthesis",
                    "usage": "150-300mcg iodine from kelp supplements daily"
                },
                {
                    "remedy": "Brazil Nuts",
                    "benefit": "High in selenium",
                    "explanation": "Selenium required for T4 to T3 conversion",
                    "usage": "2-3 Brazil nuts daily (provides ~200mcg selenium)"
                },
                {
                    "remedy": "Ashwagandha",
                    "benefit": "Adaptogen supporting thyroid function",
                    "explanation": "Helps normalize thyroid hormone levels and reduces stress",
                    "usage": "300-500mg standardized extract twice daily"
                }
            ],
            
            "hyperthyroidism": [
                {
                    "remedy": "Lemon Balm",
                    "benefit": "Blocks thyroid stimulating hormone",
                    "explanation": "Rosmarinic acid inhibits TSH receptor activation",
                    "usage": "300-500mg extract or 2-3 cups tea daily"
                },
                {
                    "remedy": "L-Carnitine",
                    "benefit": "Reduces hyperthyroid symptoms",
                    "explanation": "Blocks thyroid hormone action at cellular level",
                    "usage": "2-4g daily in divided doses"
                },
                {
                    "remedy": "Bugleweed",
                    "benefit": "Reduces thyroid hormone production",
                    "explanation": "Inhibits thyroid peroxidase enzyme",
                    "usage": "1-2ml tincture 3x daily (under supervision)"
                }
            ],
            
            # Cardiovascular
            "hypertension": [
                {
                    "remedy": "Hibiscus Tea",
                    "benefit": "Natural ACE inhibitor",
                    "explanation": "Anthocyanins relax blood vessels and lower pressure",
                    "usage": "2-3 cups hibiscus tea daily"
                },
                {
                    "remedy": "Garlic",
                    "benefit": "Vasodilator and cardioprotective",
                    "explanation": "Allicin promotes nitric oxide production, relaxing arteries",
                    "usage": "600-900mg aged garlic extract daily"
                },
                {
                    "remedy": "Hawthorn Berry",
                    "benefit": "Strengthens heart and improves circulation",
                    "explanation": "Oligomeric procyanidins support cardiovascular health",
                    "usage": "160-900mg standardized extract daily"
                }
            ],
            
            "heart attack": [
                {
                    "remedy": "Immediate Medical Attention",
                    "benefit": "Life-saving emergency care",
                    "explanation": "Heart attacks require immediate professional medical intervention",
                    "usage": "Call 911 immediately - this is a medical emergency"
                },
                {
                    "remedy": "Aspirin (if available)",
                    "benefit": "Blood thinner to reduce clot formation",
                    "explanation": "Inhibits platelet aggregation during acute event",
                    "usage": "Chew 325mg aspirin if not allergic (while waiting for emergency care)"
                }
            ],
            
            # Musculoskeletal
            "arthritis": [
                {
                    "remedy": "Turmeric with Black Pepper",
                    "benefit": "Powerful anti-inflammatory",
                    "explanation": "Curcumin reduces inflammatory cytokines, piperine enhances absorption",
                    "usage": "500-1000mg curcumin with 5mg piperine daily"
                },
                {
                    "remedy": "Fish Oil (Omega-3)",
                    "benefit": "Reduces joint inflammation",
                    "explanation": "EPA/DHA decrease inflammatory prostaglandins and leukotrienes",
                    "usage": "2-3g combined EPA/DHA daily with meals"
                },
                {
                    "remedy": "Boswellia",
                    "benefit": "Natural COX-2 inhibitor",
                    "explanation": "Boswellic acids block inflammatory enzymes without stomach irritation",
                    "usage": "300-400mg standardized extract 2-3x daily"
                }
            ],
            
            # Neurological
            "migraine": [
                {
                    "remedy": "Feverfew",
                    "benefit": "Prevents migraine attacks",
                    "explanation": "Parthenolide reduces inflammation and vascular spasms",
                    "usage": "100-300mg standardized extract daily for prevention"
                },
                {
                    "remedy": "Magnesium Glycinate",
                    "benefit": "Reduces migraine frequency",
                    "explanation": "Prevents cortical spreading depression and vascular changes",
                    "usage": "400-600mg daily for prevention"
                },
                {
                    "remedy": "Riboflavin (B2)",
                    "benefit": "Improves cellular energy metabolism",
                    "explanation": "Enhances mitochondrial function in brain cells",
                    "usage": "400mg daily for 3 months minimum"
                }
            ]
        }
        
        # Merge with existing remedies
        for disease, remedies in comprehensive_remedies.items():
            if disease not in self.remedy_database:
                self.remedy_database[disease] = remedies
            else:
                # Add new remedies to existing ones
                existing_remedy_names = {r['remedy'] for r in self.remedy_database[disease]}
                for remedy in remedies:
                    if remedy['remedy'] not in existing_remedy_names:
                        self.remedy_database[disease].append(remedy)
    
    def get_remedies(self, condition: str) -> List[Dict]:
        """Get remedies for a specific condition."""
        return self.remedy_database.get(condition.lower(), [])
    
    def get_precautions(self, condition: str) -> List[str]:
        """Get precautions for a specific condition."""
        return self.precautions_database.get(condition.lower(), [])
    
    def get_emergency_remedies(self, condition: str) -> Dict:
        """Get emergency remedies for critical conditions."""
        emergency_conditions = {
            "heart attack": {
                "immediate_actions": [
                    "Call 911 immediately",
                    "Chew aspirin if available and not allergic",
                    "Sit down and rest",
                    "Loosen tight clothing"
                ],
                "warning": "This is a life-threatening emergency requiring immediate medical attention"
            },
            "paralysis (brain hemorrhage)": {
                "immediate_actions": [
                    "Call 911 immediately",
                    "Do not give food or water",
                    "Keep person calm and still",
                    "Note time symptoms started"
                ],
                "warning": "Brain hemorrhage requires immediate emergency medical care"
            },
            "hepatitis e": {
                "immediate_actions": [
                    "Seek immediate medical attention",
                    "Avoid alcohol completely",
                    "Stay hydrated with clear fluids",
                    "Rest and avoid strenuous activity"
                ],
                "warning": "Acute liver failure can be life-threatening"
            }
        }
        
        return emergency_conditions.get(condition.lower(), {})
    
    def get_lifestyle_recommendations(self, condition: str) -> List[str]:
        """Get lifestyle recommendations for managing conditions."""
        lifestyle_recommendations = {
            "diabetes": [
                "Follow a low-glycemic diet",
                "Exercise regularly (150 minutes/week)",
                "Monitor blood sugar levels",
                "Maintain healthy weight",
                "Stay hydrated",
                "Get adequate sleep (7-9 hours)"
            ],
            "hypertension": [
                "Reduce sodium intake (<2300mg/day)",
                "Increase potassium-rich foods",
                "Maintain healthy weight",
                "Exercise regularly",
                "Limit alcohol consumption",
                "Manage stress through meditation/yoga",
                "Quit smoking"
            ],
            "arthritis": [
                "Maintain healthy weight",
                "Low-impact exercise (swimming, walking)",
                "Apply heat/cold therapy",
                "Practice gentle stretching",
                "Use ergonomic tools",
                "Get adequate sleep"
            ],
            "gerd": [
                "Eat smaller, frequent meals",
                "Avoid trigger foods (spicy, acidic, fatty)",
                "Don't lie down after eating",
                "Elevate head of bed",
                "Maintain healthy weight",
                "Quit smoking",
                "Limit alcohol and caffeine"
            ]
        }
        
        return lifestyle_recommendations.get(condition.lower(), [])
    
    def get_dietary_recommendations(self, condition: str) -> Dict:
        """Get specific dietary recommendations."""
        dietary_recommendations = {
            "diabetes": {
                "foods_to_include": [
                    "Leafy greens", "Fatty fish", "Nuts and seeds", 
                    "Berries", "Sweet potatoes", "Legumes"
                ],
                "foods_to_avoid": [
                    "Refined sugars", "White bread", "Processed foods",
                    "Sugary drinks", "Trans fats"
                ]
            },
            "hypertension": {
                "foods_to_include": [
                    "Bananas", "Leafy greens", "Berries", "Beets",
                    "Oats", "Garlic", "Dark chocolate"
                ],
                "foods_to_avoid": [
                    "High sodium foods", "Processed meats", "Canned soups",
                    "Fast food", "Alcohol in excess"
                ]
            },
            "arthritis": {
                "foods_to_include": [
                    "Fatty fish", "Leafy greens", "Berries", "Cherries",
                    "Olive oil", "Nuts", "Turmeric"
                ],
                "foods_to_avoid": [
                    "Processed foods", "Refined sugars", "Trans fats",
                    "Excessive omega-6 oils"
                ]
            }
        }
        
        return dietary_recommendations.get(condition.lower(), {})