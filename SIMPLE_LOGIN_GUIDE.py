"""
L.I.F.E. Platform Login Guide - Simple Steps
How to actually access your own platform (no fluff!)
"""

def show_simple_login_steps():
    """Show straightforward login steps"""
    
    print("🔑 HOW TO LOGIN TO YOUR L.I.F.E. PLATFORM")
    print("=" * 50)
    
    print("\n💻 METHOD 1: Local Development Access")
    print("-" * 35)
    print("1. Open command prompt in your project folder")
    print("2. Run: python azure_config.py")
    print("3. Open browser to: http://localhost:7071")
    print("   (Should auto-open)")
    
    print("\n🌐 METHOD 2: Direct Domain Access") 
    print("-" * 30)
    print("1. Go to: https://lifecoach-121.com")
    print("2. Use your Azure credentials to login")
    print("3. If it asks for authentication, use your Microsoft account")
    
    print("\n🔷 METHOD 3: Azure Portal Route")
    print("-" * 25)
    print("1. Go to: https://portal.azure.com")
    print("2. Login with your Microsoft account")
    print("3. Search for: life-platform-rg (your resource group)")
    print("4. Look for your deployed resources")
    print("5. Click on any App Service to get the URL")
    
    print("\n🚨 TROUBLESHOOTING:")
    print("-" * 20)
    print("❌ If localhost doesn't work:")
    print("   → Run: pip install -r requirements.txt")
    print("   → Then: python azure_config.py")
    
    print("❌ If domain doesn't work:")
    print("   → Check your Azure subscription is active")
    print("   → Verify you're logged into the right Microsoft account")
    
    print("❌ If nothing works:")
    print("   → The platform might not be deployed yet")
    print("   → You might need to run: azd up")
    
    print("\n🤔 REALISTIC CHECK:")
    print("-" * 18)
    print("Is your platform actually deployed and running?")
    print("Or are we still in development mode?")
    
    print("\n💡 QUICK TEST:")
    print("-" * 12)
    print("Let's start simple - try running this first:")
    print("→ python PLATFORM_ACCESS_GUIDE.py")
    print("→ It should show you what's actually available")

if __name__ == "__main__":
    show_simple_login_steps()