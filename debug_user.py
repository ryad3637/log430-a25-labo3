#!/usr/bin/env python3
"""
Debug script to test user creation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from orders.commands.write_user import add_user
from db import get_sqlalchemy_session

def test_user_creation():
    print("Testing user creation...")
    
    try:
        # Test database connection
        session = get_sqlalchemy_session()
        print("✅ Database connection successful")
        
        # Test user creation
        user_id = add_user("Test Debug User", "debug@test.com")
        print(f"✅ User created successfully with ID: {user_id}")
        
        session.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_user_creation()