#!/usr/bin/env python3
"""
Simple test script for the AI Medical Diagnosis System
"""

from ai_engine import analyze_symptoms


def test_emergency_detection():
    """Test emergency symptom detection."""
    print("Testing emergency detection...")
    result = analyze_symptoms("chest pain")
    assert result["emergency"]["emergency"] == True
    assert result["emergency"]["level"] == "critical"
    print("✓ Emergency detection works")


def test_normal_diagnosis():
    """Test normal symptom diagnosis."""
    print("Testing normal diagnosis...")
    result = analyze_symptoms("fever and body pain")
    assert result["diagnosis"]["condition"] == "viral infection"
    assert len(result["remedies"]) > 0
    assert result["emergency"]["emergency"] == False
    print("✓ Normal diagnosis works")


def test_throat_infection():
    """Test throat infection diagnosis."""
    print("Testing throat infection...")
    result = analyze_symptoms("sore throat")
    assert result["diagnosis"]["condition"] == "throat infection"
    assert len(result["remedies"]) > 0
    assert result["remedies"][0]["remedy"] == "Salt Water Gargle"
    print("✓ Throat infection diagnosis works")


def test_enhanced_diagnosis():
    """Test enhanced diagnosis with Kaggle data."""
    print("Testing enhanced diagnosis with Kaggle data...")
    result = analyze_symptoms("itching and skin rash")
    assert result["diagnosis"]["condition"] in ["impetigo", "fungal infection", "hepatitis b"]
    assert result["emergency"]["emergency"] == False
    print("✓ Enhanced diagnosis works")


def test_single_word_symptoms():
    """Test single-word symptom processing."""
    print("Testing single-word symptoms...")
    
    # Test headache
    result = analyze_symptoms("headache")
    assert result["diagnosis"]["condition"] == "stress or dehydration"
    assert result["emergency"]["emergency"] == False
    
    # Test fever
    result = analyze_symptoms("fever")
    assert result["diagnosis"]["condition"] == "viral infection"
    assert result["emergency"]["emergency"] == False
    
    # Test cough
    result = analyze_symptoms("cough")
    assert result["diagnosis"]["condition"] == "respiratory irritation"
    assert result["emergency"]["emergency"] == False
    
    print("✓ Single-word symptoms work correctly")


def main():
    """Run all tests."""
    print("🧪 Running AI Medical Diagnosis System Tests")
    print("=" * 50)
    
    try:
        test_emergency_detection()
        test_normal_diagnosis()
        test_throat_infection()
        test_enhanced_diagnosis()
        test_single_word_symptoms()
        
        print("=" * 50)
        print("✅ All tests passed!")
        
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())