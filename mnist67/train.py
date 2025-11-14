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


def get_6_vs_7_dataset(dataset_size, train=True, val_split=0.2):
    transform = transforms.ToTensor()
    mnist_full = datasets.MNIST(
        root="./data",
        train=train,
        download=True,
        transform=transform,
    )

    targets = mnist_full.targets
    mask = (targets == 6) | (targets == 7)
    indices = torch.nonzero(mask, as_tuple=False).squeeze()

    if dataset_size is not None and dataset_size > 0:
        dataset_size = min(dataset_size, indices.numel())
        torch.manual_seed(0)
        perm = torch.randperm(indices.numel())[:dataset_size]
        indices = indices[perm]

    # Split into train and val if training
    if train and val_split > 0:
        split_idx = int(len(indices) * (1 - val_split))
        torch.manual_seed(0)
        perm = torch.randperm(len(indices))
        indices = indices[perm]
        train_indices = indices[:split_idx]
        val_indices = indices[split_idx:]
        train_subset = Subset(mnist_full, train_indices)
        val_subset = Subset(mnist_full, val_indices)
        return train_subset, val_subset
    else:
        subset = Subset(mnist_full, indices)
        return subset


def evaluate(model, val_loader, criterion, device):
    """Evaluate model on validation set."""
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in val_loader:
            images = images.view(images.size(0), -1).to(device)
            labels = (labels == 7).long().to(device)  # 6 -> 0, 7 -> 1
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            total_loss += loss.item() * images.size(0)
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
    
    model.train()
    avg_loss = total_loss / total if total > 0 else 0.0
    acc = correct / total * 100.0 if total > 0 else 0.0
    return avg_loss, acc


def train(args):
    device = torch.device("cpu")

    # Get train and validation datasets
    train_dataset, val_dataset = get_6_vs_7_dataset(
        args.dataset_size, train=True, val_split=args.val_split
    )
    train_loader = DataLoader(
        train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=0
    )
    val_loader = DataLoader(
        val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=0
    )

    model = SimpleMLP(width=args.model_width, depth=args.model_depth).to(device)
    optimizer = optim.Adam(model.parameters(), lr=args.learning_rate)
    criterion = nn.CrossEntropyLoss()

    model.train()
    
    for epoch in range(args.epochs):
        total_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images = images.view(images.size(0), -1).to(device)
            labels = (labels == 7).long().to(device)  # 6 -> 0, 7 -> 1

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * images.size(0)
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        # Evaluate on validation set at end of epoch
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        
        avg_loss = total_loss / total
        acc = correct / total * 100.0
        print(
            f"Epoch {epoch + 1}/{args.epochs} "
            f"- train_loss: {avg_loss:.4f} - train_acc: {acc:.2f}% "
            f"- val_loss: {val_loss:.4f} - val_acc: {val_acc:.2f}%"
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train a simple MLP to classify 6 vs 7 on MNIST."
    )
    parser.add_argument("--learning_rate", type=float, default=1e-3)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--model_width", type=int, default=64)
    parser.add_argument("--model_depth", type=int, default=2)
    parser.add_argument(
        "--dataset_size",
        type=int,
        default=2000,
        help="Number of (6/7) training examples to use (<= available).",
    )
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument(
        "--val_split",
        type=float,
        default=0.2,
        help="Fraction of dataset to use for validation.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train(args)