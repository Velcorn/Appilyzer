import torch
import torchvision
from augmentations import augmentation, ContrastiveAugmentation
import torchvision.transforms as transforms
from torchvision.datasets import VisionDataset
from PIL import Image
import os
import os.path
import numpy as np
import pickle
import torch
from typing import Any, Callable, Optional, Tuple
from os import listdir
from os.path import isfile, join
import io
import cv2

class AppylizerHealthDataset(VisionDataset):
    def __init__(
            self,
            root: str,
            train: bool = True,
            transform: Optional[Callable] = None,
            target_transform: Optional[Callable] = None,
            download: bool = False,
    ) -> None:

        super(AppylizerHealthDataset, self).__init__(root, transform=transform,
                                      target_transform=target_transform)

        self.train = train  # training set or test set

        data_dirs = ["healthy_", "unhealthy_"]

        for l in range(len(data_dirs)):
            if self.train:
                data_dirs[l] = data_dirs[l] + "train"
            else:
                data_dirs[l] = data_dirs[l] + "test"

        self.data: Any = []
        self.targets = []

        for unhealthy, directory in enumerate(data_dirs):
            current_dir = self.root + directory
            print(current_dir)
            #print(current_dir)
            onlyfiles = [f for f in listdir(current_dir) if isfile(join(current_dir, f))]
            print("Len only files: {0}".format(len(onlyfiles)))
            file_counter = 0
            for file_id, filename in enumerate(onlyfiles):
                ##print(filename)
                file_path = os.path.join(self.root, directory, filename)
                if bool(unhealthy):
                    entry = np.array(cv2.resize(cv2.imread(file_path), (100, 100)), dtype=np.uint8)
                else:
                    entry = np.array(cv2.imread(file_path), dtype=np.uint8)
                #entry = torchvision.datasets.mnist.read_image_file(file_path)
                if not(bool(unhealthy)):
                    self.data.append(entry)
                    self.targets.append(unhealthy)
                    file_counter += 1
                elif bool(unhealthy):
                    self.data.append(entry)
                    self.targets.append(unhealthy)
                    file_counter += 1
            print(f"Nbr images class {unhealthy}: {file_counter}")
        ##print(self.data)
        #self.data = np.vstack(self.data).reshape(-1, 3, 256, 256)
        #self.data = self.data.transpose((0, 2, 3, 1))  # convert to HWC

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        """
        Args:
            index (int): Index

        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        img, target = self.data[index], self.targets[index]

        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        img = Image.fromarray(img)

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target

    def __len__(self) -> int:
        return len(self.data)



class initialize_dataset:
    def __init__(self, image_resolution=256, batch_size=128, MNIST=True):
        self.image_resolution= image_resolution
        self.batch_size=batch_size
        self.MNIST = MNIST

    def load_dataset(self, transform=False):
        path = "S:/data/Appilyzer/dataset/"
        #path = './data'
        if transform:
            transform = augmentation(image_resolution=self.image_resolution)
        elif self.MNIST:
            transform = transforms.Compose([transforms.ToTensor(), transforms.Resize((self.image_resolution, self.image_resolution)),
                                            transforms.Normalize((0.1307,), (0.3081,))])
        else:
            transform = transforms.Compose([transforms.ToTensor(), transforms.Resize((self.image_resolution, self.image_resolution)),
                        transforms.RandomHorizontalFlip(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

        #if self.MNIST:
        #    train_dataset = torchvision.datasets.MNIST(root=path, train=True,
        #                                                transform = transform,
        #                                                download=True)
        #    test_dataset = torchvision.datasets.MNIST(root=path, train=False,
        #                                            transform = transform,
        #                                            download=True)
        #else:
        #    train_dataset = torchvision.datasets.CIFAR10(root=path, train=True,
        #                                                transform = transform,
        #                                                download=True)
        #    test_dataset = torchvision.datasets.CIFAR10(root=path, train=False,
        #                                            transform = transform,
        #                                            download=True)

        train_dataset = AppylizerHealthDataset(root=path, train=True,
                                                     transform = transform,
                                                     download=True)

        test_dataset = AppylizerHealthDataset(root=path, train=False,
                                               transform=transform,
                                               download=True)

        train_dataloader = torch.utils.data.DataLoader(dataset = train_dataset,
                                                        batch_size=self.batch_size,
                                                        shuffle=True)
        test_dataloader = torch.utils.data.DataLoader(dataset = test_dataset,
                                                        batch_size=self.batch_size,
                                                        shuffle=True)

        return train_dataloader, test_dataloader
