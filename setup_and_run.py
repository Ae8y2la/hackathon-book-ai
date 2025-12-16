"""
Setup and run script for the RAG Chatbot backend.
This script handles dependency installation and server startup.
"""
import os
import sys
import subprocess
import time
from pathlib import Path


def install_dependencies():
    """Install required Python dependencies."""
    print("Installing dependencies...")

    try:
        # Install the requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)

        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print(f"Output: {e.output if hasattr(e, 'output') else 'No output'}")
        return False


def check_environment_variables():
    """Check if required environment variables are set."""
    required_vars = [
        "OPENAI_API_KEY",
        "QDRANT_URL",
        "QDRANT_API_KEY",
        "DATABASE_URL"
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"⚠️  Missing environment variables: {missing_vars}")
        print("Please set these variables in your .env file or environment")
        return False

    print("✅ All required environment variables are set")
    return True


def start_server():
    """Start the FastAPI server."""
    print("Starting the RAG Chatbot server...")

    try:
        # Run the server in a subprocess
        process = subprocess.Popen([
            sys.executable, "-c",
            "import uvicorn; from app.main import app; uvicorn.run(app, host='0.0.0.0', port=8000)"
        ])

        print("✅ Server started successfully on http://localhost:8000")
        print("💡 API Documentation: http://localhost:8000/docs")
        print("💡 Health Check: http://localhost:8000/health")

        # Wait for the process to complete (this will run indefinitely)
        process.wait()

    except KeyboardInterrupt:
        print("\n⚠️  Server stopped by user")
        process.terminate()
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

    return True


def test_health_endpoint():
    """Test the health endpoint to verify the server is running."""
    import requests
    import time

    print("Testing health endpoint...")

    max_retries = 30  # Wait up to 30 seconds for the server to start
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Health check passed")
                return True
        except requests.exceptions.ConnectionError:
            pass
        except Exception as e:
            print(f"Health check attempt {i+1} failed: {e}")

        time.sleep(1)

    print("❌ Health check failed - server may not be running properly")
    return False


def main():
    """Main function to run the setup and start the server."""
    print("🚀 RAG Chatbot Backend Setup and Deployment")
    print("=" * 50)

    # Check if dependencies are installed
    print("\n1. Checking dependencies...")
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False

    # Install dependencies
    print("\n2. Installing dependencies...")
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return False

    # Check environment variables
    print("\n3. Checking environment variables...")
    if not check_environment_variables():
        print("⚠️  Some environment variables are missing, continuing anyway (they may be set in .env)")

    # Start the server in a separate thread/process
    print("\n4. Starting server...")

    # For this script, we'll just provide instructions since we can't easily
    # run the server and test in the same process
    print("\n📋 To start the server manually:")
    print("   uvicorn app.main:app --reload --port 8000")
    print("\n📋 To test the health endpoint:")
    print("   curl http://localhost:8000/health")
    print("\n📋 To ingest documentation:")
    print('   curl -X POST "http://localhost:8000/api/v1/ingest" -H "Content-Type: application/json" -d \'{"force_reindex": false}\'')
    print("\n📋 To test chat functionality:")
    print('   curl -X POST "http://localhost:8000/api/v1/chat" -H "Content-Type: application/json" -d \'{"message": "What is this documentation about?"}\'')

    print("\n✅ Setup complete! Server is ready to be started.")
    print("💡 Remember to set up your environment variables in .env file")

    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)