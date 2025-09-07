"""
Test client for WordSmith Backend API
Run this to test your backend API
"""
import requests
import json
import time

API_BASE_URL = "http://localhost:8000/api/v1"

def test_health_check():
    """Test health check endpoint."""
    print("🏥 Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    print("-" * 50)

def test_transformations_list():
    """Test getting available transformations."""
    print("📋 Testing transformations list...")
    try:
        response = requests.get(f"{API_BASE_URL}/transformations")
        if response.status_code == 200:
            print("✅ Transformations list retrieved!")
            data = response.json()
            print(f"Available transformations: {data['total_count']}")
            for key, value in data['transformations'].items():
                print(f"  • {value['name']} ({value['icon']}) - {value['description']}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print("-" * 50)

def test_text_transformation():
    """Test text transformation endpoint."""
    print("🔄 Testing text transformation...")
    
    test_cases = [
        {
            "text": "hey there how r u doing today",
            "transformation_type": "grammar_fix",
            "additional_instructions": "Make it professional"
        },
        {
            "text": "Please review the attached document and provide feedback at your earliest convenience.",
            "transformation_type": "friendly",
            "additional_instructions": None
        },
        {
            "text": "This is a very long sentence that contains a lot of information and details that could potentially be made shorter and more concise for better readability.",
            "transformation_type": "shorten",
            "additional_instructions": None
        },
        {
            "text": "Great news!",
            "transformation_type": "emoji",
            "additional_instructions": None
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['transformation_type']}")
        print(f"Original: {test_case['text']}")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/transform",
                json=test_case
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Transformed: {result['transformed_text']}")
                print(f"⏱️ Processing time: {result['processing_time']}s")
                print(f"📊 Words: {result['word_count_original']} → {result['word_count_transformed']}")
            else:
                print(f"❌ Failed with status: {response.status_code}")
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(1)  # Small delay between requests
    
    print("-" * 50)

def test_batch_transformation():
    """Test batch transformation endpoint."""
    print("📦 Testing batch transformation...")
    
    batch_request = {
        "texts": [
            "hello world",
            "how are u",
            "thanks alot"
        ],
        "transformation_type": "grammar_fix",
        "additional_instructions": "Make them professional"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/batch-transform",
            json=batch_request
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Batch transformation completed!")
            print(f"⏱️ Total processing time: {result['total_processing_time']}s")
            print(f"✅ Successful: {result['successful_transformations']}")
            print(f"❌ Failed: {result['failed_transformations']}")
            
            for i, res in enumerate(result['results'], 1):
                print(f"\nResult {i}:")
                print(f"  Original: {res['original_text']}")
                print(f"  Transformed: {res['transformed_text']}")
                
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("-" * 50)

def test_cache_stats():
    """Test cache statistics endpoint."""
    print("💾 Testing cache statistics...")
    try:
        response = requests.get(f"{API_BASE_URL}/cache/stats")
        if response.status_code == 200:
            print("✅ Cache stats retrieved!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print("-" * 50)

def main():
    """Run all tests."""
    print("🧪 WordSmith Backend API Test Suite")
    print("=" * 50)
    
    # Run tests
    test_health_check()
    test_transformations_list()
    test_text_transformation()
    test_batch_transformation()
    test_cache_stats()
    
    print("🎉 All tests completed!")
    print("\n💡 Tips:")
    print("- Check http://localhost:8000/docs for interactive API documentation")
    print("- Monitor the server logs for detailed information")
    print("- Use the cache endpoints to manage memory usage")

if __name__ == "__main__":
    main()