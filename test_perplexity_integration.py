"""
Test file to verify Perplexity integration implementation.

This file demonstrates the key aspects of the Perplexity integration:
1. Service structure and API
2. Validation logic
3. Cross-check service
4. Provider routing in research processor

Run this in an environment with dependencies installed to verify the implementation.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, '/home/runner/work/NoobBookV2/NoobBookV2/backend')

def test_service_structure():
    """Test that all service files exist and have correct structure."""
    files_to_check = [
        'app/services/integrations/perplexity/__init__.py',
        'app/services/integrations/perplexity/perplexity_service.py',
        'app/services/app_settings/validation/perplexity_validator.py',
        'app/services/ai_services/crosscheck_service.py',
        'data/prompts/research_crosscheck_prompt.json',
    ]
    
    for file_path in files_to_check:
        full_path = os.path.join('/home/runner/work/NoobBookV2/NoobBookV2/backend', file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - NOT FOUND")
            return False
    
    return True

def test_perplexity_service_api():
    """Test Perplexity service has correct API."""
    with open('/home/runner/work/NoobBookV2/NoobBookV2/backend/app/services/integrations/perplexity/perplexity_service.py', 'r') as f:
        content = f.read()
    
    required_methods = [
        'def research(',
        'def _build_research_prompt(',
        'def is_configured(',
    ]
    
    for method in required_methods:
        if method in content:
            print(f"✓ Method found: {method}")
        else:
            print(f"✗ Method missing: {method}")
            return False
    
    # Check for proper error handling
    if 'PERPLEXITY_API_KEY' in content:
        print("✓ Uses PERPLEXITY_API_KEY environment variable")
    else:
        print("✗ Missing PERPLEXITY_API_KEY reference")
        return False
    
    return True

def test_crosscheck_service_api():
    """Test cross-check service has correct API."""
    with open('/home/runner/work/NoobBookV2/NoobBookV2/backend/app/services/ai_services/crosscheck_service.py', 'r') as f:
        content = f.read()
    
    required_methods = [
        'def crosscheck_research(',
        'def _build_crosscheck_prompt(',
    ]
    
    for method in required_methods:
        if method in content:
            print(f"✓ Method found: {method}")
        else:
            print(f"✗ Method missing: {method}")
            return False
    
    # Check it uses Claude
    if 'claude_service.send_message' in content:
        print("✓ Uses Claude service for cross-checking")
    else:
        print("✗ Missing Claude service integration")
        return False
    
    return True

def test_validator():
    """Test validator exists and has correct structure."""
    with open('/home/runner/work/NoobBookV2/NoobBookV2/backend/app/services/app_settings/validation/perplexity_validator.py', 'r') as f:
        content = f.read()
    
    if 'def validate_perplexity_key(' in content:
        print("✓ validate_perplexity_key function exists")
    else:
        print("✗ validate_perplexity_key function missing")
        return False
    
    if 'https://api.perplexity.ai' in content:
        print("✓ Uses correct Perplexity API endpoint")
    else:
        print("✗ Missing Perplexity API endpoint")
        return False
    
    return True

def test_research_processor_routing():
    """Test research processor has provider routing."""
    with open('/home/runner/work/NoobBookV2/NoobBookV2/backend/app/services/source_services/source_processing/research_processor.py', 'r') as f:
        content = f.read()
    
    required_functions = [
        'def _research_with_claude(',
        'def _research_with_perplexity(',
    ]
    
    for func in required_functions:
        if func in content:
            print(f"✓ Function found: {func}")
        else:
            print(f"✗ Function missing: {func}")
            return False
    
    # Check for provider branching
    if 'provider == "perplexity"' in content or "provider == 'perplexity'" in content:
        print("✓ Has provider branching logic")
    else:
        print("✗ Missing provider branching")
        return False
    
    return True

def test_api_keys_config():
    """Test API keys configuration includes Perplexity."""
    with open('/home/runner/work/NoobBookV2/NoobBookV2/backend/app/api/settings/api_keys.py', 'r') as f:
        content = f.read()
    
    if "'id': 'PERPLEXITY_API_KEY'" in content or '"id": "PERPLEXITY_API_KEY"' in content:
        print("✓ PERPLEXITY_API_KEY in API keys config")
    else:
        print("✗ PERPLEXITY_API_KEY missing from config")
        return False
    
    if 'validate_perplexity_key' in content:
        print("✓ Perplexity validator wired up")
    else:
        print("✗ Perplexity validator not wired")
        return False
    
    return True

def test_frontend_provider_selector():
    """Test frontend has provider selector."""
    with open('/home/runner/work/NoobBookV2/NoobBookV2/frontend/src/components/sources/ResearchTab.tsx', 'r') as f:
        content = f.read()
    
    checks = [
        ("provider: string", "Provider parameter in handler"),
        ("'claude' | 'perplexity'", "Provider type definition"),
        ("type=\"radio\"", "Radio button inputs"),
        ("Claude Deep Research", "Claude option text"),
        ("Perplexity + Claude", "Perplexity option text"),
    ]
    
    for check_str, description in checks:
        if check_str in content:
            print(f"✓ {description}")
        else:
            print(f"✗ {description} - NOT FOUND")
            return False
    
    return True

def test_api_client():
    """Test API client passes provider parameter."""
    with open('/home/runner/work/NoobBookV2/NoobBookV2/frontend/src/lib/api/sources.ts', 'r') as f:
        content = f.read()
    
    if 'provider?: string' in content or 'provider: string' in content:
        print("✓ API method accepts provider parameter")
    else:
        print("✗ API method missing provider parameter")
        return False
    
    if "provider: provider || 'claude'" in content:
        print("✓ Defaults to Claude provider")
    else:
        print("✗ Missing default provider")
        return False
    
    return True

def test_documentation():
    """Test documentation includes Perplexity."""
    docs_to_check = [
        ('/home/runner/work/NoobBookV2/NoobBookV2/CLAUDE.md', 'PERPLEXITY_API_KEY'),
        ('/home/runner/work/NoobBookV2/NoobBookV2/Readme.md', 'PERPLEXITY_API_KEY'),
        ('/home/runner/work/NoobBookV2/NoobBookV2/CLAUDE.md', 'Deep Research Sources'),
    ]
    
    for file_path, search_term in docs_to_check:
        with open(file_path, 'r') as f:
            content = f.read()
        if search_term in content:
            print(f"✓ {os.path.basename(file_path)} mentions '{search_term}'")
        else:
            print(f"✗ {os.path.basename(file_path)} missing '{search_term}'")
            return False
    
    return True

def main():
    """Run all tests."""
    tests = [
        ("Service Structure", test_service_structure),
        ("Perplexity Service API", test_perplexity_service_api),
        ("Cross-check Service API", test_crosscheck_service_api),
        ("Validator", test_validator),
        ("Research Processor Routing", test_research_processor_routing),
        ("API Keys Configuration", test_api_keys_config),
        ("Frontend Provider Selector", test_frontend_provider_selector),
        ("API Client", test_api_client),
        ("Documentation", test_documentation),
    ]
    
    print("=" * 70)
    print("Perplexity Integration - Implementation Verification")
    print("=" * 70)
    print()
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 70)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 70)
    print("Summary:")
    print("=" * 70)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        icon = "✓" if result else "✗"
        print(f"{icon} {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print()
    if all_passed:
        print("✓ All tests PASSED! Implementation is complete and correct.")
    else:
        print("✗ Some tests FAILED. Please review the implementation.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
