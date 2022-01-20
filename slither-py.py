import os
import pathlib
from typing import Type
from detector_api.skeleton_detector import Skeleton
from detector_api.too_many_digits import TooManyDigits
from slither.detectors.abstract_detector import AbstractDetector
from slither import Slither
import json

class SoliditySlitherAnalyzer:
    def __init__(
            self,
            detector: Type[AbstractDetector],
            solc_ver: str,

        ):
        """
        :param detector-api:
        :param solc_ver:
        Slither-Analyzer Class Constructor takes two arguments first is Slither-detector-API, Second is solidity version that set is static
        """
        self.detector = detector
        self.expected_result = detector.__name__ + ".json"
        self.solc_ver = solc_ver
        print(f"detector-Api {self.detector.__name__} Init.. ")


    def getCompilerVersion(self,soliditiy_file):
        '''
        it's help to get solc version from given solidity file
        :param soliditiy_file
        soliditiy_file path convert into full absolute path with the help of pathlib library
        '''

        solidityFile =  pathlib.Path(
            pathlib.Path().absolute(),
            soliditiy_file
        )

        solidityFile  = open(solidityFile, 'r')
        Lines = solidityFile.readlines()
        compilerVersion = ''

        # reads line by line from solidtiy file
        for line in Lines:
            line =line.replace(" ", "")


            if ('pragma' in line):
                totLenOfLine = len(line)
                found = line.find("^", 0, totLenOfLine)

                if (found != -1):

                    compilerVersion = line[found + 1:totLenOfLine - 2]

                else:
                    gtfound = line.find(">=", 0, totLenOfLine)
                    ltfound = line.find('<', 0, totLenOfLine)
                    compilerVersion = line[gtfound + 2:ltfound - 1]
                    if (line[ltfound - 1] == '.'):
                        compilerVersion = compilerVersion + '0'
                break

        # if user does not mention solidity version then progaram will ask to put solidity version of solc file
        if (not compilerVersion):
            print("pragma-solidity version missing in file please enter manually")
            compilerVersion = input("Enter solidity version that you are use: ")


        print("compilversion: ",compilerVersion)


        commandToExec = 'solc-select install ' + compilerVersion
        os.system(commandToExec)
        commandToExec = 'solc-select use ' + compilerVersion
        os.system(commandToExec)
        cmd = "solc --version"
        os.system(cmd)

    def _generate_test(self, solidityFile, skip_existing=False):
        '''
             :param skip_existing : help to check user want to create new file or overwrite file
             :param solidityFile :  file_name

             '''

        # To set solc version env
        self.getCompilerVersion(solidityFile)

        base = os.path.basename(solidityFile)


        test_dir_path = pathlib.Path(
            pathlib.Path().absolute(),
            "detector_log",
            self.detector.ARGUMENT,
            os.path.splitext(base)[0],
            self.solc_ver,
        )

        # check created path is existe or not if directory not existe then created it
        if not os.path.exists(test_dir_path):
            os.makedirs(test_dir_path)

        # attach json file in test_dir_path
        expected_result_path = str(pathlib.Path(test_dir_path, self.expected_result).absolute())

        # if file already exist then program will terminate
        if skip_existing:
            if os.path.isfile(expected_result_path):
                return

        # Init Slither Object
        sl = Slither(solidityFile)
        # attach Slither-detector-Api
        sl.register_detector(self.detector)
        results = sl.run_detectors()

        results_as_string = json.dumps(results)
        print("result:-  ", results_as_string)
        results = json.loads(results_as_string)


        # create new json file and write  result into it
        with open(expected_result_path, "w") as f:
            f.write(json.dumps(results, indent=4))

        print(" Result dir_path: ", test_dir_path)

        print("json file Path : ", expected_result_path)

if __name__ == "__main__":

    file_name = "soliditiy_files/backdoor.sol"

    analyzer = SoliditySlitherAnalyzer(Skeleton, "0.4.25")
    #analyzer.getCompilerVersion(file_name)
    analyzer._generate_test(file_name,skip_existing=True)