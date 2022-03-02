'''Dataset class for pytorch presenting raw landmark data froma a csv file'''
import pandas as pd
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
# pylint: disable=E1101
# (torch.from_numpy is not recognised by pylint)
class GestureDataset(Dataset):
    '''Dataset of hand gestures to train model on.'''
    def __init__(self, location="source/data/data.csv",
                 transform=None, target_transform=None):
        self.data = pd.read_csv(location, header = None, dtype=np.float32)
        self.transform = transform
        self.target_transform = target_transform


    def __len__(self):
        '''Returns number of samples in dataset'''
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data.iloc[idx,:63].to_numpy(dtype=np.float32)
        label = np.array(int(self.data.iloc[idx, 63]))
        sample, label = torch.from_numpy(sample), torch.from_numpy(label)
        if self.transform:
            sample = self.transform(sample)
        if self.target_transform:
            label = self.target_transform(label)
        return sample, label

def main():
    '''Demo: returns a single batch of data'''
    dataset = GestureDataset()

    dataloader = DataLoader(dataset=dataset, batch_size=4, shuffle=True, num_workers=2)
    dataiter = iter(dataloader)

    data = dataiter.next()
    features, labels = data
    print(features, labels)

if __name__ == '__main__':
    main()
