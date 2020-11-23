import json
import os
import struct


class Pack(object):

    def __init__(self, inFolder, outFile):
        self.inFolder = inFolder
        self.outFile = outFile
        self.tempFile = self.outFile + ".tmp"

    def pack(self):
        def list_sub_files(folder):
            files = {
                "files": {}
            }
            for f in os.listdir(folder):
                fullPath = os.path.join(folder, f)
                if os.path.isdir(fullPath):
                    files["files"][f] = list_sub_files(fullPath)
                    continue

                with open(fullPath, "rb") as i:
                    with open(self.tempFile, "ab") as o:
                        offset = o.tell()
                        o.write(i.read())

                files["files"][f] = {
                    "size": os.stat(fullPath).st_size,
                    "offset": str(offset)
                }
            return files

        header = json.dumps(list_sub_files(self.inFolder), separators=(",", ":")).encode("utf-8")

        with open(self.outFile, "wb") as f:
            f.write(struct.pack("I", 4))
            f.write(struct.pack("I", len(header) + 8))
            f.write(struct.pack("I", len(header) + 4))
            f.write(struct.pack("I", len(header)))
            f.write(header)
            with open(self.tempFile, "rb") as i:
                chunkSize = 2**14
                for data in iter(lambda: i.read(chunkSize), b""):
                    f.write(data)

        os.remove(self.tempFile)

