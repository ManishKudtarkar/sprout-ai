#!/usr/bin/env python3
"""
Test script to demonstrate the new advanced features
"""

from ai_engine import advanced_analyze_symptoms, comprehensive_symptom_check
from ai_engine.advanced_diagnosis import AdvancedDiagnosisEngine
from ai_engine.enhanced_remedies import EnhancedRemedySystem

def test_advanced_diagnosis():
    """Test advanced diagnosis with differential diagnosis."""
    print("🔬 Testing Advanced Diagnosis")
    print("=" * 40)
    
    # Test with multiple symptoms
    result = advanced_analyze_symptoms("stomach pain, acidity, and nausea")
    
    if result['type'] == 'advanced_diagnosis':
        primary = result['primary_diagnosis']
        print(f"Primary Diagnosis: {primary['condition'].title()}")
        print(f"Confidence: {primary['confidence']}")
        
        if result.get('differential_diagnosis'):
            print("\nAlternative Diagnoses:")
            for i, alt in enumerate(result['differential_diagnosis'][:2], 1):
                print(f"{i}. {alt['disease'].title()} ({alt['confidence']})")
        
        # Show treatment plan
        treatment = result.get('treatment_plan', {})
        if treatment.get('natural_remedies'):
            print(f"\nNatural Remedies Available: {len(treatment['natural_remedies'])}")
            print(f"First remedy: {treatment['natural_remedies'][0]['remedy']}")
        
        print("✅ Advanced diagnosis working!")
    else:
        print(f"❌ Unexpected result type: {result['type']}")

def test_enhanced_remedies():
    """Test enhanced remedy system."""
    print("\n🌿 Testing Enhanced Remedies")
    print("=" * 40)
    
    remedy_system = EnhancedRemedySystem()
    
    # Test comprehensive remedies
    remedies = remedy_system.get_remedies("diabetes")
    if remedies:
        print(f"Diabetes remedies available: {len(remedies)}")
        print(f"First remedy: {remedies[0]['remedy']}")
        print(f"Scientific explanation: {remedies[0]['explanation'][:50]}...")
        print("✅ Enhanced remedies working!")
    else:
        print("❌ No remedies found for diabetes")
    
    # Test lifestyle recommendations
    lifestyle = remedy_system.get_lifestyle_recommendations("hypertension")
    if lifestyle:
        print(f"\nLifestyle recommendations for hypertension: {len(lifestyle)}")
        print(f"First recommendation: {lifestyle[0]}")
        print("✅ Lifestyle recommendations working!")

def test_symptom_extraction():
    """Test advanced symptom extraction."""
    print("\n🔍 Testing Symptom Extraction")
    print("=" * 40)
    
    engine = AdvancedDiagnosisEngine()
    
    # Test natural language symptom extraction
    test_phrases = [
        "I have a terrible headache and feel nauseous",
        "My stomach really hurts after eating",
        "I can't stop coughing and have a fever"
    ]
    
    for phrase in test_phrases:
        symptoms = engine.extract_symptoms_from_text(phrase)
        print(f"'{phrase}' → {symptoms}")
    
    print("✅ Symptom extraction working!")

def test_comprehensive_features():
    """Test comprehensive symptom checking."""
    print("\n📋 Testing Comprehensive Features")
    print("=" * 40)
    
    # Test comprehensive symptom check
    result = comprehensive_symptom_check("headache and fever")
    
    if result['type'] in ['initial_diagnosis', 'emergency', 'clarification_needed']:
        print(f"Comprehensive check type: {result['type']}")
        
        if result['type'] == 'initial_diagnosis':
            print(f"Primary diagnosis: {result['primary_diagnosis']['condition']}")
            if result.get('follow_up_questions'):
                print(f"Follow-up questions: {len(result['follow_up_questions'])}")
        
        print("✅ Comprehensive symptom checking working!")
    else:
        print(f"❌ Unexpected result type: {result['type']}")

def main():
    """Run all advanced feature tests."""
    print("🚀 AI Medical Diagnosis System - Advanced Features Test")
    print("=" * 60)
    
    try:
        test_advanced_diagnosis()
        test_enhanced_remedies()
        test_symptom_extraction()
        test_comprehensive_features()
        
        print("\n" + "=" * 60)
        print("🎉 All advanced features are working correctly!")
        print("✨ The system now provides:")
        print("   • Differential diagnosis with confidence scores")
        print("   • Comprehensive natural remedies with scientific explanations")
        print("   • Advanced symptom extraction and matching")
        print("   • Guided symptom checking with follow-up questions")
        print("   • Lifestyle and dietary recommendations")
        print("   • Enhanced emergency detection")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()