import requests
import json
from collections import Counter
import argparse

def get_binary_packages_from_api(branch):
    url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
    response = requests.get(url)
    return response.json()


def get_all_arch(packages):
    all_arch = set(pkg['arch'] for pkg in packages['packages'])
    return all_arch


def compare_packages(sisyphus_packages, p10_packages, arch):
    diff = {
        "p10_not_in_sisyphus": [],
        "sisyphus_not_in_p10": [],
        "greater_version_in_sisyphus": []
    }

    sisyphus_package_names = {pkg["name"] for pkg in sisyphus_packages['packages'] if pkg['arch'] == arch}
    p10_package_names = {pkg["name"] for pkg in p10_packages['packages'] if pkg['arch'] == arch}

    diff["p10_not_in_sisyphus"] = list(p10_package_names - sisyphus_package_names)
    diff["sisyphus_not_in_p10"] = list(sisyphus_package_names - p10_package_names)

    version_release_sisyphus = Counter([f'{pkg["version"]}-{pkg["release"]}' for pkg in sisyphus_packages['packages'] if pkg['arch'] == arch])
    version_release_p10 = Counter([f'{pkg["version"]}-{pkg["release"]}' for pkg in p10_packages['packages'] if pkg['arch'] == arch])

    for version_release in version_release_sisyphus:
        if version_release in version_release_p10:
            if version_release_sisyphus[version_release] > version_release_p10[version_release]:
                diff["greater_version_in_sisyphus"].append(version_release)

    return diff


def main(args):
    sisyphus_branch = args.sisyphus_branch
    p10_branch = args.p10_branch

    sisyphus_packages = get_binary_packages_from_api(sisyphus_branch)
    p10_packages = get_binary_packages_from_api(p10_branch)

    result = {}
    all_arch = get_all_arch(sisyphus_packages)

    for arch in all_arch:
        res = compare_packages(sisyphus_packages, p10_packages, arch)
        result[arch] = res

    with open(args.output_file, 'w') as json_file:
        json.dump(result, json_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare binary packages between two branches.')
    parser.add_argument('sisyphus_branch', type=str, help='The name of the Sisyphus branch')
    parser.add_argument('p10_branch', type=str, help='The name of the p10 branch')
    parser.add_argument('--output-file', type=str, default='res.json', help='Output file name for the result')

    args = parser.parse_args()
    main(args)
