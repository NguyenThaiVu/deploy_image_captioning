import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from collections import Counter
from PIL import Image

import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torch.nn.utils.rnn import pad_sequence


class Vocabulary:
    """
    This class will build the vocabulary for the words in the captions.
    """
    
    def __init__(self, freq_threshold):
        # setting the reserved tokens for special characters
        self.int_2_str = {0:"<PAD>", 1:"<SOS>", 2:"<EOS>", 3:"<UNK>"}
        
        self.str_2_int = {v:k for k,v in self.int_2_str.items()}
        
        self.freq_threshold = freq_threshold
        
        
    def __len__(self): 
        return len(self.int_2_str)
    
    @staticmethod
    def tokenize(text):
        """
        This function will tokenize the text into words by splitting it by space.
        """
        return [token.lower() for token in text.split()]
    
    def build_vocab(self, sentence_list):
        """
        This is the main function, which will build the vocabulary from the sentence list
        """
        frequencies = Counter()
        idx = 4
        
        for sentence in sentence_list:
            for word in self.tokenize(sentence):
                frequencies[word] += 1
                
                # add the word to the vocab if it reaches minum frequecy threshold
                if frequencies[word] == self.freq_threshold:
                    self.str_2_int[word] = idx
                    self.int_2_str[idx] = word
                    idx += 1
    
    def numericalize(self, text):
        """ 
        For each word in the text corresponding index token for that word form the built vocab.
        """
        tokenized_text = self.tokenize(text)
        list_numerical = []
        
        for token in tokenized_text:
            if token in self.str_2_int:
                list_numerical.append(self.str_2_int[token])
            else:  # word not in vocab
                list_numerical.append(self.str_2_int["<UNK>"])
        return list_numerical
    
    
    
class FlickrDataset(Dataset):
    """
    This class will create a custom dataset for the images and captions. 
    Note: this class is inherrited from torch.utils.data.Dataset. 
            Later, we will use this class to create a dataloader, which is the reason why we define the __len__ and __getitem__ methods.
    """    
    def __init__(self, df, vocab, path_folder_images, transform=None):
        self.df = df
        self.vocab = vocab
        self.path_folder_images = path_folder_images
        self.transform = transform
        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        img_name = self.df.loc[idx, 'image']
        img_path = os.path.join(self.path_folder_images, img_name)
        img = Image.open(img_path).convert('RGB')
        
        caption = self.df.loc[idx, 'caption']
        numericalized_caption = [self.vocab.str_2_int['<SOS>']]
        numericalized_caption += self.vocab.numericalize(caption)
        numericalized_caption.append(self.vocab.str_2_int['<EOS>'])
        
        if self.transform:
            img = self.transform(img)
        
        return img, torch.tensor(numericalized_caption)
    
    
def display_random_image(dataset):
    """
    Display a random image from the dataset
    """
    idx = np.random.randint(0, len(dataset))
    img, caption = dataset[idx]
    print(f"Caption numerical: {caption}")
    print(f"Caption: {' '.join([dataset.vocab.int_2_str[i.item()] for i in caption])}")
    img = img.permute(1, 2, 0)
    plt.imshow(img);
    
    
class Collate:
    """
    This class will be used to pad the captions to the same length for Dataloader.
    """
    def __init__(self, padding_value, batch_first=True):
        self.padding_value = padding_value
        self.batch_first = batch_first
        
    def __call__(self, batch):
        images = [item[0].unsqueeze(0) for item in batch]
        images = torch.cat(images, dim=0)
        
        captions = [item[1] for item in batch]
        captions = pad_sequence(captions, batch_first=self.batch_first, padding_value=self.padding_value)
        
        return images, captions