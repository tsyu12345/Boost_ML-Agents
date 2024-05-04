from enum import Enum

class MLAgentsReleases(Enum):
    REREASE_21 = 21
    REREASE_20 = 20
    REREASE_19 = 19

class MLAgentsEditors:
    """
    release対応毎に、対応するUnityEditorのバージョンを定義する
    """
    editors: dict[MLAgentsReleases, list[str]] = {
        MLAgentsReleases.REREASE_21: ["2020.3.15f2", "2021.1.15f1", "2021.2.7f1"],
        MLAgentsReleases.REREASE_20: ["2020.3.15f2", "2021.1.15f1", "2021.2.7f1"],
        MLAgentsReleases.REREASE_19: ["2020.3.15f2", "2021.1.15f1", "2021.2.7f1"],
    }