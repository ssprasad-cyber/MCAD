"""
Training pipeline for the MS-GAT anomaly detection model.

Usage (from repo root — activate mcad_cuda env first):

    # Binary mode (UCF-Crime anomaly vs normal)
    cd src
    python models/train_msgat.py \\
        --data_dirs ../data/graphs/anomaly ../data/graphs/normal \\
        --output_dir ../models \\
        --epochs 50 \\
        --lr 1e-3 \\
        --window_size 10 \\
        --balanced

    # Resume from checkpoint
    python models/train_msgat.py \\
        --data_dirs ../data/graphs/anomaly ../data/graphs/normal \\
        --resume ../models/msgat_best.pt
"""

import os
import sys
import argparse
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.msgat_model import MSGAT
from dataset.graph_dataset import GraphDataset, collate_fn, make_sampler
from evaluation.metrics import evaluate
from utils.logger import Logger


def build_loaders(args):
    dataset = GraphDataset(
        data_dirs=args.data_dirs,
        multi_class=False,   # binary mode
        max_samples=args.max_samples
    )

    val_size  = max(1, int(0.2 * len(dataset)))
    train_size = len(dataset) - val_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])

    sampler = make_sampler(train_ds.dataset) if args.balanced else None

    train_loader = DataLoader(
        train_ds,
        batch_size=args.batch_size,
        shuffle=(sampler is None),
        sampler=sampler,
        collate_fn=collate_fn,
        num_workers=0,
        pin_memory=False
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=1,
        shuffle=False,
        collate_fn=collate_fn,
        num_workers=0
    )

    return train_loader, val_loader


def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0

    for windows, labels in loader:
        for window, label in zip(windows, labels):
            window = window.to(device)
            label  = label.to(device)

            optimizer.zero_grad()
            score = model(window).squeeze()
            loss  = criterion(score, label.squeeze())
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

    return total_loss / max(len(loader), 1)


@torch.no_grad()
def validate(model, loader, device):
    model.eval()
    all_scores, all_labels = [], []

    for windows, labels in loader:
        for window, label in zip(windows, labels):
            window = window.to(device)
            score  = model(window).cpu().squeeze().item()
            all_scores.append(score)
            all_labels.append(int(label.item()))

    return all_scores, all_labels


def train(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on: {device}\n")

    train_loader, val_loader = build_loaders(args)

    model = MSGAT(in_dim=5, edge_dim=2, hidden_dim=64).to(device)

    start_epoch = 1
    if args.resume and os.path.exists(args.resume):
        model.load_state_dict(torch.load(args.resume, map_location=device))
        print(f"Resumed from: {args.resume}")

    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=1e-4)
    criterion = nn.BCELoss()
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="max", patience=5, factor=0.5, verbose=True
    )

    os.makedirs(args.output_dir, exist_ok=True)
    exp_dir = os.path.join(args.output_dir, "..", "experiments")
    os.makedirs(exp_dir, exist_ok=True)
    logger = Logger(os.path.join(exp_dir, "results.json"))

    best_auc = 0.0
    best_path = os.path.join(args.output_dir, "msgat_best.pt")

    print(f"{'Epoch':>6}  {'Loss':>8}  {'AUC':>7}  {'F1':>7}  {'P':>7}  {'R':>7}")
    print("-" * 55)

    for epoch in range(start_epoch, args.epochs + 1):
        avg_loss = train_one_epoch(model, train_loader, optimizer, criterion, device)
        scores, labels = validate(model, val_loader, device)
        metrics = evaluate(labels, scores)

        roc_auc = metrics["roc_auc"]
        scheduler.step(roc_auc)

        print(
            f"{epoch:>6}  {avg_loss:>8.4f}  {roc_auc:>7.4f}  "
            f"{metrics['f1']:>7.4f}  {metrics['precision']:>7.4f}  {metrics['recall']:>7.4f}"
        )

        logger.log({
            "epoch":     epoch,
            "loss":      round(avg_loss, 4),
            "roc_auc":   metrics["roc_auc"],
            "precision": metrics["precision"],
            "recall":    metrics["recall"],
            "f1":        metrics["f1"]
        })

        if roc_auc > best_auc:
            best_auc = roc_auc
            torch.save(model.state_dict(), best_path)
            print(f"  ★ New best model saved  (AUC={best_auc:.4f})")

        # Save checkpoint every 10 epochs
        if epoch % 10 == 0:
            ckpt_path = os.path.join(args.output_dir, f"msgat_epoch{epoch:03d}.pt")
            torch.save(model.state_dict(), ckpt_path)

    print(f"\nTraining complete.  Best AUC: {best_auc:.4f}  →  {best_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train MS-GAT for anomaly detection")

    parser.add_argument(
        "--data_dirs", nargs="+",
        default=["../data/graphs/anomaly", "../data/graphs/normal"],
        help="One or more directories containing graph JSON files"
    )
    parser.add_argument("--output_dir", type=str, default="../models")
    parser.add_argument("--epochs",      type=int,   default=50)
    parser.add_argument("--lr",          type=float, default=1e-3)
    parser.add_argument("--batch_size",  type=int,   default=4,
                        help="Windows per gradient step (processed sequentially within each batch)")
    parser.add_argument("--balanced",    action="store_true",
                        help="Use WeightedRandomSampler for class-balanced training")
    parser.add_argument("--resume",      type=str,   default=None,
                        help="Path to checkpoint to resume from")
    parser.add_argument("--max_samples", type=int,   default=None,
                        help="Cap total dataset size (for quick experiments)")

    args = parser.parse_args()
    train(args)
