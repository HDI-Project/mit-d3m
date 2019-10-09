# -*- coding: utf-8 -*-

"""Top-level package for mit-d3m."""

__author__ = """MIT Data To AI Lab"""
__email__ = 'dailabmit@gmail.com'
__version__ = '0.2.1-dev0'

import os
import shutil
import tarfile

import boto3
import botocore
import botocore.config
from funcy import memoize

from mit_d3m.dataset import D3MDS
from mit_d3m.loaders import get_loader
from mit_d3m.metrics import METRICS_DICT

DATA_PATH = 'data'
BUCKET = 'd3m-data-dai'


@memoize
def get_client():
    config = botocore.config.Config(signature_version=botocore.UNSIGNED)
    client = boto3.client('s3', config=config)
    return client


def download_dataset(bucket, dataset, root_dir):
    client = get_client()
    print("Downloading dataset {}".format(dataset))
def get_dataset_tarfile_path(datapath, dataset):
    return os.path.join(datapath, '{dataset}.tar.gz'.format(dataset=dataset))


def get_dataset_dir(datapath, dataset):
    return os.path.join(datapath, dataset)


    key = 'datasets/' + dataset + '.tar.gz'
    filename = root_dir + '.tar.gz'
def get_dataset_s3_key(dataset):
    return 'datasets/{dataset}.tar.gz'.format(dataset=dataset)

    print("Getting file {} from S3 bucket {}".format(key, bucket))
    client.download_file(Bucket=bucket, Key=key, Filename=filename)

    shutil.rmtree(root_dir, ignore_errors=True)

    print("Extracting {}".format(filename))
    with tarfile.open(filename, 'r:gz') as tf:
        tf.extractall(os.path.dirname(root_dir))
def contains_files(d):
    for _, _, files in os.walk(d):
        if files:
            return True
    return False


def extract_dataset(src, dst):
    print("Extracting {}".format(src))
    shutil.rmtree(dst, ignore_errors=True)
    with tarfile.open(src, 'r:gz') as tf:
        tf.extractall(dst)


def load_d3mds(dataset, root=DATA_PATH, force_download=False):
    if dataset.endswith('_dataset_TRAIN'):
        dataset = dataset[:-14]

    root_dir = os.path.join(root, dataset)

    if root == DATA_PATH and (force_download or not os.path.exists(root_dir)):
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)

        download_dataset(BUCKET, dataset, root_dir)

    phase_root = os.path.join(root_dir, 'TRAIN')
    dataset_path = os.path.join(phase_root, 'dataset_TRAIN')
    problem_path = os.path.join(phase_root, 'problem_TRAIN')

    return D3MDS(dataset=dataset_path, problem=problem_path)


def load_dataset(dataset, root=DATA_PATH, force_download=False):

    d3mds = load_d3mds(dataset, root, force_download)

    loader = get_loader(
        d3mds.get_data_modality(),
        d3mds.get_task_type()
    )

    dataset = loader.load(d3mds)

    dataset.scorer = METRICS_DICT[d3mds.get_metric()]

    return dataset
