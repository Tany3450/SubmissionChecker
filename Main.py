#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gradleParser as gr
from androGuard.apk import APK
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()


def apk_SIZE(size):
    if size < 15728640:
        print "APK2 - Success. APK size is less than 15 MB."
    else:
        print "APK2 - Fail. APK size is more than 15 MB."


def min_SDK(min_sdk_version):
    if min_sdk_version == parser.get('B5', 'minSdkVersion'):
        print "B5 - Success. MinSDKVersion is set to 16."
    else:
        print "B5 - Fail. MinSDKVersion is not set to 16."


def target_SDK(target_sdk_version):
    if target_sdk_version == parser.get('B6', 'targetSdkVersion'):
        print "B6 - Success. TargetSDKVersion is set to 24."
    else:
        print "B6 - Fail. TargetSDKVersion is not set to 24."


def package_NAME(package_name):
    if package_name[:17] == "com.monitise.mea.":
        print "B4 - Success. ApplicationId respects com.monitise.mea.<product> convention."
    else:
        print "B4 - Fail. ApplicationId does not respect com.monitise.mea.<product> convention."


def manifest_AllowBackup(application):
    try:
        if application.attributes['android:allowBackup'].value == parser.get('SEC1', 'allowBackup'):
            print "SEC1 - Success. android:allowBackup is set to false."
        else:
            print "SEC1 - Fail. android:allowBackup is set to true."
    except:
        print "SEC1 - Fail. android:allowBackup is not set."


def manifest_InstallLocation(application):
    try:
        if application.attributes['android:installLocation'].value != "externalOnly":
            print "MAN5 - Success. android:installLocation is not set to externalOnly."
        else:
            print "MAN5 - Fail. android:installLocation is set to externalOnly."
    except:
        print "MAN5 - Success. android:installLocation is not set."


def dependencyChecker(dependencies):
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
        print "B7 - Success. Google Play Services API is included as separate dependencies."
    else:
        print "B7 - Fail. Google Play Services API is not included as separate dependencies."
    if errorVersion == False:
        print "B8 - Success. Each dependency injected has a specific version specified."
    else:
        print "B8 - Fail. Some dependencies injected have not specified a version."


def versionName(version_name):
    if (version_name > parser.get('MAN2', 'previousVersionName')):
        print "MAN2 - Success. android:versionName attribute is updated."
    else:
        print "MAN2 - Fail. android:versionName attribute is not updated."

    if (len(version_name.split(".")) == 4):
        print "MAN3 - Success. android:versionName follows <major>.<minor>.<patch>.<buildNumber> convention."
    else:
        print "MAN3 - Fail. android:versionName does not follow <major>.<minor>.<patch>.<buildNumber> convention."


def proguardChecker(release_build):
    try:
        if (release_build["minifyEnabled"][0][0] == "true" and release_build["shrinkResources"][0][0] == "true"):
            print "PRG2 - Success. minifyEnabled and shrinkResoureces are set to true for release build type."
        else:
            print "PRG2 - Fail. minifyEnabled or/and shrinkResoureces are not set to true for release build type."
    except:
        print "PRG2 - Error. minifyEnabled or/and shrinkResources could not be found."

    allIncluded = True
    proguardFilesGradle = release_build["proguardFiles"]
    proguardFilesConfig = parser.get('PRG3', 'proguardList').split()
    for proguardFileConfig in proguardFilesConfig:
        if not (proguardFileConfig in proguardFilesGradle[0]):
            allIncluded = False
    if (allIncluded == True):
        print "PRG3 - Success. proguard configurations files are added through proguardFiles property in the release build type."
    else:
        print "PRG3 - Fail. not all proguard configurations files are added through proguardFiles property in the release build type."


def debuggableChecker(release_build):
    try:
        if (release_build["debuggable"][0][0] != 'true'):
            print "B9 - Success. Release build type in gradle build file doesn't have debuggable set to true."
        else:
            print "B9 - Fail. Release build type in gradle build file has debuggable set to true."
    except:
        print "B9 - Success. Release build type in gradle build file doesn't have debuggable attribute."


