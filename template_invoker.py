import csv
import subprocess
import os

versions_path = "version/version - Sheet1.csv"
combinations_path = "combination/combination - Sheet1.csv"
nexus_url = ""
base_directory = "base_images"


def read_files_to_map(file_name):
    data_map = {}
    with open(file_name, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            key = row.pop(0)
            data_map[key] = row
    file.close()

    return data_map


def generate_image_properties(composition, versions):
    dependencies = composition.split(",")
    template = dependencies.pop(0)
    template_version = versions[template][0]

    # print("template : {} dependencies : {}".format(template, dependencies))
    dependency_map = {}
    image_name = "run_" + template[:-1] + "-" + str(versions[template][0]) + "_"
    for dependency in dependencies:
        dependency_version = versions[dependency][0]
        image_name = image_name + dependency[:-1] + "-" + str(dependency_version) + "_"
        dependency_map[dependency[:-1] + "_version"] = dependency_version

    image_name = image_name[:-1]
    return template[:-1], template_version, image_name, dependency_map


def build_args_string(template, template_version,  dependencies):
    build_string = ""
    build_string = build_string + "--build-arg " + template + "=" + template_version
    for dependency in dependencies:
        build_string = build_string + " --build-arg " + dependency + "=" + dependencies[dependency]

    return build_string


def build_docker_image(template, template_version, image_name, dependencies):
    try:
        print("Current working directory: {0}".format(os.getcwd()))
        os.chdir(template)
        print("Current working directory: {0}".format(os.getcwd()))

        build_arg_string = build_args_string(template, template_version, dependencies)
        docker_image_reference = "{0}/{1}/{2}".format(nexus_url, base_directory, image_name)
        docker_build_command = "docker build -t {0} {1} .".format(docker_image_reference, build_arg_string)

        docker_push_command = "docker push {0}".format(docker_image_reference)


        print("docker build commands : {0}".format(docker_build_command))
        print("docker push commands : {0}".format(docker_push_command))

        os.system(docker_build_command)
        os.system(docker_push_command)
        os.chdir('../')

    except Exception as e:
        print("build_docker_image exception: {0}".format(e))
        os.chdir('../')


def generate_images_map(versions, combinations):
    for key in combinations:
        # print(key)
        # print(combinations[key])
        # print(combinations[key][0])

        unique_images = combinations[key][0].split(":")

        for image in unique_images:
            image_composition = image.strip()
            # print("key- {} image- {}".format(key, image_composition))
            template, template_version, image_name, dependencies = generate_image_properties(image_composition,
                                                                                             versions)

            print("template: {} template_version: {} image_name: {} dependencies: {}".format(template, template_version,
                                                                                             image_name, dependencies))

            # todo call relevant script using template and pass dependencies
            # template invoke here
            build_docker_image(template, template_version, image_name, dependencies)


version_map = read_files_to_map(versions_path)
combinations_map = read_files_to_map(combinations_path)

print("versions_map: {}".format(version_map))
print("combinations_map: {}".format(combinations_map))

generate_images_map(version_map, combinations_map)
