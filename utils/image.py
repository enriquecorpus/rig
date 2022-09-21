from bing_image_downloader.bing import Bing
from pathlib import Path
import os
import base64
import shutil


class ImageDownloader(Bing):
    def get_filter(self, shorthand):
        ret = super(ImageDownloader, self).get_filter(shorthand)
        if shorthand == "thumbnail":
            return "+filterui:imagesize-small"
        return ret

    def get_result_as_base64(self):
        try:
            self.run()
            file = os.listdir(self.output_dir)[0]
            with open(Path(self.output_dir).joinpath(file).absolute(), "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            shutil.rmtree(self.output_dir)
            return encoded_string.decode("utf-8")
        except Exception as e:
            return ""
