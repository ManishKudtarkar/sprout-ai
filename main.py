#!/usr/bin/env python3
"""
AI Medical Diagnosis System - Main Entry Point

A natural remedy-focused medical diagnosis system that provides
preliminary health assessments and suggests natural remedies.
Enhanced with advanced diagnosis and comprehensive treatment plans.

Usage:
    python main.py
    python main.py "I have fever and headache"
    python main.py --advanced "I have fever and headache"
"""

import sys
import json
import argparse
from ai_engine import analyze_symptoms, advanced_analyze_symptoms


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


def format_advanced_output(result):
    """Format advanced analysis result for display."""
    output = []
    
    if result["type"] == "emergency":
        output.append("🚨 MEDICAL EMERGENCY DETECTED 🚨")
        output.append(f"Condition: {result['emergency'].get('suspected_condition', 'Critical')}")
        output.append(f"Urgency: {result['emergency']['level'].upper()}")
        output.append(f"Action Required: {result['emergency']['message']}")
        
        if result.get('emergency_remedies'):
            emergency_remedies = result['emergency_remedies']
            if emergency_remedies.get('immediate_actions'):
                output.append("\nIMMEDIATE ACTIONS:")
                for action in emergency_remedies['immediate_actions']:
                    output.append(f"• {action}")
                output.append(f"\n⚠️ {emergency_remedies.get('warning', '')}")
        
        return "\n".join(output)
    
    elif result["type"] == "unknown":
        output.append("🤔 ANALYSIS RESULT")
        output.append(result['message'])
        
        if result.get('extracted_symptoms'):
            output.append(f"\nSymptoms detected: {', '.join(result['extracted_symptoms'])}")
        
        if result.get('suggestions'):
            output.append("\nCommon symptoms I can analyze:")
            for suggestion in result['suggestions']:
                output.append(f"• {suggestion}")
        
        return "\n".join(output)
    
    elif result["type"] == "advanced_diagnosis":
        # Primary diagnosis
        primary = result['primary_diagnosis']
        output.append("🔬 ADVANCED MEDICAL ANALYSIS")
        output.append("=" * 50)
        output.append(f"Primary Diagnosis: {primary['condition'].title()}")
        output.append(f"Confidence Level: {primary['confidence'].title()}")
        
        if 'score' in primary:
            output.append(f"Confidence Score: {primary['score']:.1%}")
        
        # Matching symptoms
        if primary.get('matching_symptoms'):
            output.append(f"Matching Symptoms: {', '.join(primary['matching_symptoms'])}")
        
        output.append("")
        
        # Differential diagnosis
        if result.get('differential_diagnosis'):
            output.append("🔍 ALTERNATIVE POSSIBILITIES")
            for i, alt_diagnosis in enumerate(result['differential_diagnosis'][:3], 1):
                output.append(f"{i}. {alt_diagnosis['disease'].title()} (confidence: {alt_diagnosis['confidence']})")
            output.append("")
        
        # Treatment plan
        treatment = result.get('treatment_plan', {})
        
        # Natural remedies
        if treatment.get('natural_remedies'):
            output.append("🌿 RECOMMENDED NATURAL REMEDIES")
            for i, remedy in enumerate(treatment['natural_remedies'][:3], 1):
                output.append(f"{i}. {remedy['remedy']}")
                output.append(f"   • Benefit: {remedy['benefit']}")
                output.append(f"   • How it works: {remedy['explanation']}")
                if 'usage' in remedy:
                    output.append(f"   • Usage: {remedy['usage']}")
                output.append("")
        
        # Lifestyle recommendations
        if treatment.get('lifestyle_recommendations'):
            output.append("🏃 LIFESTYLE RECOMMENDATIONS")
            for rec in treatment['lifestyle_recommendations']:
                output.append(f"• {rec}")
            output.append("")
        
        # Dietary recommendations
        if treatment.get('dietary_recommendations'):
            dietary = treatment['dietary_recommendations']
            if dietary.get('foods_to_include'):
                output.append("🥗 FOODS TO INCLUDE")
                output.append(f"• {', '.join(dietary['foods_to_include'])}")
                output.append("")
            if dietary.get('foods_to_avoid'):
                output.append("🚫 FOODS TO AVOID")
                output.append(f"• {', '.join(dietary['foods_to_avoid'])}")
                output.append("")
        
        # Medical precautions
        if treatment.get('medical_precautions'):
            output.append("⚠️  IMPORTANT PRECAUTIONS")
            for precaution in treatment['medical_precautions']:
                output.append(f"• {precaution}")
            output.append("")
        
        # Analysis summary
        output.append(f"📊 ANALYSIS SUMMARY")
        output.append(f"Total symptoms analyzed: {result.get('total_symptoms_analyzed', 0)}")
        output.append("")
        
        # Disclaimer
        output.append("⚠️  DISCLAIMER")
        output.append(result["disclaimer"])
    
    return "\n".join(output)


def interactive_mode():
    """Run the system in interactive mode."""
    print("🏥 AI Medical Diagnosis System (Enhanced)")
    print("=" * 50)
    print("Choose your analysis mode:")
    print("1. Simple mode - Basic symptom analysis")
    print("2. Advanced mode - Detailed differential diagnosis")
    print()
    
    while True:
        try:
            mode_choice = input("Select mode (1/2) or 'quit' to exit: ").strip()
            
            if mode_choice.lower() in ['quit', 'exit', 'q']:
                print("Thank you for using the AI Medical Diagnosis System!")
                break
            
            if mode_choice not in ['1', '2']:
                print("Please enter 1 for simple mode or 2 for advanced mode.")
                continue
            
            advanced_mode = (mode_choice == '2')
            mode_name = "Advanced" if advanced_mode else "Simple"
            
            print(f"\n🔬 {mode_name} Analysis Mode")
            print("Enter your symptoms (or 'back' to change mode):")
            
            while True:
                symptoms = input("Symptoms: ").strip()
                
                if symptoms.lower() == 'back':
                    break
                
                if symptoms.lower() in ['quit', 'exit', 'q']:
                    print("Thank you for using the AI Medical Diagnosis System!")
                    return
                
                if not symptoms:
                    print("Please enter your symptoms.")
                    continue
                
                # Analyze symptoms
                if advanced_mode:
                    result = advanced_analyze_symptoms(symptoms)
                    formatted_output = format_advanced_output(result)
                else:
                    result = analyze_symptoms(symptoms)
                    formatted_output = format_output(result)
                
                # Display results
                print("\n" + "=" * 60)
                print(formatted_output)
                print("=" * 60)
                print()
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='AI Medical Diagnosis System')
    parser.add_argument('symptoms', nargs='*', help='Symptoms to analyze')
    parser.add_argument('--advanced', '-a', action='store_true', 
                       help='Use advanced analysis with differential diagnosis')
    
    args = parser.parse_args()
    
    if args.symptoms:
        # Command line mode
        symptoms = " ".join(args.symptoms)
        
        if args.advanced:
            result = advanced_analyze_symptoms(symptoms)
            print(format_advanced_output(result))
        else:
            result = analyze_symptoms(symptoms)
            print(format_output(result))
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()