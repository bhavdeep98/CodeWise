import os
import pandas as pd
from googletrans import Translator
from googlesearch import search

class DataExtractor:
    def __init__(self, directory, translator):
        self.directory = directory
        self.translator = translator

    def extract_data(self):
        data = []

        for root, subdirs, files in os.walk(self.directory):
            tag = os.path.basename(root)

            for subdir in subdirs:
                key = subdir
                code_file, readme_file = self.find_files(root, subdir, files)

                if code_file and readme_file:
                    code_content, extension = self.extract_code_content(code_file)
                    readme_content = self.translate_readme(readme_file)
                    data.append({
                        'tags': tag,
                        'key': key,
                        'code_content': code_content,
                        'extension': extension,
                        'readme': readme_content
                    })

        return pd.DataFrame(data)

    def find_files(self, root, subdir, files):
        code_file = None
        readme_file = None

        for file in files:
            if file.endswith(('.cpp', '.py', '.java')):
                code_file = os.path.join(root, subdir, file)
                break
            elif file.lower() == 'readme.md':
                readme_file = os.path.join(root, subdir, file)

        return code_file, readme_file

    def extract_code_content(self, code_file):
        with open(code_file, 'r') as f:
            code_content = f.read()
            extension = os.path.splitext(code_file)[1]
        return code_content, extension

    def find_leetcode_link(self, key):
        for result in search(key + " leetcode.com", tld="com", lang="en", num=5, stop=5, pause=2):  # Adjust search parameters as needed
            if "leetcode.com" in result:
                return result
        return None  # Return None if no relevant link found

    def translate_readme(self, readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            readme_content = f.read()
            return self.translator.translate(readme_content, src='zh-cn', dest='en').text



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Example usage:
    directory = './LeetCode'
    translator = Translator()
    extractor = DataExtractor(directory, translator)
    df = extractor.extract_data()
    print(df.head())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
