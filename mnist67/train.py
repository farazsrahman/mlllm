#!/usr/bin/env python3
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms


class SimpleMLP(nn.Module):
    def __init__(self, input_dim=28 * 28, width=64, depth=2, num_classes=2):
        super().__init__()
        layers = []
        in_dim = input_dim
        for _ in range(depth):
            layers.append(nn.Linear(in_dim, width))
            layers.append(nn.ReLU())
            in_dim = width
        layers.append(nn.Linear(in_dim, num_classes))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)


def get_6_vs_7_dataset(dataset_size, val_size=1000):
    """Get 6 vs 7 dataset with fixed-size validation set."""
    mnist_full = datasets.MNIST(root="./data", train=True, download=True, transform=transforms.ToTensor())
    targets = mnist_full.targets
    all_indices = torch.nonzero((targets == 6) | (targets == 7), as_tuple=False).squeeze()
    
    # Extract fixed validation set (same across all dataset_size values)
    torch.manual_seed(42)
    perm = torch.randperm(len(all_indices))
    val_indices = all_indices[perm[:val_size]]
    remaining_indices = all_indices[perm[val_size:]]
    
    # Extract training samples from remaining pool
    actual_train_size = min(dataset_size, len(remaining_indices))
    torch.manual_seed(0)
    train_perm = torch.randperm(len(remaining_indices))[:actual_train_size]
    train_indices = remaining_indices[train_perm]
    
    return Subset(mnist_full, train_indices), Subset(mnist_full, val_indices)


def evaluate(model, val_loader, criterion, device):
    """Evaluate model on validation set."""
    model.eval()
    total_loss, correct, total = 0.0, 0, 0
    with torch.no_grad():
        for images, labels in val_loader:
            images = images.view(images.size(0), -1).to(device)
            labels = (labels == 7).long().to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            total_loss += loss.item() * images.size(0)
            correct += (outputs.argmax(dim=1) == labels).sum().item()
            total += labels.size(0)
    model.train()
    return total_loss / total, correct / total * 100.0


def train(args, seed=None):
    """Train model and return metrics."""
    device = torch.device("cpu")
    val_size = getattr(args, 'val_size', 1000)
    train_dataset, val_dataset = get_6_vs_7_dataset(args.dataset_size, val_size)
    
    if seed is not None:
        torch.manual_seed(seed)
        generator = torch.Generator().manual_seed(seed)
    else:
        generator = None
    
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=0, generator=generator)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=0)
    
    model = SimpleMLP(width=args.model_width, depth=args.model_depth).to(device)
    optimizer = optim.Adam(model.parameters(), lr=args.learning_rate)
    criterion = nn.CrossEntropyLoss()
    
    model.train()
    for epoch in range(args.epochs):
        total_loss, correct, total = 0.0, 0, 0
        for images, labels in train_loader:
            images = images.view(images.size(0), -1).to(device)
            labels = (labels == 7).long().to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * images.size(0)
            correct += (outputs.argmax(dim=1) == labels).sum().item()
            total += labels.size(0)
        
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
    
    # Print only the final validation loss
    print(f"{val_loss:.4f}")
    
    return {
        "train_loss": total_loss / total,
        "train_acc": correct / total * 100.0,
        "val_loss": val_loss,
        "val_acc": val_acc,
        "dataset_size": args.dataset_size,
        "train_size": len(train_dataset),
        "val_size": len(val_dataset),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--learning_rate", type=float, default=1e-3)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--model_width", type=int, default=64)
    parser.add_argument("--model_depth", type=int, default=2)
    parser.add_argument("--dataset_size", type=int, default=2000)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--val_size", type=int, default=1000)
    args = parser.parse_args()
    train(args)
