import torch
from torch.utils.data import DataLoader
import argparse
from datetime import datetime
import logging

import cellshape_cloud as cscloud
from cellshape_cloud.vendor.chamfer_distance import ChamferLoss


from helpers.reports import get_experiment_name
from deep_embedded_clustering import DeepEmbeddedClustering
from training_functions import train


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cellshape-cloud")
    parser.add_argument(
        "--model_type",
        default="cloud",
        type=str,
        choices=["cloud", "voxel"],
        help="Please provide the type of model: [cloud, voxel]",
    )
    parser.add_argument(
        "--cloud_convert",
        default="False",
        type=str2bool,
        help="Do you need to convert 3D images to point clouds?",
    )
    parser.add_argument(
        "--num_points",
        default=2048,
        type=int,
        help="The number of points used in each point cloud.",
    )
    parser.add_argument(
        "--train_type",
        default="DEC",
        type=str,
        choices=["pretrain", "DEC"],
        help="Please provide the type of training mode: [pretrain, full]",
    )
    parser.add_argument(
        "--pretrain",
        default="False",
        type=str2bool,
        help="Please provide whether or not to pretrain the autoencoder",
    )
    parser.add_argument(
        "--tif_dataset_path",
        default="/home/mvries/Documents/CellShape/"
        "UploadData/Dataset/TestConvert/TestTiff/",
        type=str,
        help="Please provide the path to the " "dataset of 3D tif images",
    )
    parser.add_argument(
        "--mesh_dataset_path",
        default="/home/mvries/Documents/CellShape/"
        "UploadData/Dataset/TestConvert/TestMesh/",
        type=str,
        help="Please provide the path to the " "dataset of 3D meshes.",
    )
    parser.add_argument(
        "--cloud_dataset_path",
        default="/home/mvries/Documents/CellShape/"
        "UploadData/cellshapeData/",
        type=str,
        help="Please provide the path to the " "dataset of the point clouds.",
    )
    parser.add_argument(
        "--dataset_type",
        default="SingleCell",
        type=str,
        choices=["SingleCell", "Other"],
        help="Please provide the type of dataset. "
        "If using the one from our paper, then choose 'SingleCell', "
        "otherwise, choose 'Other'.",
    )
    parser.add_argument(
        "--dataframe_path",
        default="/home/mvries/Documents/CellShape/UploadData/"
        "cellshapeData/all_data_removedwrong_ori.csv",
        type=str,
        help="Please provide the path to the dataframe "
        "containing information on the dataset.",
    )
    parser.add_argument(
        "--output_dir",
        default="/home/mvries/Documents/Testing_output/",
        type=str,
        help="Please provide the path for where to save output.",
    )
    parser.add_argument(
        "--num_epochs_autoencoder",
        default=1,
        type=int,
        help="Provide the number of epochs for the autoencoder training.",
    )
    parser.add_argument(
        "--num_epochs_clustering",
        default=3,
        type=int,
        help="Provide the number of epochs for the autoencoder training.",
    )
    parser.add_argument(
        "--num_features",
        default=128,
        type=int,
        help="Please provide the number of features to extract.",
    )
    parser.add_argument(
        "--num_clusters",
        default=3,
        type=int,
        help="Please provide the number of clusters to find.",
    )
    parser.add_argument(
        "--k", default=20, type=int, help="Please provide the value for k."
    )
    parser.add_argument(
        "--encoder_type",
        default="dgcnn",
        type=str,
        help="Please provide the type of encoder.",
    )
    parser.add_argument(
        "--decoder_type",
        default="foldingnetbasic",
        type=str,
        help="Please provide the type of decoder.",
    )
    parser.add_argument(
        "--learning_rate_autoencoder",
        default=0.0001,
        type=float,
        help="Please provide the learning rate "
        "for the autoencoder training.",
    )
    parser.add_argument(
        "--learning_rate_clustering",
        default=0.00001,
        type=float,
        help="Please provide the learning rate "
        "for the autoencoder training.",
    )
    parser.add_argument(
        "--batch_size",
        default=16,
        type=int,
        help="Please provide the batch size.",
    )
    parser.add_argument(
        "--update_interval",
        default=1,
        type=int,
        help="How often to update the target "
        "distribution for the kl divergence.",
    )
    parser.add_argument(
        "--gamma",
        default=1,
        type=int,
        help="Please provide the value for gamma.",
    )
    parser.add_argument(
        "--alpha",
        default=1.0,
        type=float,
        help="Please provide the value for alpha.",
    )
    parser.add_argument(
        "--divergence_tolerance",
        default=0.01,
        type=float,
        help="Please provide the divergence tolerance.",
    )
    parser.add_argument(
        "--proximal",
        default=2,
        type=int,
        help="Do you want to look at cells distal "
        "or proximal to the coverslip?"
        "[0 = distal, 1 = proximal, 2 = both].",
    )
    parser.add_argument(
        "--pretrained_path",
        default=None,
        type=str,
        help="Please provide the path to a pretrained autoencoder.",
    )

    args = parser.parse_args()
    if args.cloud_convert:
        print("Converting tif to point cloud using cellshape-helper")

    autoencoder = cscloud.CloudAutoEncoder(
        num_features=args.num_features,
        k=args.k,
        encoder_type=args.encoder_type,
        decoder_type=args.decoder_type,
    )

    try:
        checkpoint = torch.load(args.autoencoder_path)
    except FileNotFoundError:
        print(
            "This model doesn't exist. "
            "Please check the provided path and try again."
        )
        checkpoint = {"model_state_dict": None}

    try:
        autoencoder.load_state_dict(checkpoint["model_state_dict"])
        print(f"The loss of the loaded model is {checkpoint['loss']}")
    except RuntimeError:
        print("The model architecture given doesn't match the one provided.")
        print("Training from scratch.")
    except AttributeError:
        print("Training from scratch.")

    model = DeepEmbeddedClustering(autoencoder=autoencoder, num_clusters=10)

    dataset = cscloud.PointCloudDataset(args.dataset_path)

    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=False)
    # it is very important that shuffle=False here!
    dataloader_inf = DataLoader(dataset, batch_size=1, shuffle=False)
    # it is very important that batch_size=1 and shuffle=False here!

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=args.learning_rate * 16 / args.batch_size,
        betas=(0.9, 0.999),
        weight_decay=1e-6,
    )

    reconstruction_criterion = ChamferLoss()
    cluster_criterion = torch.nn.KLDivLoss(reduction="sum")

    name_logging, name_model, name_writer, name = get_experiment_name(
        model=model, output_dir=args.output_dir
    )
    logging_info = name_logging, name_model, name_writer, name

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    logging.basicConfig(filename=name_logging, level=logging.INFO)
    logging.info(f"Started training model {name} at {now}.")
    logging.info(f"Loading autoencoder from {args.autoencoder_path}")
    print(
        f"Loading autoencoder from {args.autoencoder_path} "
        f"with loss {checkpoint['loss']}"
    )

    train(
        model=model,
        dataloader=dataloader,
        dataloader_inf=dataloader_inf,
        num_epochs=args.num_epochs,
        optimizer=optimizer,
        reconstruction_criterion=reconstruction_criterion,
        cluster_criterion=cluster_criterion,
        update_interval=args.update_interval,
        gamma=args.gamma,
        divergence_tolerance=args.divergence_tolerance,
        logging_info=logging_info,
    )
