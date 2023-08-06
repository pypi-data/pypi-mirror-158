#!/usr/bin/env python3

from typing import List
import pandas as pd
from .utilities import read_utilities
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, Birch
from sklearn.mixture import GaussianMixture


class Dataset:
    def __init__(self) -> None:
        pass

    def load_stats(self, dataset_name: str) -> dict or None:
        """
        Load specific dataset statistics from local.
        Statistics are calculated using the dataset_utilities

        Args:
            dataset_name: str - name of dataset

        Return:
            dict or None - dataset_info.json content or None if dataset is missing in catalogue
        """
        dataset_info = read_utilities.load_dataset_info()
        if dataset_name not in dataset_info:
            print(
                f"Dataset {dataset_name} not present in the local catalogue. To update catalogue, run update_local_info()"
            )
            return None
        else:
            return dataset_info[dataset_name]["stats"]

    def load_description(self, dataset_name: str):
        """
        Load specific dataset descritption from local.
        Description is given by authors and contributors of the dataset

        Args:
            dataset_name: str - name of dataset

        Return:
            dict or None - description provided or None if dataset is missing in catalogue
        """
        dataset_info = read_utilities.load_dataset_info()
        if dataset_name not in dataset_info:
            print(
                f"Dataset {dataset_name} not present in the local catalogue. To update catalogue, run update_local_info()"
            )
            return None
        else:
            return dataset_info[dataset_name]["description"]

    def load(
        self, dataset_name: str, download=False, overwrite=False
    ) -> pd.DataFrame or None:
        """
        Load specific dataset from local. Optionally one can download dataset if specified to local

        Args:
            dataset_name: str - name of dataset
            download: bool - download dataset if missing locally on demand
            overwrite: bool - overwrite downloaded dataset. Used only if download==True

        Return:
            pd.DataFrame or None - dataset data in pd.DataFrame or None if dataset is missing locally or in catalogue
        """
        dataset_info = read_utilities.load_dataset_info()
        if dataset_name not in dataset_info:
            print(
                f"Dataset {dataset_name} not present in the local catalogue. To update catalogue, run update_local_info()"
            )
            return None
        if dataset_name not in self.list(is_print=False):
            if download:
                self.download(dataset_name, overwrite)
            else:
                print(
                    f"Dataset {dataset_name} isn't present in local environment. To allow downloading, specify load(download=True)"
                )
                return None
        return read_utilities.load(dataset_name)

    def download(self, dataset_names: str or List, overwrite=False) -> None:
        """
        Download dataset from source repo. One can pass single dataset name or list of names.

        Args:
            datasets: str or List[str] - one or single dataset names
            overwrite: bool - overwrite if dataset is present
        """
        read_utilities.download(dataset_names, overwrite=overwrite)

    def list(self, is_print: bool = True) -> List:
        """
        Listing all available datasets locally.

        Args:
            is_print: bool - print datasets list if True

        Return:
            filename: List - list of all locally avaliable datasets
        """
        datasets = read_utilities.list_local_datasets()
        if is_print:
            print(datasets)
        return datasets

    def update_local_info_files(self):
        """
        Update local files from github source
        """
        read_utilities.update_local_jsons()


class Methods:
    def __init__(self) -> None:
        pass

    def KMeans(*args):
        return KMeans(args)

    def DBSCAN(*args):
        return DBSCAN(args)

    def AgglomerativeClustering(*args):
        return AgglomerativeClustering(args)

    def GaussianMixture(*args):
        return GaussianMixture(args)

    def Birch(*args):
        return Birch(args)


class Tasks:
    def __init__():
        pass

    def AnomalyDetection(dataset):
        """
        Detect anomalies in the passed dataset
        """
        pass

    def calculate_number_of_clusters(dataset, methods=["kmeans"]):
        """
        Calculater the number of clusters in the passed dataset
        """
        pass

    def cluster_ensembling(dataset, methods=["kmeans", "gmm", "dbscan"]):
        """Provide cluster ensempling"""
        pass

    def cluster_similarity(dataset, method="knn", nearest_neighbors=3):
        """Provides similar known datasets to provided one using knn"""
        pass