def signingConfigs(signingConfigs_release):
    try:
        if (signingConfigs_release["storeFile"][0] != None):
            print "SIGN2 - Success. Release keystore is included in source control."
            if not ("/build/" in signingConfigs_release["storeFile"][0][0]):
                print "SIGN3 - Success. The release keystore is NOT included in build classpath."
            else:
                print "SIGN3 - Fail. The release keystore is included in build classpath."
    except:
        print "SIGN2 - Fail. Release keystore is not included in source control."
    try:
        if (signingConfigs_release["storePassword"][0] != None
            and signingConfigs_release["keyAlias"][0] != None
            and signingConfigs_release["keyPassword"][0] != None):
            print "SIGN4 - Success. StorePassword, keyAlias, keyPassword are set in the build.gradle file for release signing config."
    except:
        print "SIGN4 - Fail. storePassword, keyAlias, keyPassword are not set in the build.gradle file for release signing config."


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
        print "SEC4 - Success. Android:exported is set to false for all services, activities and broadcast receivers containing intent filters."
    else:
        print "SEC4 - Fail. Android:exported is not set to false for some/all services, activities and broadcast receivers containing intent filters."


def versionCode(defaultConfig):
    if (defaultConfig["versionCode"][0][0] > parser.get('MAN1', 'previousVersionCode')):
        print "MAN1 - Success. android:versionCode is incremented."
    else:
        print "MAN1 - Fail. android:versionCode is not incremented."


def hardwareFeatures(features, featuresIsRequired):
    i = 0
    error = False
    for feature in features:
        if "hardware" in feature:
            if featuresIsRequired[i] != "false":
                error = True
        i = i + 1
    if error != True:
        print "PERM3 - Success. android:required is set to false for hardware features."
    else:
        print "PERM3 - Fail. android:required is not set to false for hardware features."


def resConfigs(res_configs):
    error = False
    for res_config in res_configs:
        if not (res_config in parser.get('B1', 'resConfigs').split()):
            error = True
    if error != True:
        print "B1 - Success. res configs minimized by only including necessary resources."
    else:
        print "B1 - Fail. res configs are not minimized by only including necessary resources."


def main():
    parser.read('config.ini')
    myapk = APK("/users/ozefet/AndroidStudioProjects/UdacityMovies/app/build/outputs/apk/app-debug.apk")
    manifestXML = myapk.get_android_manifest_xml()
    gradleResult = gr.GradleParser().parse(False)
    apk_SIZE(myapk.file_size)
    resConfigs(gradleResult["android"]["defaultConfig"][0]["resConfigs"][0])
    package_NAME(myapk.package)
    min_SDK(myapk.get_min_sdk_version())
    target_SDK(myapk.get_target_sdk_version())
    dependencyChecker(gradleResult["dependencies"]["compile"])
    debuggableChecker(gradleResult["android"]["buildTypes"][0]["release"][0])
    versionCode(gradleResult["android"]["defaultConfig"][0])
    versionName(manifestXML.getElementsByTagName('manifest')[0].attributes['android:versionName'].value)
    manifest_InstallLocation(manifestXML.getElementsByTagName('application')[0])
    proguardChecker(gradleResult["android"]["buildTypes"][0]["release"][0])
    signingConfigs(gradleResult["android"]["signingConfigs"][0]["release"][0])
    manifest_AllowBackup(manifestXML.getElementsByTagName('application')[0])
    exportedCheck(
        manifestXML.getElementsByTagName('manifest')[0].getElementsByTagName('application')[0].getElementsByTagName(
            'service')
        , manifestXML.getElementsByTagName('manifest')[0].getElementsByTagName('application')[0].getElementsByTagName(
            'activity')
        , manifestXML.getElementsByTagName('manifest')[0].getElementsByTagName('application')[0].getElementsByTagName(
            'receiver'))
    hardwareFeatures(myapk.features, myapk.featuresIsRequired)


if __name__ == "__main__":
    main()
