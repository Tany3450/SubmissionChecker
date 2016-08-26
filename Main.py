#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gradleParser as gr
from androGuard.apk import APK
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
html_str = "<table border=1><tr><th>ID</th><th>Result</th><th>Explanation</th></tr>"


def apk_SIZE(size):
    if size < 15728640:
        result = "APK2.Success.APK size is less than 15 MB."
        print result
        return result
    else:
        result = "APK2.Fail.APK size is more than 15 MB."
        print result
        return result


def min_SDK(min_sdk_version):
    if min_sdk_version == parser.get('B5', 'minSdkVersion'):
        result = "B5.Success.MinSDKVersion is set to 16."
        print result
        return result
    else:
        result = "B5.Fail.MinSDKVersion is not set to 16."
        print result
        return result


def target_SDK(target_sdk_version):
    if target_sdk_version == parser.get('B6', 'targetSdkVersion'):
        result = "B6.Success.TargetSDKVersion is set to 24."
        print result
        return result
    else:
        result = "B6.Fail.TargetSDKVersion is not set to 24."
        print result
        return result


def package_NAME(package_name):
    if package_name[:17] == "com.monitise.mea.":
        result = "B4.Success.ApplicationId respects com/monitise/mea/<product> convention."
        print result
        return result
    else:
        result = "B4.Fail.ApplicationId does not respect com/monitise/mea/<product> convention."
        print result
        return result

def manifest_AllowBackup(application):
    try:
        if application.attributes['android:allowBackup'].value == parser.get('SEC1', 'allowBackup'):
            result = "SEC1.Success.android:allowBackup is set to false."
            print result
            return result
        else:
            result = "SEC1.Fail.android:allowBackup is set to true."
            print result
            return result
    except:
        result = "SEC1.Fail.android:allowBackup is not set."
        print result
        return result


def manifest_InstallLocation(application):
    try:
        if application.attributes['android:installLocation'].value != "externalOnly":
            result = "MAN5.Success.android:installLocation is not set to externalOnly."
            print result
            return result
        else:
            result = "MAN5.Fail.android:installLocation is set to externalOnly."
            print result
            return result
    except:
        result = "MAN5.Success.android:installLocation is not set."
        print result
        return result


def dependencyChecker(dependencies):
    global html_str
    errorGoogleAPI = False
    errorVersion = False
    for dependency in dependencies:
        if (len(dependency) == 1):
            if ("+" in dependency[0]):
                errorVersion = True
                # print "B8 - " + dependency
            if ("com.google.android.gms:play-services:" == dependency[0][:37]):
                errorGoogleAPI = True
    if (errorGoogleAPI == False):
        print "B7.Success.Google Play Services API is included as separate dependencies."
        html_str += "<tr><td>" + "B7" + "</td><td>" + "Success" + "</td><td>" + "Google Play Services API is included as separate dependencies." + "</td></tr>"
    else:
        print "B7.Fail.Google Play Services API is not included as separate dependencies."
        html_str += "<tr><td>" + "B7" + "</td><td>" + "Fail" + "</td><td>" + "Google Play Services API is not included as separate dependencies." + "</td></tr>"
    if errorVersion == False:
        print "B8.Success.Each dependency injected has a specific version specified."
        html_str += "<tr><td>" + "B8" + "</td><td>" + "Success" + "</td><td>" + "Each dependency injected has a specific version specified." + "</td></tr>"
    else:
        print "B8.Fail.Some dependencies injected have not specified a version."
        html_str += "<tr><td>" + "B8" + "</td><td>" + "Fail" + "</td><td>" + "Some dependencies injected have not specified a version." + "</td></tr>"


def versionName(version_name):
    global html_str
    if (version_name > parser.get('MAN2', 'previousVersionName')):
        print "MAN2.Success.android:versionName attribute is updated."
        html_str += "<tr><td>" + "MAN2" + "</td><td>" + "Success" + "</td><td>" + "android:versionName attribute is updated." + "</td></tr>"
    else:
        print "MAN2.Fail.android:versionName attribute is not updated."
        html_str += "<tr><td>" + "MAN2" + "</td><td>" + "Fail" + "</td><td>" + "android:versionName attribute is not updated." + "</td></tr>"

    if (len(version_name.split(".")) == 4):
        print "MAN3.Success.android:versionName follows <major>.<minor>.<patch>.<buildNumber> convention."
        html_str += "<tr><td>" + "MAN3" + "</td><td>" + "Success" + "</td><td>" + "android:versionName follows <major>.<minor>.<patch>.<buildNumber> convention." + "</td></tr>"
    else:
        print "MAN3.Fail.android:versionName does not follow <major>.<minor>.<patch>.<buildNumber> convention."
        html_str += "<tr><td>" + "MAN3" + "</td><td>" + "Fail" + "</td><td>" + "android:versionName does not follow <major>.<minor>.<patch>.<buildNumber> convention." + "</td></tr>"


