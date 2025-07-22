from core.processor import process_img


class FaceSwapPicture:
    def swap(self, source, target):
        output = process_img(source, target)
        return output


faceSwapPicture = FaceSwapPicture()
