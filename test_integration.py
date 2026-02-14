#!/usr/bin/env python3
"""Validation script to verify the integration files."""

import json
import yaml
import ast
import os

def validate_files():
    """Validate all integration files."""
    print("🔍 Validating Tickets Event Integration Files\n")
    
    base_path = "custom_components/tickets_event"
    
    # Test 1: Check that all required files exist
    print("1. Checking required files...")
    required_files = [
        "__init__.py",
        "manifest.json",
        "services.yaml"
    ]
    
    for file in required_files:
        file_path = os.path.join(base_path, file)
        assert os.path.exists(file_path), f"Missing required file: {file_path}"
        print(f"   ✓ Found {file}")
    
    # Test 2: Validate manifest.json
    print("\n2. Validating manifest.json...")
    with open(os.path.join(base_path, "manifest.json")) as f:
        manifest = json.load(f)
    
    required_keys = ["domain", "name", "version", "documentation", "requirements", "codeowners"]
    for key in required_keys:
        assert key in manifest, f"Missing required key in manifest: {key}"
        print(f"   ✓ {key}: {manifest[key]}")
    
    assert manifest["domain"] == "tickets_event", "Domain should be 'tickets_event'"
    
    # Test 3: Validate services.yaml
    print("\n3. Validating services.yaml...")
    with open(os.path.join(base_path, "services.yaml")) as f:
        services = yaml.safe_load(f)
    
    assert "fire_event" in services, "Missing 'fire_event' service definition"
    service_def = services["fire_event"]
    assert "name" in service_def, "Service missing 'name' field"
    assert "description" in service_def, "Service missing 'description' field"
    assert "fields" in service_def, "Service missing 'fields' field"
    print(f"   ✓ Service definition looks good")
    
    # Validate service fields
    fields = service_def["fields"]
    required_fields = ["type", "ticket_id", "description", "priority"]
    for field in required_fields:
        assert field in fields, f"Missing field definition: {field}"
        print(f"   ✓ Field '{field}' defined")
    
    # Test 4: Validate Python syntax
    print("\n4. Validating Python syntax...")
    with open(os.path.join(base_path, "__init__.py")) as f:
        code = f.read()
    
    try:
        ast.parse(code)
        print("   ✓ Python syntax is valid")
    except SyntaxError as e:
        raise AssertionError(f"Python syntax error: {e}")
    
    # Test 5: Check for required code elements
    print("\n5. Checking code structure...")
    
    # Parse the AST to check for DOMAIN constant
    tree = ast.parse(code)
    domain_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "DOMAIN":
                    if isinstance(node.value, ast.Constant) and node.value.value == "tickets_event":
                        domain_found = True
                        break
    assert domain_found, "DOMAIN constant not properly defined"
    print("   ✓ DOMAIN constant defined correctly")
    
    assert "async def async_setup" in code, "Missing async_setup function"
    print("   ✓ async_setup function defined")
    
    assert "async def handle_ticket_event" in code, "Missing handle_ticket_event function"
    print("   ✓ handle_ticket_event function defined")
    
    assert "hass.services.async_register" in code, "Service not being registered"
    print("   ✓ Service registration code present")
    
    assert "hass.bus.async_fire" in code, "Event firing code not present"
    print("   ✓ Event firing code present")
    
    print("\n" + "="*50)
    print("✅ All validation checks passed!")
    print("="*50)
    print("\n📋 Integration Summary:")
    print(f"   Domain: {manifest['domain']}")
    print(f"   Name: {manifest['name']}")
    print(f"   Version: {manifest['version']}")
    print(f"   Service: {manifest['domain']}.fire_event")
    print(f"   Event Type: {manifest['domain']}_event")

if __name__ == "__main__":
    try:
        validate_files()
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        exit(1)
