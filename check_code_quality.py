import requests
import subprocess

def check_code_quality(repository_url):
    # Retrieve repository information using GitHub API
    repository_details = get_repository_details(repository_url)
    if not repository_details:
        print("Error retrieving repository details. Please check the repository URL.")
        return

    # Extract repository name and path
    repository_name = repository_details["name"]
    repository_path = os.path.join(os.getcwd(), repository_name)

    # Clone the repository if not already cloned
    if not os.path.exists(repository_path):
        subprocess.check_call(["git", "clone", repository_url])

    # Run Flake8 and PyLint to check for code quality issues
    flake8_output = subprocess.check_output(["flake8", repository_path])
    flake8_errors = flake8_output.decode("utf-8").splitlines()

    pylint_output = subprocess.check_output(["pylint", repository_path])
    pylint_errors = pylint_output.decode("utf-8").splitlines()

    # Combine and process error messages from Flake8 and PyLint
    code_quality_issues = []
    for error_line in flake8_errors:
        if error_line:
            code_quality_issues.append(error_line)

    for error_line in pylint_errors:
        if error_line:
            code_quality_issues.append(error_line)

    # Return the list of code quality issues
    return code_quality_issues

def get_repository_details(repository_url):
    # Construct the API URL with the repository URL
    api_url = "https://api.github.com/repos/{}/{}".format(repository_url.split("/")[2], repository_url.split("/")[-1])

    # Set the authorization header using a personal access token
    headers = {"Authorization": "token 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"}

    # Send a GET request to the API endpoint
    response = requests.get(api_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response into a Python dictionary
        repository_data = json.loads(response.content)

        # Extract relevant repository information
        repository_name = repository_data["name"]
        description = repository_data["description"]
        created_at = repository_data["created_at"]
        updated_at = repository_data["updated_at"]

        # Return the extracted repository information
        return {
            "name": repository_name,
            "description": description,
            "created_at": created_at,
            "updated_at": updated_at
        }

    else:
        # Handle error cases
        print("Error retrieving repository details:", response.status_code)
        return None

if __name__ == "__main__":
    repository_url = input("Enter the repository URL: ")
    code_quality_issues = check_code_quality(repository_url)

    if code_quality_issues:
        print("\nCode Quality Issues:")
        for issue in code_quality_issues:
            print(issue)
    else:
        print("No code quality issues found.")
