import os
import pandas as pd
from googletrans import Translator
from googlesearch import search
import logging

class Logger:
    def __init__(self, filename='data_extractor.log', level=logging.DEBUG):
        self.logger = logging.getLogger(__name__)  # Get the logger for this module
        logging.basicConfig(filename=filename, level=level)  # Set up logging configuration
    def log_warning(self, message, exc_info=False):
        self.logger.warning(message, exc_info=exc_info)
    def log_error(self, message, exc_info=False):
        self.logger.error(message, exc_info=exc_info)

class DataExtractor:
    def __init__(self, directory, translator, logger=None):
        self.directory = directory
        self.translator = translator
        self.logger = logger
    def extract_data(self):
        data = []

        for root, subdirs, files in os.walk(self.directory):
            try:
                tag = os.path.basename(root)

                for subdir in subdirs:
                    key = subdir
                    code_file, readme_file = self.find_files(root, subdir, files)

                    if code_file and readme_file:
                        code_content, extension = self.extract_code_content(code_file)
                        readme_content = self.translate_readme(readme_file)
                        link = self.find_leetcode_link(key)
                        data.append({
                            'tags': tag,
                            'key': key,
                            'code_content': code_content,
                            'extension': extension,
                            'readme': readme_content,
                            'link': link
                        })
            except Exception as e:
                self.logger.log_error(f"Error processing directory: {root}", exc_info=True)
                return None  # Gracefully exit the function

        return pd.DataFrame(data)

    def find_files(self, root, subdir, files):
        try:
            code_file = None
            readme_file = None

            for file in files:
                if file.endswith(('.cpp', '.py', '.java')):
                    code_file = os.path.join(root, subdir, file)
                    break
                elif file.lower() == 'readme.md':
                    readme_file = os.path.join(root, subdir, file)

            if not code_file:
                self.logger.log_warning(f"No code file found in directory: {root}")
            if not readme_file:
                self.logger.log_warning(f"No README file found in directory: {root}")

            return code_file, readme_file
        except Exception as e:
            self.logger.log_error(f"Error finding files in directory: {root}", exc_info=True)
            return None, None  # Return None if errors occur

    # ... (other methods with logging)

    def extract_code_content(self, code_file):
        try:
            with open(code_file, 'r') as f:
                code_content = f.read()
                extension = os.path.splitext(code_file)[1]
            return code_content, extension
        except Exception as e:
            self.logger.log_error(f"Error reading code file: {code_file}", exc_info=True)
            return None, None

    def translate_readme(self, readme_file):
        try:
            with open(readme_file, 'r', encoding='utf-8') as f:
                readme_content = f.read()
                return self.translator.translate(readme_content, src='zh-cn', dest='en').text
        except Exception as e:
            self.logger.log_error(f"Error translating README file: {readme_file}", exc_info=True)
            return None

    def find_leetcode_link(self, key):
        try:
            for result in search(key + " leetcode.com", tld="com", lang="en", num=5, stop=5, pause=2):
                if "leetcode.com" in result:
                    return result
            self.logger.log_warning(f"No relevant LeetCode link found for key: {key}")
            return None
        except Exception as e:
            self.logger.log_error(f"Error searching for LeetCode link: {key}", exc_info=True)
            return None



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Create a logger instance (optional)
    logger = Logger(filename='CodeWise.log')


    directory = 'LeetCode'
    translator = Translator()


    try:
        extractor = DataExtractor(directory, translator, logger)  # Default logger will be used
        df = extractor.extract_data()
        if df is None:
            print("Data extraction failed due to errors. Check the log for details.")
        else:
            print(df.head())
    except Exception as e:
        print("Unexpected error occurred:", e)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
