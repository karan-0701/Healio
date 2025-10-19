import os
import shutil
import zipfile
import subprocess
import sys


def main():
    print("Creating Lambda deployment package...")

    # Clean up
    if os.path.exists("lambda-package"):
        shutil.rmtree("lambda-package")
    if os.path.exists("lambda-deployment.zip"):
        os.remove("lambda-deployment.zip")

    # Create package directory
    os.makedirs("lambda-package")

    # Install dependencies using Docker with Lambda runtime image
    print("Installing dependencies for Lambda runtime...")
    
    try:
        subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{os.getcwd()}:/var/task",
                "--platform",
                "linux/amd64",
                "--entrypoint",
                "/bin/bash",
                "public.ecr.aws/lambda/python:3.12",
                "-c",
                "pip install -r /var/task/requirements.txt --target /var/task/lambda-package --upgrade --no-cache-dir",
            ],
            check=True,
            capture_output=True,
            text=True
        )
        print("✓ Dependencies installed successfully")
        
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install dependencies")
        print(f"Error: {e.stderr}")
        sys.exit(1)

    # Copy application files
    print("Copying application files...")
    app_files = ["server.py", "lambda_handler.py", "context.py", "resources.py"]
    for file in app_files:
        if os.path.exists(file):
            shutil.copy2(file, "lambda-package/")
        else:
            print(f"⚠ {file} not found, skipping")
    
    # Copy data directory
    if os.path.exists("data"):
        shutil.copytree("data", "lambda-package/data")

    # Create zip
    print("Creating zip file...")
    with zipfile.ZipFile("lambda-deployment.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("lambda-package"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "lambda-package")
                zipf.write(file_path, arcname)
                
    # Show package size
    size_mb = os.path.getsize("lambda-deployment.zip") / (1024 * 1024)
    print(f"\n✓ Created lambda-deployment.zip ({size_mb:.2f} MB)")
    
    # Size warnings
    if size_mb > 250:
        print("❌ ERROR: Unzipped package will exceed 250 MB Lambda limit!")
        print("   Consider using Lambda Layers or removing unused dependencies")
    elif size_mb > 50:
        print("⚠ WARNING: Package exceeds 50 MB")
        print("   You must upload to S3 instead of direct upload")
    
    print("\nDeployment package ready. Handler: lambda_handler.handler")


if __name__ == "__main__":
    main()