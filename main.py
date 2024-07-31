from url_image_dataset import UrlImageDataset

if __name__ == '__main__':
    dataset = UrlImageDataset("test.csv", "test")
    print(dataset[0])
