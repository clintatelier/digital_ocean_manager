import os
import subprocess

def deploy_mobile_app(app_name, platform):
    # Change to the app directory
    os.chdir(f"../mobile_apps/{app_name}")

    # Install dependencies
    subprocess.run(["npm", "install"], check=True)

    if platform.lower() == "android":
        # Build Android app
        subprocess.run(["./gradlew", "assembleRelease"], check=True)
        print(f"Android APK built for {app_name}")
    elif platform.lower() == "ios":
        # Build iOS app
        subprocess.run(["xcodebuild", "-workspace", f"{app_name}.xcworkspace", "-scheme", f"{app_name}", "-configuration", "Release"], check=True)
        print(f"iOS app built for {app_name}")
    else:
        print("Invalid platform. Please choose 'android' or 'ios'.")

    print(f"Mobile app {app_name} built successfully for {platform}")
    print("Please distribute the app through the appropriate app store or testing platform.")

if __name__ == '__main__':
    app_name = input("Enter the name of your mobile app: ")
    platform = input("Enter the target platform (android/ios): ")
    deploy_mobile_app(app_name, platform)