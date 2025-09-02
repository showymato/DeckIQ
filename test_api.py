import os
import google.generativeai as genai

def test_gemini_api():
    """Test script to verify your Gemini API key works"""

    print("🧪 Testing Google Gemini API Connection")
    print("=" * 40)

    # Get API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        print("💡 Set it with: export GOOGLE_API_KEY='your_key_here'")
        return False

    print(f"🔑 API Key found: {api_key[:10]}...")

    try:
        # Configure Gemini
        genai.configure(api_key=api_key)

        # Try to list models
        print("📋 Checking available models...")
        models = list(genai.list_models())
        print(f"✅ Found {len(models)} available models")

        # Test with different models
        test_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"]

        for model_name in test_models:
            try:
                print(f"\n🤖 Testing {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Hello! Please respond with 'API Test Successful' if you receive this.")

                if response.text and "successful" in response.text.lower():
                    print(f"✅ {model_name}: WORKING")
                    print(f"📝 Response: {response.text[:50]}...")
                    return True
                else:
                    print(f"⚠️  {model_name}: Unexpected response")

            except Exception as e:
                print(f"❌ {model_name}: {str(e)}")

        print("\n❌ No models are working properly")
        return False

    except Exception as e:
        print(f"❌ API Configuration Error: {str(e)}")
        print("\n💡 Troubleshooting:")
        print("   1. Check your API key at: https://aistudio.google.com/")
        print("   2. Ensure Gemini API is enabled")
        print("   3. Verify no typos in the API key")
        return False

if __name__ == "__main__":
    success = test_gemini_api()

    print("\n" + "=" * 40)
    if success:
        print("🎉 API TEST PASSED! Your setup is working correctly.")
        print("🚀 You can now deploy the Pitch Deck Enhancer app.")
    else:
        print("🔧 API TEST FAILED. Please fix the issues above.")
        print("📞 Visit https://aistudio.google.com/ for help.")
    print("=" * 40)
