import os
import sqlite3
import pandas as pd
from torch.utils.data import Dataset
from torchvision.io import read_image
from torchvision.transforms.functional import to_pil_image
from util import download_image


class UrlImageDataset(Dataset):
    def __init__(self, label_csv_path: str, dir_path: str, transform=None, target_transform=None):
        self.img_label_df = pd.read_csv(label_csv_path, header=None)
        self.dir_path = dir_path
        self.transform = transform
        self.target_transform = target_transform

        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

        connection = sqlite3.connect(os.path.join(self.dir_path, 'uu_map'))
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS uu_map (url, uid)')
        connection.close()

    def __len__(self):
        return len(self.img_label_df.index)

    def __getitem__(self, idx):
        image_url = self.img_label_df.iloc[idx, 0]
        label = self.img_label_df.iloc[idx, 1]

        connection = sqlite3.connect(os.path.join(self.dir_path, 'uu_map'))
        cursor = connection.cursor()

        row = cursor.execute(f'SELECT uid FROM uu_map WHERE url=\'{image_url}\'').fetchone()

        uid = None if row is None else row[0]

        if uid is None:
            uid = download_image(image_url, self.dir_path)
            cursor.execute(f'INSERT INTO uu_map (url, uid) VALUES (\'{image_url}\', \'{uid}\')')

        connection.commit()
        connection.close()

        img_path = os.path.join(self.dir_path, uid)
        image = to_pil_image(read_image(img_path))

        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)

        return image, label
