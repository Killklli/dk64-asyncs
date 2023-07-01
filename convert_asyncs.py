import os
import base64
import zipfile
import io
import json

# Iterate over the lanky files in the asyncs directory
for filename in os.listdir('asyncs'):
    if filename.endswith('.lanky'):
        print('Converting ' + filename)
        # Read the encoded zip file
        with open('asyncs/' + filename, 'r') as f:
            encoded_zip = f.read().encode('utf8')

        # Decode the base64-encoded zip
        decoded_zip = base64.b64decode(encoded_zip)

        # Read the decoded zip file as a zip archive
        with zipfile.ZipFile(io.BytesIO(decoded_zip), 'r') as existing_zip:
            # Read the spoiler_log file from the zip
            spoiler_log = existing_zip.read('spoiler_log')
            
            # Load the JSON from the decoded spoiler_log
            loaded_json = json.loads(spoiler_log)

            # Remove all sections not named "Settings"
            settings = loaded_json['Settings']
            converted = {'Settings': settings, "Cosmetics": {}}
            modified_log = json.dumps(converted)
            # Write the spoiler_log to a file
            truncated_filename = filename.split('.')[0]
            with open('asyncs/' + truncated_filename + '-spoiler.json', 'w') as f:
                f.write(json.dumps(loaded_json, indent=4))
            # Create a new zip file to store the modified content
            modified_zip_file = zipfile.ZipFile('asyncs/' + filename + '.modified', 'w')

            # Add the modified JSON as the new spoiler_log in the zip file
            modified_zip_file.writestr('spoiler_log', modified_log)

            # Add all other files from the existing zip to the modified zip
            for file_info in existing_zip.infolist():
                if file_info.filename != 'spoiler_log':
                    file_data = existing_zip.read(file_info.filename)
                    modified_zip_file.writestr(file_info, file_data)

            # Close the modified zip file
            modified_zip_file.close()

        # Encode the modified zip as base64
        encoded_modified_zip = base64.b64encode(open('asyncs/' + filename + '.modified', 'rb').read())
        # Delete the modified zip file
        os.remove('asyncs/' + filename + '.modified')
        # Write the encoded zip to a file
        with open('asyncs/' + filename, 'wb') as f:
            f.write(encoded_modified_zip)