def proguardChecker(release_build):
    global html_str
    try:
        if (release_build["minifyEnabled"][0][0] == "true" and release_build["shrinkResources"][0][0] == "true"):
            print "PRG2.Success.minifyEnabled and shrinkResoureces are set to true for release build type."
            html_str += "<tr><td>" + "PRG2" + "</td><td>" + "Success" + "</td><td>" + "minifyEnabled and shrinkResoureces are set to true for release build type." + "</td></tr>"
        else:
            print "PRG2.Fail.minifyEnabled or/and shrinkResoureces are not set to true for release build type."
            html_str += "<tr><td>" + "PRG2" + "</td><td>" + "Fail" + "</td><td>" + "minifyEnabled or/and shrinkResoureces are not set to true for release build type." + "</td></tr>"
    except:
        print "PRG2.Error.minifyEnabled or/and shrinkResources could not be found."
        html_str += "<tr><td>" + "PRG2" + "</td><td>" + "Error" + "</td><td>" + "minifyEnabled or/and shrinkResources could not be found." + "</td></tr>"

    allIncluded = True
    proguardFilesGradle = release_build["proguardFiles"]
    proguardFilesConfig = parser.get('PRG3', 'proguardList').split()
    for proguardFileConfig in proguardFilesConfig:
        if not (proguardFileConfig in proguardFilesGradle[0]):
            allIncluded = False
    if (allIncluded == True):
        print "PRG3.Success.proguard configurations files are added through proguardFiles property in the release build type."
        html_str += "<tr><td>" + "PRG3" + "</td><td>" + "Success" + "</td><td>" + "proguard configurations files are added through proguardFiles property in the release build type." + "</td></tr>"
    else:
        print "PRG3.Fail.not all proguard configurations files are added through proguardFiles property in the release build type."
        html_str += "<tr><td>" + "PRG3" + "</td><td>" + "Fail" + "</td><td>" + "not all proguard configurations files are added through proguardFiles property in the release build type." + "</td></tr>"


def debuggableChecker(release_build):
    try:
        if (release_build["debuggable"][0][0] != 'true'):
            result = "B9.Success.Release build type in gradle build file doesn't have debuggable set to true."
            print result
            return result
        else:
            result = "B9.Fail.Release build type in gradle build file has debuggable set to true."
            print result
            return result
    except:
        result = "B9.Success.Release build type in gradle build file doesn't have debuggable attribute."
        print result
        return result


def signingConfigs(signingConfigs_release):
    global html_str
    try:
        if (signingConfigs_release["storeFile"][0] != None):
            print "SIGN2.Success.Release keystore is included in source control."
            html_str += "<tr><td>" + "SIGN2" + "</td><td>" + "Success" + "</td><td>" + "Release keystore is included in source control." + "</td></tr>"
            if not ("/build/" in signingConfigs_release["storeFile"][0][0]):
                print "SIGN3.Success.The release keystore is NOT included in build classpath."
                html_str += "<tr><td>" + "SIGN3" + "</td><td>" + "Success" + "</td><td>" + " The release keystore is NOT included in build classpath." + "</td></tr>"

            else:
                print "SIGN3.Fail.The release keystore is included in build classpath."
                html_str += "<tr><td>" + "SIGN3" + "</td><td>" + "Fail" + "</td><td>" + "The release keystore is included in build classpath." + "</td></tr>"

    except:
        print "SIGN2.Fail.Release keystore is not included in source control."
        html_str += "<tr><td>" + "SIGN2" + "</td><td>" + "Fail" + "</td><td>" + "Release keystore is not included in source control." + "</td></tr>"

    try:
        if (signingConfigs_release["storePassword"][0] != None
            and signingConfigs_release["keyAlias"][0] != None
            and signingConfigs_release["keyPassword"][0] != None):
            print "SIGN4.Success.StorePassword, keyAlias, keyPassword are set in the build.gradle file for release signing config."
            html_str += "<tr><td>" + "SIGN4" + "</td><td>" + "Success" + "</td><td>" + "StorePassword, keyAlias, keyPassword are set in the build.gradle file for release signing config." + "</td></tr>"

    except:
        print "SIGN4.Fail.storePassword, keyAlias, keyPassword are not set in the build.gradle file for release signing config."
        html_str += "<tr><td>" + "SIGN4" + "</td><td>" + "Fail" + "</td><td>" + "storePassword, keyAlias, keyPassword are not set in the build.gradle file for release signing config." + "</td></tr>"


def exportedCheck(services, activities, receivers):
    errorCheck = False
    for service in services:
        try:
            if service.getElementsByTagName('intent-filter')[0] != None:
                try:
                    if service.attributes['android:exported'].value != "false":
                        errorCheck = True
                except:
                    errorCheck = True
        except:
            None
    for activity in activities:
        try:
            if activity.getElementsByTagName('intent-filter')[0] != None:
                try:
                    if activity.attributes['android:exported'].value != "false":
                        errorCheck = True
                except:
                    errorCheck = True
        except:
            None
    for receiver in receivers:
        try:
            if receiver.getElementsByTagName('intent-filter')[0] != None:
                try:
                    if receiver.attributes['android:exported'].value != "false":
                        errorCheck = True
                except:
                    errorCheck = True
        except:
            None
    if errorCheck != True:
        result = "SEC4.Success.Android:exported is set to false for all services, activities and broadcast receivers containing intent filters."
        print result
        return result
    else:
        result = "SEC4.Fail.Android:exported is not set to false for some/all services, activities and broadcast receivers containing intent filters."
        print result
        return result


