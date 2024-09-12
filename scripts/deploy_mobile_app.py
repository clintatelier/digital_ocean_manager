import os
import subprocess
import platform
from gather_deployment_info import gather_and_output_info

def build_android_app(app_name):
    os.chdir(f"../mobile_apps/{app_name}")
    
    # Install dependencies
    subprocess.run(["npm", "install"], check=True)
    
    # Build Android app
    subprocess.run(["./gradlew", "assembleRelease"], check=True)
    
    print(f"Android APK built for {app_name}")
    print(f"APK location: ./android/app/build/outputs/apk/release/{app_name}-release.apk")

def build_ios_app(app_name):
    if platform.system() != "Darwin":
        print("iOS builds can only be performed on macOS")
        return

    os.chdir(f"../mobile_apps/{app_name}")
    
    # Install dependencies
    subprocess.run(["npm", "install"], check=True)
    
    # Build iOS app
    subprocess.run(["xcodebuild", "-workspace", f"ios/{app_name}.xcworkspace", "-scheme", app_name, "-configuration", "Release", "-archivePath", f"{app_name}.xcarchive", "archive"], check=True)
    
    print(f"iOS app archived for {app_name}")
    print(f"Archive location: ./{app_name}.xcarchive")

def prepare_for_distribution(app_name, platform):
    if platform.lower() == "android":
        print("\nTo distribute your Android app:")
        print("1. Sign your APK using your release key")
        print("2. Upload the signed APK to the Google Play Console")
        print("3. Follow the Google Play Console prompts to publish your app")
    elif platform.lower() == "ios":
        print("\nTo distribute your iOS app:")
        print("1. Open Xcode and select 'Archive' from the 'Product' menu")
        print("2. Click 'Distribute App' in the Archives organizer")
        print("3. Follow the prompts to upload your app to the App Store")
    else:
        print(f"Unknown platform: {platform}")

def deploy_mobile_app(app_name, platform):
    try:
        if platform.lower() == "android":
            build_android_app(app_name)
        elif platform.lower() == "ios":
            build_ios_app(app_name)
        else:
            raise ValueError(f"Unknown platform: {platform}")

        prepare_for_distribution(app_name, platform)

        print(f"\nMobile app {app_name} for {platform} has been built and is ready for distribution")

        # Gather and output deployment information
        output_file = gather_and_output_info(app_name, f"mobile_app_{platform.lower()}")
        print(f"Deployment information saved to {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error building mobile app: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    app_name = input("Enter the name of your mobile app: ")
    platform = input("Enter the target platform (android/ios): ")
    
    deploy_mobile_app(app_name, platform)