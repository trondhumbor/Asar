import json
import os
import struct


class Unpack(object):

    def __init__(self, file):
        self.file = file
        with open(self.file, "rb") as f:
            f.seek(8)
            self.baseOffset = struct.unpack("I", f.read(4))[0] + 12
            header_length = struct.unpack("I", f.read(4))[0]
            self.header = json.loads(f.read(header_length).decode())

    def _extractFile(self, relativeOffset, size, output):
        with open(self.file, "rb") as i:
            i.seek(self.baseOffset + relativeOffset)
            with open(output, "wb") as o:
                o.write(i.read(size))

    def listFiles(self):
        def list_sub_files(folder, path=""):
            files = []
            for k, v in folder.items():
                if k == "files" or "files" in v:
                    for item in list_sub_files(v, path if k == "files" else os.path.join(path, k)):
                        files.append(item)

                if ("unpacked" in v and v["unpacked"]) or k == "files":
                    continue

                files.append({
                    "path": os.path.join(path, k),
                    "size": int(v["size"]) if "size" in v else None,
                    "offset": int(v["offset"]) if "offset" in v else None,
                    "is_file": "size" in v and "offset" in v
                })
            return files

        return list_sub_files(self.header["files"])

    def extractFile(self, inFile, outFile):
        for f in self.listFiles():
            if (os.path.normpath(inFile) == os.path.normpath(f["path"])) and f["is_file"]:
                self._extractFile(f["offset"], f["size"], outFile)
                break

    def extractFiles(self, outDir):
        os.makedirs(outDir, exist_ok=True)
        for f in self.listFiles():
            fullPath = os.path.join(outDir, f["path"])
            if not f["is_file"]:
                os.makedirs(fullPath, exist_ok=True)
                continue

            os.makedirs(os.path.dirname(fullPath), exist_ok=True)
            self._extractFile(f["offset"], f["size"], fullPath)
