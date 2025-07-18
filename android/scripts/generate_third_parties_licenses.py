import os
import sys
import zipfile

MODULE_NAME = sys.argv[1]
INCLUDE_AAR_METADATA = len(sys.argv) > 2 and sys.argv[2].lower() == "true"

# Move to project root
os.chdir("../")

print("|---> 🧠 GENERATING THIRD PARTIES LICENSE FILE FOR MODULE {MODULE_NAME}...")

# Generate license report
os.system("./gradlew generateLicenseReport")

# Paths
unziped_dir = f"{MODULE_NAME}/build/outputs/aar/unziped"
aar_output_dir = f"{MODULE_NAME}/build/outputs/aar"
third_party_license_src = f"{MODULE_NAME}/build/licenses/licenses.json"
third_party_license_dst = os.path.join(unziped_dir, "THIRD_PARTY_LICENSES.txt")
license_src = "LICENSE.txt"
license_dst = os.path.join(unziped_dir, "LICENSE.txt")
aar_output_path = os.path.join(aar_output_dir, f"{MODULE_NAME}-release.aar")

# Copy license files
os.system(f"cp {third_party_license_src} {third_party_license_dst}")
os.system(f"cp {license_src} {license_dst}")

print("|---> ✅ LICENSE.txt and THIRD_PARTY_LICENSES.txt ready for aar release.")

# Zip the contents of 'unziped' into the final AAR
def zip_folder(source_folder, output_zip):
    source_folder = os.path.abspath(source_folder)
    output_zip = os.path.abspath(output_zip)

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_folder):
            for file in files:
                if file == "aar-metadata.properties" and not INCLUDE_AAR_METADATA:
                    continue
                abs_file = os.path.join(root, file)
                rel_path = os.path.relpath(abs_file, source_folder)
                zipf.write(abs_file, arcname=rel_path)

    print(f"|---> ✅ Zipped AAR to: {output_zip}")

print("|---> Zipping AAR contents...")
zip_folder(unziped_dir, aar_output_path)
