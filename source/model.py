'''Trains a Feed Forward net to classify different hand gestures as Rock, Paper or Scissor'''
import torch
import torch.nn as nn
import gesturedataset
from torch.utils.data import random_split, DataLoader
# pylint: disable=E1101

# hyper parameters
HIDDEN_SIZE = 150
INPUT_SIZE = 21 * 3
NUM_CLASSES = 3
NUM_EPOCHS = 10
BATCH_SIZE = 4
LEARNING_RATE = 0.001
#NUM_WORKERS = 1  kind of annoying creates errors on my machine when passed to data loader

# Initialise dataset and split into train and test sets
model_dataset = gesturedataset.GestureDataset()
total_samples = len(model_dataset)
train_samples = int(0.8 * total_samples)
test_samples = int(0.2 * total_samples)
train_dataset, test_dataset = random_split(model_dataset, (train_samples,test_samples))

# Initialise data loaders
trainset_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE,
                                  shuffle=True)
testset_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE,
                                 shuffle=False)


# Model
class GestureClassifier(nn.Module):
    '''Basic FFN classifier neural net'''
    def __init__(self, input_size, hidden, classes):
        super(GestureClassifier, self).__init__()
        self.lin_1 = nn.Linear(input_size, hidden)
        self.relu = nn.ReLU()
        self.lin_2 = nn.Linear(hidden, classes)

    def forward(self, sample):
        '''inputs x to the model'''
        out = self.lin_1(sample)
        out = self.relu(out)
        out = self.lin_2(out)
        return out

def get_classifier():
    '''Gives a classifier of correct specs'''
    return GestureClassifier(INPUT_SIZE, HIDDEN_SIZE, NUM_CLASSES)

# loss, optimizer, and model
model = get_classifier()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

def train():
    '''Train the model on data from gesturedataset'''
    # training loop
    n_total_steps = len(trainset_loader)
    for epoch in range(NUM_EPOCHS):
        for i, (samples, labels) in enumerate(trainset_loader):
            # forward
            outputs = model(samples)
            loss = criterion(outputs, labels)

            #backward
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i+1)%10 == 0:
                print(f"epoch {epoch+1} / {NUM_EPOCHS}, step {i+1} \
                       / {n_total_steps}, Loss: {loss.item():.4f} ")

    with torch.no_grad():
        n_correct = 0
        n_samples = 0
        for samples, labels in testset_loader:
            outputs = model(samples)
            _, predictions = torch.max(outputs, 1)
            n_samples += labels.shape[0]
            n_correct += (predictions == labels).sum().item()

        acc = 100.0 * n_correct / n_samples
        print(f"accuracy = {acc}")

    save = input("Save the model? y/n")
    if save == 'y':
        torch.save(model.state_dict(), 'source/model/model_weights.pth')
        print("Model saved")


if __name__ == '__main__':
    train()