def versionCode(defaultConfig):
    if (defaultConfig["versionCode"][0][0] > parser.get('MAN1', 'previousVersionCode')):
        result = "MAN1.Success.android:versionCode is incremented."
        print result
        return result
    else:
        result = "MAN1.Fail.android:versionCode is not incremented."
        print result
        return result


def hardwareFeatures(features, featuresIsRequired):
    i = 0
    error = False
    for feature in features:
        if "hardware" in feature:
            if featuresIsRequired[i] != "false":
                error = True
        i = i + 1
    if error != True:
        result = "PERM3.Success.android:required is set to false for hardware features."
        print result
        return result
    else:
        result = "PERM3.Fail.android:required is not set to false for hardware features."
        print result
        return result


def resConfigs(res_configs):
    error = False
    for res_config in res_configs:
        if not (res_config in parser.get('B1', 'resConfigs').split()):
            error = True
    if error != True:
        result = "B1.Success.res configs minimized by only including necessary resources."
        print result
        return result
    else:
        result = "B1.Fail.res configs are not minimized by only including necessary resources."
        print result
        return result


def apkNameFormat(apkName, versionName, gradle):
    apkName = apkName[apkName.index("apk/") + len("apk/"):].split("-")
    if (len(apkName) != 4):
        result = "APK1.Fail.Apk name is missing some arguments."
        print result
        return result
    try:
        app_name = gradle['monitise']['appOptions'][0]['projectName'][0]
        flavors = gradle['android']['productFlavors'][0].keys()
        build_types = gradle['android']['buildTypes'][0].keys()
    except:
        result = "APK1.Fail.Some format types were not found."
        print result
        return result
    if (apkName[0] == app_name and apkName[1] in flavors and apkName[2] in build_types and apkName[3] == versionName()):
        result = "APK1.Success.Apk follows correct name format."
        print result
        return result
    else:
        result = "APK1.Success.Apk follows correct name format."
        print result
        return result


def addToHtml(result):
    global html_str
    html_str += "<tr><td>" + result[0] + "</td><td>" + result[1] + "</td><td>" + result[2] + "</td></tr>"


def main():
    global html_str
    Html_file = open("filename", "w")
    parser.read('config.ini')
    myapk = APK("/users/ozefet/AndroidStudioProjects/UdacityMovies/app/build/outputs/apk/app-debug.apk")
    manifestXML = myapk.get_android_manifest_xml()
    gradleResult = gr.GradleParser().parse(False)
    result = apkNameFormat(myapk.filename,
                           manifestXML.getElementsByTagName('manifest')[0].attributes['android:versionName'].value,
                           gradleResult).split(".")
    addToHtml(result)
    addToHtml(apk_SIZE(myapk.file_size).split("."))
    addToHtml(resConfigs(gradleResult["android"]["defaultConfig"][0]["resConfigs"][0]).split("."))
    addToHtml(package_NAME(myapk.package).split("."))
    addToHtml(min_SDK(myapk.get_min_sdk_version()).split("."))
    addToHtml(target_SDK(myapk.get_target_sdk_version()).split("."))
    dependencyChecker(gradleResult["dependencies"]["compile"])
    addToHtml(debuggableChecker(gradleResult["android"]["buildTypes"][0]["release"][0]).split("."))
    addToHtml(versionCode(gradleResult["android"]["defaultConfig"][0]).split("."))
    versionName(manifestXML.getElementsByTagName('manifest')[0].attributes['android:versionName'].value)
    addToHtml(manifest_InstallLocation(manifestXML.getElementsByTagName('application')[0]).split("."))
    proguardChecker(gradleResult["android"]["buildTypes"][0]["release"][0])
    signingConfigs(gradleResult["android"]["signingConfigs"][0]["release"][0])
    addToHtml(manifest_AllowBackup(manifestXML.getElementsByTagName('application')[0]).split("."))
    result = exportedCheck(
        manifestXML.getElementsByTagName('manifest')[0].getElementsByTagName('application')[0].getElementsByTagName(
            'service')
        , manifestXML.getElementsByTagName('manifest')[0].getElementsByTagName('application')[0].getElementsByTagName(
            'activity')
        , manifestXML.getElementsByTagName('manifest')[0].getElementsByTagName('application')[0].getElementsByTagName(
            'receiver')).split(".")
    addToHtml(result)
    addToHtml(hardwareFeatures(myapk.features, myapk.featuresIsRequired).split("."))
    html_str += "</tr></indent></table></body></html>"
    Html_file.write(html_str)
    Html_file.close()


if __name__ == "__main__":
    main()
