#!/usr/bin/env python3
"""
AI Medical Diagnosis System - Main Entry Point

A natural remedy-focused medical diagnosis system that provides
preliminary health assessments and suggests natural remedies.

Usage:
    python main.py
    python main.py "I have fever and headache"
"""

import sys
import json
from ai_engine import analyze_symptoms


def format_output(result):
    """Format the analysis result for display."""
    output = []
    
    # Emergency check
    if result["emergency"]["emergency"]:
        output.append("🚨 EMERGENCY ALERT 🚨")
        output.append(f"Level: {result['emergency']['level'].upper()}")
        output.append(f"Message: {result['emergency']['message']}")
        output.append("=" * 50)
        return "\n".join(output)
    
    # Diagnosis
    if result["diagnosis"]:
        output.append("📋 DIAGNOSIS")
        output.append(f"Condition: {result['diagnosis']['condition'].title()}")
        output.append(f"Confidence: {result['diagnosis']['confidence'].title()}")
        if "message" in result["diagnosis"]:
            output.append(f"Note: {result['diagnosis']['message']}")
        output.append("")
    
    # Remedies
    if result["remedies"]:
        output.append("🌿 NATURAL REMEDIES")
        for i, remedy in enumerate(result["remedies"], 1):
            output.append(f"{i}. {remedy['remedy']}")
            output.append(f"   Benefit: {remedy['benefit']}")
            output.append(f"   How it works: {remedy['explanation']}")
            output.append("")
    
    # Precautions
    if result.get("precautions"):
        output.append("⚠️  PRECAUTIONS")
        for i, precaution in enumerate(result["precautions"], 1):
            output.append(f"{i}. {precaution}")
        output.append("")
    
    # Disclaimer
    output.append("⚠️  DISCLAIMER")
    output.append(result["disclaimer"])
    
    return "\n".join(output)


def interactive_mode():
    """Run the system in interactive mode."""
    print("🏥 AI Medical Diagnosis System")
    print("=" * 40)
    print("Enter your symptoms (or 'quit' to exit):")
    print()
    
    while True:
        try:
            symptoms = input("Symptoms: ").strip()
            
            if symptoms.lower() in ['quit', 'exit', 'q']:
                print("Thank you for using the AI Medical Diagnosis System!")
                break
            
            if not symptoms:
                print("Please enter your symptoms.")
                continue
            
            # Analyze symptoms
            result = analyze_symptoms(symptoms)
            
            # Display results
            print("\n" + "=" * 50)
            print(format_output(result))
            print("=" * 50)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main function."""
    if len(sys.argv) > 1:
        # Command line mode
        symptoms = " ".join(sys.argv[1:])
        result = analyze_symptoms(symptoms)
        print(format_output(result))
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()