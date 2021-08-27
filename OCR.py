from save_csv import Csv
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'tesseract'


def saveTxt(name, text):
    with open(name, 'w') as f:
        f.write(text)

def givePhotos(folder_name = './OCR'):
    return [photo for photo in os.listdir(folder_name) if not photo.startswith('.')]

def splitDOM(text):
    text = text.split()
    try:
        comment_index = text.index('Yorum')

        comment = text[comment_index - 1]
        like = text[comment_index - 2]
        share = text[comment_index + 1]

        try:
            comment = int(comment)
        except ValueError:
            comment = 0

        try:
            like = int(like)
        except ValueError:
            like = 0

        try:
            share = int(share)
        except ValueError:
            share = 0

        ret = [like, comment, share]
    except ValueError:
        ret = [0, 0, 0]
    return ret


if __name__ == '__main__':

    photos = givePhotos()
    md5 = photos[0].split('_')[2]

    fieldnames = ['Begeni', 'Yorum', 'Paylasim']
    ocr_csv = Csv(f'./OCR/bot-facebook_{md5}.csv', fieldnames=fieldnames)
    ocr_csv.initialize(close_file=True)
    ocr_csv.open(mode='a')

    for photo in photos:
        name = './OCR/' + photo.split(".")[0] + '.txt'
        text = pytesseract.image_to_string(Image.open('./OCR/' + photo))

        saveTxt(name, text)

        row = splitDOM(text)
        ocr_csv.writerow(row)
    ocr_csv.close()