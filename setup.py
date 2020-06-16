import subprocess
import urllib.request
import sys
import os

pyaudio = {
    "27": "https://download.lfd.uci.edu/pythonlibs/s2jqpv5t/cp27/PyAudio-0.2.11-cp27-cp27m-win_amd64.whl",
    "34": "https://download.lfd.uci.edu/pythonlibs/s2jqpv5t/cp34/PyAudio-0.2.11-cp34-cp34m-win_amd64.whl",
    "35": "https://download.lfd.uci.edu/pythonlibs/s2jqpv5t/cp35/PyAudio-0.2.11-cp35-cp35m-win_amd64.whl",
    "36": "https://download.lfd.uci.edu/pythonlibs/s2jqpv5t/PyAudio-0.2.11-cp36-cp36m-win_amd64.whl",
    "37": "https://download.lfd.uci.edu/pythonlibs/s2jqpv5t/PyAudio-0.2.11-cp37-cp37m-win_amd64.whl",
    "38": "https://download.lfd.uci.edu/pythonlibs/s2jqpv5t/PyAudio-0.2.11-cp38-cp38-win_amd64.whl"
}


def version():
    platform = str(sys.version_info[0]) + str(sys.version_info[1])
    return platform


def download():
    required = version()
    url = pyaudio[f"{required}"]
    urllib.request.urlretrieve(url, "pyaudio.whl")
    pass


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    pass


packages = [
    "pyaudio.whl",
    "playsound",
    "SpeechRecognition",
    "gtts",
    "webbrowser",
    "googleapiclient.discovery",
    "google_auth_oauthlib.flow",
    "google.auth.transport.requests",
    "pyttsx3",
    "pytz"
]


def main():
    download()
    for package in packages:
        install(package)
    os.remove(packages[0])
    pass


if __name__ == '__main__':
    main()
    pass
