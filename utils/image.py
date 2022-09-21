from bing_image_downloader import bing as b

class ImageDownloader(b.Bing):
    def get_filter(self, shorthand):
        ret = super(ImageDownloader, self).get_filter(shorthand)
        if shorthand == "thumbnail":
            return "+filterui:imagesize-small"
        return ret
