import json
import os
import re
import warnings

from wapitiCore.net.crawler import Response
from wapitiCore.net.html import Html


class ApplicationDataException(Exception):
    """Raised when application data file is not properly formatted"""

    def __init__(self, message):
        message = "Application data file is not properly formatted : " + message
        super().__init__(message)


class ApplicationData:
    """
    Store application database.
    For instance https://raw.githubusercontent.com/wapiti-scanner/wappalyzer/master/src/technologies/.
    """

    def __init__(self, categories_file_path=None, groups_file_path=None, technologies_file_path=None):
        """
        Initialize a new ApplicationData object.
        """
        base_dir = os.path.join(os.getenv("HOME") or os.getenv("USERPROFILE"), ".wapiti")
        default_categories_file_path = os.path.join(base_dir, "wappalyzer", "data/categories.json")
        default_groups_file_path = os.path.join(base_dir, "wappalyzer", "data/groups.json")
        default_technologies_file_path = os.path.join(base_dir, "wappalyzer", "data/technologies.json")

        with open(categories_file_path or default_categories_file_path, 'r', encoding='utf-8') as categories_file:
            self.categories = json.load(categories_file)

        with open(groups_file_path or default_groups_file_path, 'r', encoding='utf-8') as groups_file:
            self.groups = json.load(groups_file)

        with open(technologies_file_path or default_technologies_file_path, 'r', encoding='utf-8') as technologies_file:
            self.applications = json.load(technologies_file)

        self.normalize_applications()

        # Ignore regex parsing warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.normalize_application_regex()

        self.normalize_categories()
        self.normalize_groups()

    def normalize_applications(self):
        """
        Ensure that each needed field is at least an empty element
        """
        for application_name in self.applications:

            for list_field in ["cats", "html", "implies", "scriptSrc"]:
                if list_field not in self.applications[application_name]:
                    # Complete with empty elements if not already present
                    self.applications[application_name][list_field] = []
                elif not isinstance(self.applications[application_name][list_field], list):
                    # Ensure to not iterate on a string value
                    self.applications[application_name][list_field] = [self.applications[application_name][list_field]]

            for dict_field in ["meta", "js", "cookies", "headers"]:
                if dict_field not in self.applications[application_name]:
                    # Complete with empty elements if not already present
                    self.applications[application_name][dict_field] = {}
                elif not isinstance(self.applications[application_name][dict_field], dict):
                    # Raise an exception if the provided field is not a dict
                    raise ApplicationDataException(
                        f"{dict_field} is not a dict in {self.applications[application_name]}"
                    )

                # Ensure keys are lowercase
                dict_items = self.applications[application_name][dict_field].items()
                self.applications[application_name][dict_field] = {key.lower(): value for (key, value) in dict_items}

            for string_field in ["url", "icon", "website", "cpe"]:
                if string_field not in self.applications[application_name]:
                    # Complete with empty elements if not already present
                    self.applications[application_name][string_field] = ""
                elif not isinstance(self.applications[application_name][string_field], str):
                    # Ensure to not evaluate a list or dict
                    self.applications[application_name][string_field] = str(
                        self.applications[application_name][string_field])

    def normalize_categories(self):
        """
        Ensure that at least each needed field exists
        """
        for category in self.categories:
            for field in ["name"]:
                if field not in self.categories[category]:
                    raise ApplicationDataException(f"{field} field is not in {self.categories[category]}")

    def normalize_groups(self):
        """
        Ensure that at least each needed field exists
        """
        for group in self.groups:
            for field in ["name"]:
                if field not in self.groups[group]:
                    raise ApplicationDataException(f"{field} field is not in {self.groups[group]}")

    def normalize_application_regex(self):
        """
        Format application regex provided in interesting fields
        """
        for application_name in self.applications:

            for list_field in ["html", "implies", "scriptSrc"]:
                self.applications[application_name][list_field] = [
                    self.normalize_regex(pattern) for pattern in self.applications[application_name][list_field]
                ]

            for dict_field in ["meta", "cookies", "headers"]:
                for (key, patterns) in self.applications[application_name][dict_field].items():
                    # Sometimes key is provided but pattern is empty
                    # However looking for key seems to be interesting
                    if patterns == "":
                        patterns = key

                    # {meta: {generator: "abc"}} --> {meta: {generator: ["abc"]}}
                    if not isinstance(patterns, list):
                        self.applications[application_name][dict_field][key] = [patterns]

                    for i, pattern in enumerate(self.applications[application_name][dict_field][key]):
                        self.applications[application_name][dict_field][key][i] = self.normalize_regex(pattern)

            for string_field in ["url"]:
                regex = self.applications[application_name][string_field]
                if regex != '':
                    self.applications[application_name][string_field] = self.normalize_regex(regex)

    @staticmethod
    def normalize_regex(pattern: str):
        """
        Return a dict containing version regex and application regex extracted from pattern string and compiled regex
        """
        regex_params = {}
        pattern = pattern.split("\\;")
        for i, expression in enumerate(pattern):
            if i == 0:
                regex_params["application_pattern"] = expression
                try:
                    regex_params['regex'] = re.compile(expression, re.I)
                except re.error as err:
                    warnings.warn(
                        f"Caught {err} while compiling regex: {pattern}")
                    # regex that never matches:
                    # http://stackoverflow.com/a/1845097/413622
                    regex_params['regex'] = re.compile(r'(?!x)x')
            else:
                splitted_param_pattern = expression.split(':')
                if len(splitted_param_pattern) > 1:
                    param = splitted_param_pattern.pop(0)
                    regex_params[param] = ':'.join(splitted_param_pattern)
        return regex_params

    def get_categories(self):
        """Provide normalized ApplicationData categories"""
        return self.categories

    def get_applications(self):
        """Provide normalized ApplicationData applications"""
        return self.applications

    def get_groups(self):
        """Provide normalized ApplicationData groups"""
        return self.groups


