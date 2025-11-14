#!/usr/bin/env python3
"""
train_example.py - Sample training script for testing Trex

This is a working example that simulates a training loop with fake metrics.
Backend teammates can use this to test the job runner and log streaming.

Usage:
    python train_example.py --lr 0.001 --epochs 5 --batch_size 32
    python train_example.py --lr 0.0005 --epochs 10 --batch_size 64
"""

import argparse
import time
import random
import math


def parse_args():
    parser = argparse.ArgumentParser(description="Fake ML training script")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    parser.add_argument("--epochs", type=int, default=5, help="Number of epochs")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    return parser.parse_args()


def fake_training_loop(lr, epochs, batch_size, seed):
    """
    Simulates a training loop with decreasing loss values.
    Prints metrics that can be parsed by the analyzer.
    """
    random.seed(seed)
    
    print(f"Starting training with lr={lr}, epochs={epochs}, batch_size={batch_size}")
    print(f"Using seed: {seed}")
    print("-" * 60)
    
    # Initial loss based on hyperparameters
    initial_loss = 1.0 + random.uniform(-0.1, 0.1)
    
    for epoch in range(1, epochs + 1):
        # Simulate training taking time
        time.sleep(random.uniform(0.5, 1.5))
        
        # Calculate fake loss with exponential decay
        decay_rate = lr * 10
        epoch_noise = random.uniform(-0.05, 0.05)
        train_loss = initial_loss * math.exp(-decay_rate * epoch) + epoch_noise
        train_loss = max(0.01, train_loss)  # Floor at 0.01
        
        # Validation loss is slightly higher
        val_loss = train_loss * (1.1 + random.uniform(0, 0.1))
        
        # Print in a parseable format
        print(f"Epoch {epoch}/{epochs}")
        print(f"  train_loss: {train_loss:.4f}")
        print(f"  val_loss: {val_loss:.4f}")
        print(f"  lr: {lr}")
        
        # Simulate batch progress occasionally
        if epoch % 2 == 0:
            print(f"  batches_processed: {epoch * 100}")
        
        print()
    
    final_val_loss = val_loss
    print("-" * 60)
    print(f"Training complete!")
    print(f"Final validation loss: {final_val_loss:.4f}")
    print(f"Best validation loss: {min(final_val_loss, train_loss):.4f}")
    
    return final_val_loss


def main():
    args = parse_args()
    
    try:
        final_loss = fake_training_loop(
            lr=args.lr,
            epochs=args.epochs,
            batch_size=args.batch_size,
            seed=args.seed
        )
        print(f"\n✓ Run completed successfully with final loss: {final_loss:.4f}")
        return 0
    except Exception as e:
        print(f"\n✗ Training failed with error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
