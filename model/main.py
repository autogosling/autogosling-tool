from PIL import Image
from pathlib import Path
from json import dump
from torchvision.io import read_image
from torch.utils.data import Dataset, DataLoader
import os

def load_image(filename):
    im = Image.open(filename)
    if not im.mode == 'RGB':
        im = im.convert('RGB')
    return im

def load_json(filename):
    with open(filename,"r") as f:
        json_text = f.read()
        return json.loads(json_text)

# Read dataset
class GoslingDataset(Dataset):
    def __init__(self, image_folder, label_folder, bbox_folder):
        self.image_folder = image_folder
        self.label_folder = label_folder
        self.bbox_folder = bbox_folder
        # creates a mapping dictionary that has the shape {`train-images` : {`00001` : `train_images/0001.png`,...}, `train-labels` : {`00001` : `train-labels/00001.json`,...}, `train-bounding-boxes` : ...}
        self.all_mapping_ids_set = {folder_name:self.extract_mapping_ids(folder_name) for folder_name in [image_folder,label_folder,bbox_folder]}
        all_ids = [set(mapping_id.keys()) for mapping_id in self.all_mapping_ids_set]
        self.common_ids = list(set.intersection(*all_ids))
    def extract_mapping_ids(self,folder_path):
        '''Returns a mapping dictionary that has the shape {`00001` : `train-images/00001.png`, `00002` : `train_images/00002.png`, ...}'''
        ids = {Path(filename).stem : os.path.join(folder_path,filename) for filename in os.listdir(folder_path)}
        return ids
    
    
    def __len__(self):
        return len(self.common_ids)
    
    def __getitem__(self,idx):
        sample_id = self.common_ids[idx]
        image_filename = self.all_mapping_ids_set[self.image_folder][sample_id]
        bbox_filename = self.all_mapping_ids_set[self.bbox_folder][sample_id]
        label_filename = self.all_mapping_ids_set[self.label_folder][sample_id]

        bbox_json = load_json(bbox_filename)    
        label_json = load_json(label_filename)

        image_data = load_image(image_filename)
        return image_data, bbox_json, label_json

train_config = {
    "image_folder" : "data/train-images",
    "label_folder" : "data/train-label",
    "bbox_folder" : "data/train-bbox"
}

test_config = {
    "image_folder" : "data/test-images",
    "label_folder" : "data/test-label",
    "bbox_folder" : "data/test-bbox"
}
train_dataset = GoslingDataset(**train_config)
test_dataset = GoslingDataset(**test_config)