class Wappalyzer:
    """
    Python Wappalyzer driver.
    """

    def __init__(self, application_data: ApplicationData, web_content: Response):
        """
        Initialize a new Wappalyzer object.
        """
        self.applications = application_data.get_applications()
        self.categories = application_data.get_categories()
        self.groups = application_data.get_groups()

        self._url = web_content.url
        self._html_code = web_content.content
        # Copy some values to make sure they aren't processed more than once
        html = Html(self._html_code, self._url)
        self._scripts = html.scripts[:]
        self._cookies = dict(web_content.cookies)
        self._headers = web_content.headers
        self._metas = dict(html.metas)

    def is_application_detected(self, application: dict):
        """
        Determine whether the web content matches the application regex.
        """
        url_detected = self.is_application_detected_normalize_string(application, 'url', self._url)
        html_detected = self.is_application_detected_normalize_list(application, 'html', self._html_code)
        scripts_detected = self.is_application_detected_normalize_list(application, 'scriptSrc', self._scripts)
        cookies_detected = self.is_application_detected_normalize_dict(application, 'cookies', self._cookies)
        headers_detected = self.is_application_detected_normalize_dict(application, 'headers', self._headers)
        meta_detected = self.is_application_detected_normalize_dict(application, 'meta', self._metas)

        is_detected = (
            url_detected or html_detected or scripts_detected or cookies_detected or headers_detected or meta_detected
        )

        return is_detected

    def is_application_detected_normalize_string(self, application: dict, content_type: str, contents):
        """
        Determine whether the content matches the application regex
        Add a new version of application if the content matches
        """
        is_detected = False
        if application[content_type] != '':
            if re.search(application[content_type]['regex'], contents):
                is_detected = True
                self.update_version_detected(application, application[content_type], contents)

        return is_detected

    def is_application_detected_normalize_list(self, application: dict, content_type: str, contents):
        """
        Determine whether the content matches the application regex
        Add a new version of application if the content matches
        """
        is_detected = False

        for regex_params in application[content_type]:
            # Ensure to not iterate on a string value
            if isinstance(contents, str):
                contents = [contents]
            for content in contents:
                if re.search(regex_params['regex'], content):
                    is_detected = True
                    self.update_version_detected(application, regex_params, content)

        return is_detected

    def is_application_detected_normalize_dict(self, application: dict, content_type: str, contents):
        """
        Determine whether the content matches the application regex
        Add a new version of application if the content matches
        """
        is_detected = False
        for (key, regex_params) in application[content_type].items():
            if key in contents:
                # regex_params is a list : [{"application_pattern": "..", "regex": "re.compile(..)"}, ...]
                for i, _ in enumerate(regex_params):
                    if re.search(regex_params[i]['regex'], contents[key]):
                        is_detected = True
                        self.update_version_detected(application, regex_params[i], contents[key])

        return is_detected

    @staticmethod
    def update_version_detected(application: dict, regex_params, content):
        """
        Add a new detected version of application.
        """
        if 'version' in regex_params:
            found_occurrences = re.findall(regex_params['regex'], content)
            for occurrence in found_occurrences:
                version_pattern = regex_params['version']

                # Ensure to not iterate on a string value
                if isinstance(occurrence, str):
                    occurrence = [occurrence]
                for i, match in enumerate(occurrence):
                    # Parse ternary operator : version:\\1?\\1:\\2
                    ternary = re.search(re.compile('\\\\' + str(i + 1) + '\\?([^:]+):(.*)$', re.I), version_pattern)
                    if (ternary and len(ternary.groups()) == 2
                            and ternary.group(1) is not None
                            and ternary.group(2) is not None):
                        ternary_match = ternary.group(1) if match != '' else ternary.group(2)
                        version_pattern = version_pattern.replace(ternary.group(0), ternary_match)

                    # Replace back references
                    version_pattern = version_pattern.replace('\\' + str(i + 1), match)
                if version_pattern != '':
                    if 'versions' not in application:
                        application['versions'] = [version_pattern]
                    elif version_pattern not in application['versions']:
                        application['versions'].append(version_pattern)

    def get_rec_implied_applications(self, detected_applications: set):
        """
        Return the set of applications implied by the already detected applications.
        """

        init_implied_applications = self.get_implied_applications(detected_applications)
        final_implied_applications = set()

        while not final_implied_applications.issuperset(init_implied_applications):
            final_implied_applications.update(init_implied_applications)
            init_implied_applications = self.get_implied_applications(final_implied_applications)

        return final_implied_applications

    def get_implied_applications(self, applications: set):
        """Look for implied applications"""
        final_implied_applications = set()

        for application_name in applications:
            implied_applications = self.applications[application_name]['implies']

            for regex_params in implied_applications:
                final_implied_applications.update({regex_params['application_pattern']})
        return final_implied_applications

    def get_categories(self, application_name: str):
        """
        Returns a list of the categories for a name of application.
        """
        category_numbers = self.applications.get(application_name, {}).get("cats", [])
        category_names = [
            self.categories.get(str(category_number), "").get("name", "")
            for category_number in category_numbers
        ]

        return category_names

    def get_groups(self, application_name: str):
        """
        Returns a list of the groups for a name of application.
        """
        category_numbers = self.applications.get(application_name, {}).get("cats", [])
        application_group = []

        for application_categorie in category_numbers:
            groups_numbers = self.categories.get(str(application_categorie), {}).get("groups", [])
            application_group += [
                self.groups.get(str(group_number), "").get("name", "")
                for group_number in groups_numbers
            ]

        return application_group

    def get_versions(self, application_name: str):
        """
        Returns a list of the discovered versions for a name of application.
        """
        return ([] if 'versions' not in self.applications[application_name]
                else self.applications[application_name]['versions'])

    def detect(self):
        """
        Return a list of applications that can be detected on web content.
        """
        detected_applications = set()
        applications = self.applications
        # Try to detect some applications
        for application_name in applications:
            if self.is_application_detected(applications[application_name]):
                detected_applications.add(application_name)

        # Add implied applications
        detected_applications |= self.get_rec_implied_applications(detected_applications)

        return detected_applications

    def detect_with_versions(self):
        """
        Return a list of applications with the versions that can be detected on the web page.
        """
        detected_applications = self.detect()
        versioned_applications = {}

        for application_name in detected_applications:
            versions = self.get_versions(application_name)
            versioned_applications[application_name] = {"versions": versions}

        return versioned_applications

    def detect_with_versions_and_categories(self):
        """
        Return a list of applications with their categories and the versions that can be detected on web content.
        """
        versioned_applications = self.detect_with_versions()
        versioned_and_categorised_applications = versioned_applications

        for application_name in versioned_applications:
            versioned_and_categorised_applications[application_name]["name"] = application_name
            category_names = self.get_categories(application_name)
            versioned_and_categorised_applications[application_name]["categories"] = category_names

        return versioned_and_categorised_applications

    def detect_with_versions_and_categories_and_groups(self):
        """
        Return a list of applications with their categories, their versions & theirs groups
        that can be detected on web content.
        """
        versioned_and_categorised_applications = self.detect_with_versions_and_categories()
        applications = versioned_and_categorised_applications

        for application_name in versioned_and_categorised_applications:
            group_names = self.get_groups(application_name)
            # Set the group & prevent group duplicates
            applications[application_name]["groups"] = list(dict.fromkeys(group_names))

        return applications
