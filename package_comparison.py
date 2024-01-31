import requests
import json
from collections import Counter

def get_binary_packages_from_api(branch):
    url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
    response = requests.get(url)
    return response.json()


def compare_packages(sisyphus_packages, p10_packages):
    diff = {
        "p10_not_in_sisyphus": [],
        "sisyphus_not_in_p10": [],
        "greater_version_in_sisyphus": []
    }

    sisyphus_package_names = {pkg["name"] for pkg in sisyphus_packages['packages']}
    p10_package_names = {pkg["name"] for pkg in p10_packages['packages']}

    diff["p10_not_in_sisyphus"] = list(p10_package_names - sisyphus_package_names)
    diff["sisyphus_not_in_p10"] = list(sisyphus_package_names - p10_package_names)

    version_release_sisyphus = Counter([f'{pkg["version"]}-{pkg["release"]}' for pkg in sisyphus_packages['packages']])
    version_release_p10 = Counter([f'{pkg["version"]}-{pkg["release"]}' for pkg in p10_packages['packages']])

    for version_release in version_release_sisyphus:
        if version_release in version_release_p10:
            if version_release_sisyphus[version_release] > version_release_p10[version_release]:
                diff["greater_version_in_sisyphus"].append(version_release)

    return diff


def main():
    sisyphus_branch = "sisyphus"
    p10_branch = "p10"

    sisyphus_packages = get_binary_packages_from_api(sisyphus_branch)
    p10_packages = get_binary_packages_from_api(p10_branch)

    result = compare_packages(sisyphus_packages, p10_packages)

    return result


if __name__ == "__main__":
    r = main()
    with open('res.json', 'w') as json_file:
        json.dump(r, json_file)
